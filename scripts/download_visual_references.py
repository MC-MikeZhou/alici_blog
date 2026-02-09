#!/usr/bin/env python3
"""
Download visual reference images for a report's "cases" Markdown files.

Design goals:
- No third-party deps (stdlib only)
- Best-effort scraping (meta og:image + <img> tags + srcset)
- Deterministic folder layout: visual-references/<category>/<case-slug>/
- Per-case manifest + README for usage notes and attribution reminders

Note: Some sources (e.g. Instagram/X) may require login/cookies and may not be
scrapable automatically. In those cases we still create folders/manifests and
record failures for manual follow-up.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


URL_RE = re.compile(r"https?://[^\s<>\")\]]+")


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _safe_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "untitled"


def _normalize_url(url: str) -> str:
    url = url.strip()
    url = url.rstrip(").,;!?:'\"")
    return url


def _is_placeholder_url(url: str) -> bool:
    host = urllib.parse.urlparse(url).hostname or ""
    if host in {"example.com", "www.example.com", "localhost", "127.0.0.1"}:
        return True
    return False


def extract_urls_from_markdown(md_text: str) -> List[str]:
    urls: List[str] = []
    for m in URL_RE.finditer(md_text):
        url = _normalize_url(m.group(0))
        if not url:
            continue
        if _is_placeholder_url(url):
            continue
        urls.append(url)
    # stable de-dupe, preserving order
    seen: Set[str] = set()
    out: List[str] = []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def _looks_like_image_url(url: str) -> bool:
    path = urllib.parse.urlparse(url).path.lower()
    return any(
        path.endswith(ext)
        for ext in (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif",
            ".bmp",
            ".tif",
            ".tiff",
            ".avif",
            ".svg",
        )
    )


def _should_skip_image_url(url: str, include_svg: bool) -> bool:
    u = url.lower()
    if u.startswith("data:"):
        return True
    if any(
        k in u
        for k in (
            "favicon",
            "sprite",
            "doubleclick",
            "googlesyndication",
            "pixel",
            "tracker",
            "tracking",
            "/logo",
            "logo.",
            "logo_",
            "logo-",
            "/icon",
            "icon.",
            "icon_",
            "icon-",
            "/avatar",
            "avatar.",
            "avatar_",
            "avatar-",
            "profile_pic",
            "badge",
            "spinner",
            "loading",
            "placeholder",
            "share",
            "social",
            "button",
            "btn",
            "appstore",
            "playstore",
            "header",
            "footer",
            "navbar",
            "nav-",
            "cookie",
            "consent",
            "adsystem",
            "adservice",
        )
    ):
        return True
    if not include_svg and (u.endswith(".svg") or "image/svg" in u):
        return True

    # Heuristic: skip very small responsive assets indicated by width/height params.
    try:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        dims: List[int] = []
        for key in ("w", "width", "h", "height"):
            if key in q and q[key]:
                try:
                    dims.append(int(str(q[key][0])))
                except ValueError:
                    pass
        if dims and max(dims) <= 120:
            return True
    except Exception:
        pass
    return False


def _guess_ext(content_type: str, url: str) -> str:
    ct = (content_type or "").split(";")[0].strip().lower()
    mapping = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/avif": ".avif",
        "image/tiff": ".tiff",
        "image/svg+xml": ".svg",
    }
    if ct in mapping:
        return mapping[ct]
    path = urllib.parse.urlparse(url).path
    _, ext = os.path.splitext(path)
    if ext and re.fullmatch(r"\.[A-Za-z0-9]{1,5}", ext):
        return ext.lower()
    return ".bin"


class _ImgExtractor(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.image_urls: List[str] = []

    def handle_starttag(self, tag: str, attrs: Sequence[Tuple[str, Optional[str]]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}

        if tag.lower() == "meta":
            prop = (attr_map.get("property") or attr_map.get("name") or "").lower()
            if prop in {
                "og:image",
                "og:image:url",
                "twitter:image",
                "twitter:image:src",
            }:
                content = attr_map.get("content", "").strip()
                if content:
                    self.image_urls.append(content)
            return

        if tag.lower() == "link":
            rel = (attr_map.get("rel") or "").lower()
            if "image_src" in rel:
                href = attr_map.get("href", "").strip()
                if href:
                    self.image_urls.append(href)
            return

        if tag.lower() != "img":
            return

        candidates: List[str] = []
        for key in ("src", "data-src", "data-original", "data-lazy-src"):
            v = attr_map.get(key, "").strip()
            if v:
                candidates.append(v)

        srcset = attr_map.get("srcset", "").strip()
        if srcset:
            # pick the largest candidate by width descriptor when available
            parsed: List[Tuple[int, str]] = []
            for part in srcset.split(","):
                part = part.strip()
                if not part:
                    continue
                toks = part.split()
                url = toks[0]
                width = 0
                if len(toks) >= 2 and toks[1].endswith("w"):
                    try:
                        width = int(toks[1][:-1])
                    except ValueError:
                        width = 0
                parsed.append((width, url))
            if parsed:
                parsed.sort(key=lambda x: x[0])
                candidates.append(parsed[-1][1])

        for c in candidates:
            if c:
                self.image_urls.append(c)


@dataclass(frozen=True)
class CaseRef:
    category: str
    slug: str
    title: str
    md_path: Path
    source_urls: Tuple[str, ...]

    @property
    def out_dir_name(self) -> str:
        return self.slug


def discover_cases(cases_dir: Path) -> List[CaseRef]:
    cases: List[CaseRef] = []
    for md_path in sorted(cases_dir.rglob("*.md")):
        rel = md_path.relative_to(cases_dir)
        category = rel.parts[0] if len(rel.parts) > 1 else "uncategorized"
        slug = md_path.stem
        title = slug.replace("-", " ").title()
        try:
            text = md_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        urls = tuple(extract_urls_from_markdown(text))
        cases.append(CaseRef(category=category, slug=slug, title=title, md_path=md_path, source_urls=urls))
    return cases


def _http_get(
    url: str,
    *,
    timeout_s: int,
    user_agent: str,
    referer: Optional[str] = None,
    max_bytes: Optional[int] = None,
    retries: int = 2,
) -> Tuple[bytes, Dict[str, str]]:
    last_err: Optional[BaseException] = None
    headers = {"User-Agent": user_agent, "Accept": "*/*"}
    if referer:
        headers["Referer"] = referer

    req = urllib.request.Request(url, headers=headers, method="GET")
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                info = {k.lower(): v for k, v in resp.headers.items()}
                if max_bytes is None:
                    data = resp.read()
                else:
                    data = resp.read(max_bytes + 1)
                    if len(data) > max_bytes:
                        raise ValueError(f"response too large (> {max_bytes} bytes): {url}")
                return data, info
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt < retries:
                time.sleep(0.6 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"unreachable: {last_err}")


def extract_image_urls_from_html(html: str, base_url: str) -> List[str]:
    parser = _ImgExtractor(base_url=base_url)
    try:
        parser.feed(html)
    except Exception:
        # HTML can be malformed; still try best-effort on partial parse
        pass
    raw = parser.image_urls
    out: List[str] = []
    seen: Set[str] = set()
    for u in raw:
        if not u:
            continue
        abs_u = urllib.parse.urljoin(base_url, u)
        abs_u = _normalize_url(abs_u)
        if abs_u in seen:
            continue
        seen.add(abs_u)
        out.append(abs_u)
    return out


def ensure_case_readme(case_dir: Path, case_ref: CaseRef) -> None:
    readme = case_dir / "README.md"
    if readme.exists():
        return
    lines = [
        f"# Visual References — {case_ref.title}",
        "",
        "## Sources",
        "",
    ]
    if case_ref.source_urls:
        for u in case_ref.source_urls:
            lines.append(f"- {u}")
    else:
        lines.append("- (no URLs found in case markdown)")
    lines += [
        "",
        "## Usage",
        "",
        "- Internal reference only: use these images to understand style, composition, UI steps, or data charts.",
        "- Before publishing: verify licensing/terms and add attribution/citation as needed.",
        "- If a source blocks scraping (e.g. X/Instagram paywalls/login): use the URL above to screenshot manually.",
        "",
        f"_Generated: {_now_iso()}_",
        "",
    ]
    readme.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(case_dir: Path, manifest: dict) -> None:
    (case_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def download_images_for_case(
    case_ref: CaseRef,
    *,
    out_root: Path,
    timeout_s: int,
    user_agent: str,
    retries: int,
    max_images_per_source: int,
    max_images_per_case: int,
    include_svg: bool,
    dry_run: bool,
    skip_domains: Set[str],
) -> dict:
    case_dir = out_root / case_ref.category / case_ref.out_dir_name
    case_dir.mkdir(parents=True, exist_ok=True)
    ensure_case_readme(case_dir, case_ref)

    manifest_path = case_dir / "manifest.json"
    existing_downloads: List[dict] = []
    existing_errors: List[dict] = []
    if manifest_path.exists():
        try:
            prev = json.loads(manifest_path.read_text(encoding="utf-8"))
            existing_downloads = list(prev.get("downloads") or [])
            existing_errors = list(prev.get("errors") or [])
        except Exception:
            existing_downloads = []
            existing_errors = []

    manifest = {
        "case": {
            "title": case_ref.title,
            "slug": case_ref.slug,
            "category": case_ref.category,
            "source_markdown": str(case_ref.md_path),
        },
        "generated_at": _now_iso(),
        "sources": [],
        "downloads": existing_downloads,
        "errors": existing_errors,
    }

    img_counter = len(existing_downloads)
    seen_img_urls: Set[str] = {d.get("image_url", "") for d in existing_downloads if d.get("image_url")}
    seen_sha: Set[str] = {d.get("sha256", "") for d in existing_downloads if d.get("sha256")}
    writes_since = 0

    for src_url in case_ref.source_urls:
        if img_counter >= max_images_per_case:
            break

        src_entry = {"url": src_url, "image_urls": [], "note": ""}
        manifest["sources"].append(src_entry)
        write_manifest(case_dir, manifest)

        host = (urllib.parse.urlparse(src_url).hostname or "").lower()
        if host in skip_domains:
            src_entry["note"] = f"Skipped by domain rule: {host}"
            write_manifest(case_dir, manifest)
            continue

        try:
            candidate_imgs: List[str] = []

            if _looks_like_image_url(src_url):
                candidate_imgs = [src_url]
            else:
                data, headers = _http_get(
                    src_url,
                    timeout_s=timeout_s,
                    user_agent=user_agent,
                    referer=None,
                    max_bytes=5_000_000,
                    retries=retries,
                )
                content_type = headers.get("content-type", "")
                if content_type.lower().startswith("image/"):
                    candidate_imgs = [src_url]
                else:
                    html = data.decode("utf-8", errors="replace")
                    candidate_imgs = extract_image_urls_from_html(html, base_url=src_url)

            # filter + cap per source
            filtered: List[str] = []
            for u in candidate_imgs:
                if _should_skip_image_url(u, include_svg=include_svg):
                    continue
                if u in seen_img_urls:
                    continue
                filtered.append(u)
            filtered = filtered[:max_images_per_source]

            src_entry["image_urls"] = filtered
            if not filtered:
                src_entry["note"] = "No images discovered (or blocked)."
                continue

            for img_url in filtered:
                if img_counter >= max_images_per_case:
                    break
                if dry_run:
                    img_counter += 1
                    continue

                try:
                    img_bytes, img_headers = _http_get(
                        img_url,
                        timeout_s=timeout_s,
                        user_agent=user_agent,
                        referer=src_url,
                        max_bytes=25_000_000,
                        retries=retries,
                    )
                    # Likely an icon/pixel; skip but still persist progress occasionally.
                    if len(img_bytes) < 10_000:
                        writes_since += 1
                        if writes_since >= 25:
                            write_manifest(case_dir, manifest)
                            writes_since = 0
                        # likely an icon/pixel; skip quietly
                        continue

                    sha = hashlib.sha256(img_bytes).hexdigest()
                    if sha in seen_sha:
                        continue
                    seen_sha.add(sha)

                    ct = img_headers.get("content-type", "")
                    ext = _guess_ext(ct, img_url)
                    domain = urllib.parse.urlparse(img_url).hostname or "unknown"
                    domain_slug = _safe_slug(domain.replace(".", "-"))[:40]
                    fname = f"{img_counter+1:03d}--{domain_slug}--{sha[:10]}{ext}"
                    tmp_path = case_dir / (fname + ".tmp")
                    out_path = case_dir / fname
                    tmp_path.write_bytes(img_bytes)
                    tmp_path.replace(out_path)

                    manifest["downloads"].append(
                        {
                            "source_url": src_url,
                            "image_url": img_url,
                            "file": str(out_path),
                            "sha256": sha,
                            "content_type": ct,
                            "bytes": len(img_bytes),
                        }
                    )
                    img_counter += 1
                    writes_since += 1
                    if writes_since >= 10:
                        write_manifest(case_dir, manifest)
                        writes_since = 0
                except Exception as e:  # noqa: BLE001
                    manifest["errors"].append({"source_url": src_url, "image_url": img_url, "error": repr(e)})
        except Exception as e:  # noqa: BLE001
            manifest["errors"].append({"source_url": src_url, "error": repr(e)})
        # persist progress after each source URL (important for long pages/threads)
        write_manifest(case_dir, manifest)

    write_manifest(case_dir, manifest)
    return manifest


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Download case visual reference images into local folders.")
    p.add_argument(
        "--report-dir",
        default=".",
        help="Report root directory (contains cases/ and visual-references/). Default: current dir.",
    )
    p.add_argument(
        "--cases-dir",
        default=None,
        help="Cases directory. Default: <report-dir>/cases",
    )
    p.add_argument(
        "--out-dir",
        default=None,
        help="Output directory. Default: <report-dir>/visual-references",
    )
    p.add_argument("--case", default=None, help="Only run for a single case slug (e.g. aitana-lopez).")
    p.add_argument("--plan-only", action="store_true", help="Only create folders/READMEs and print URLs; no network.")
    p.add_argument("--dry-run", action="store_true", help="Fetch pages but do not download images.")
    p.add_argument("--timeout", type=int, default=25, help="HTTP timeout seconds.")
    p.add_argument("--retries", type=int, default=2, help="HTTP retries per request.")
    p.add_argument("--max-images-per-source", type=int, default=80, help="Cap images extracted per source URL.")
    p.add_argument("--max-images-per-case", type=int, default=250, help="Cap total images downloaded per case.")
    p.add_argument("--include-svg", action="store_true", help="Also download SVG images.")
    p.add_argument(
        "--skip-domain",
        action="append",
        default=[],
        help="Skip source URLs from this exact hostname (repeatable), e.g. --skip-domain github.com",
    )
    p.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="User-Agent header.")
    args = p.parse_args(argv)

    report_dir = Path(args.report_dir).expanduser().resolve()
    cases_dir = Path(args.cases_dir).expanduser().resolve() if args.cases_dir else (report_dir / "cases")
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else (report_dir / "visual-references")

    if not cases_dir.exists():
        print(f"cases dir not found: {cases_dir}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    cases = discover_cases(cases_dir)
    if args.case:
        cases = [c for c in cases if c.slug == args.case]
        if not cases:
            print(f"case not found: {args.case}", file=sys.stderr)
            return 2

    if args.plan_only:
        for c in cases:
            case_dir = out_dir / c.category / c.out_dir_name
            case_dir.mkdir(parents=True, exist_ok=True)
            ensure_case_readme(case_dir, c)
            write_manifest(
                case_dir,
                {
                    "case": {
                        "title": c.title,
                        "slug": c.slug,
                        "category": c.category,
                        "source_markdown": str(c.md_path),
                    },
                    "generated_at": _now_iso(),
                    "sources": [{"url": u} for u in c.source_urls],
                    "downloads": [],
                    "errors": [],
                    "note": "plan-only: no network requests were made",
                },
            )
        print(f"Planned {len(cases)} case folders under: {out_dir}")
        return 0

    skip_domains = {d.lower().strip() for d in (args.skip_domain or []) if d.strip()}

    global_summary = {
        "report_dir": str(report_dir),
        "cases_dir": str(cases_dir),
        "out_dir": str(out_dir),
        "generated_at": _now_iso(),
        "cases": [],
    }

    for c in cases:
        manifest = download_images_for_case(
            c,
            out_root=out_dir,
            timeout_s=args.timeout,
            user_agent=args.user_agent,
            retries=args.retries,
            max_images_per_source=args.max_images_per_source,
            max_images_per_case=args.max_images_per_case,
            include_svg=args.include_svg,
            dry_run=args.dry_run,
            skip_domains=skip_domains,
        )
        global_summary["cases"].append(
            {
                "slug": c.slug,
                "category": c.category,
                "downloads": len(manifest.get("downloads", [])),
                "errors": len(manifest.get("errors", [])),
                "manifest": str((out_dir / c.category / c.out_dir_name / "manifest.json").resolve()),
            }
        )

    (out_dir / "SUMMARY.json").write_text(
        json.dumps(global_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Done. Summary: {out_dir / 'SUMMARY.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
