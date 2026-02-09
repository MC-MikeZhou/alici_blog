#!/usr/bin/env python3
"""
Basecamp Todolist Puller -> Context Pack

Fetches a Basecamp 4 todolist (and its child lists via groups) using OAuth env vars
and writes a local "context pack":

  <out>/
    01-basecamp-raw/...
    02-basecamp-normalized/context.json
    03-basecamp-digest/context.md

Notes:
- Read-only by default.
- Never prints secrets (BC_ACCESS_TOKEN / client secret).
- Uses stdlib only (urllib), consistent with other AliciBlog scripts.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import http.client
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


APP_TODOLIST_RE = re.compile(
    r"^https?://3\.basecamp\.com/(?P<account>\d+)/buckets/(?P<bucket>\d+)/todolists/(?P<todolist>\d+)(?:/todos)?/?(?:\?.*)?$"
)
APP_ANY_TODOLIST_LINK_RE = re.compile(
    r"https?://3\.basecamp\.com/(?P<account>\d+)/buckets/(?P<bucket>\d+)/todolists/(?P<todolist>\d+)"
)


def load_env_file_if_present(env_path: str) -> None:
    if not env_path:
        return
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                if key.startswith("export "):
                    key = key[len("export ") :].strip()
                val = val.strip().strip('"').strip("'")
                if not key:
                    continue
                # If env var exists but is blank, allow env-file to fill it.
                if (key not in os.environ) or (not (os.environ.get(key) or "").strip()):
                    os.environ[key] = val
    except OSError:
        return


def parse_app_todolist_url(app_url: str) -> tuple[str, str, str]:
    m = APP_TODOLIST_RE.match(app_url.strip())
    if not m:
        raise ValueError(f"Unsupported Basecamp todolist URL: {app_url}")
    return (m.group("account"), m.group("bucket"), m.group("todolist"))


def extract_linked_todolists(description_html: str) -> list[str]:
    if not description_html:
        return []
    links = []
    for m in APP_ANY_TODOLIST_LINK_RE.finditer(description_html):
        links.append(m.group(0))
    # stable, de-duped
    seen: set[str] = set()
    out: list[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            out.append(link)
    return out


def _parse_next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    # RFC 5988-ish: <url>; rel="next", <url>; rel="prev"
    for part in link_header.split(","):
        part = part.strip()
        if 'rel="next"' not in part:
            continue
        m = re.search(r"<([^>]+)>", part)
        if m:
            return m.group(1)
    return None


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    headers: dict[str, str]
    body_text: str


def http_get_json(
    *,
    url: str,
    access_token: str,
    user_agent: str,
    timeout_s: int = 60,
    max_retries: int = 3,
) -> FetchResult:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": user_agent,
            "Accept": "application/json",
        },
        method="GET",
    )

    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                status = int(getattr(resp, "status", 200))
                headers = {k.lower(): v for k, v in resp.headers.items()}
                try:
                    raw = resp.read()
                except http.client.IncompleteRead as e:
                    # Retry on truncated HTTP bodies.
                    if attempt <= max_retries:
                        time.sleep(min(1.0 * (2 ** (attempt - 1)), 10.0))
                        continue
                    raw = e.partial or b""
            text = raw.decode("utf-8", errors="replace")
            return FetchResult(url=url, status=status, headers=headers, body_text=text)
        except urllib.error.HTTPError as e:
            status = int(getattr(e, "code", 0) or 0)
            if status in (429, 500, 502, 503, 504) and attempt <= max_retries:
                retry_after = e.headers.get("Retry-After")
                sleep_s = 1.0 * (2 ** (attempt - 1))
                if retry_after:
                    try:
                        sleep_s = max(sleep_s, float(retry_after))
                    except ValueError:
                        pass
                time.sleep(min(sleep_s, 10.0))
                continue
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
            return FetchResult(url=url, status=status, headers=headers, body_text=body)
        except urllib.error.URLError:
            if attempt <= max_retries:
                time.sleep(min(1.0 * (2 ** (attempt - 1)), 10.0))
                continue
            raise


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_json_loads(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def fetch_paged_array(
    *,
    first_url: str,
    access_token: str,
    user_agent: str,
    raw_dir: Path,
    basename: str,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    url = first_url
    page = 1
    while url:
        res = http_get_json(url=url, access_token=access_token, user_agent=user_agent)
        write_text(raw_dir / f"{basename}_p{page}.headers.txt", "\n".join(f"{k}: {v}" for k, v in res.headers.items()) + "\n")
        write_text(raw_dir / f"{basename}_p{page}.json", res.body_text)
        data = safe_json_loads(res.body_text)
        if isinstance(data, list):
            for it in data:
                if isinstance(it, dict):
                    items.append(it)
        next_url = _parse_next_link(res.headers.get("link"))
        url = next_url
        page += 1
        if page > 50:
            # safety: avoid infinite loops if headers are weird
            break
    return items


def fetch_single(
    *,
    url: str,
    access_token: str,
    user_agent: str,
    raw_dir: Path,
    filename: str,
) -> Any:
    res = http_get_json(url=url, access_token=access_token, user_agent=user_agent)
    write_text(raw_dir / f"{filename}.headers.txt", "\n".join(f"{k}: {v}" for k, v in res.headers.items()) + "\n")
    write_text(raw_dir / f"{filename}.json", res.body_text)
    return safe_json_loads(res.body_text)


def normalize_todolist(obj: dict[str, Any], *, parent_root_id: int | None) -> dict[str, Any]:
    return {
        "id": int(obj.get("id")) if obj.get("id") is not None else None,
        "name": obj.get("name") or obj.get("title") or "",
        "app_url": obj.get("app_url") or "",
        "url": obj.get("url") or "",
        "bucket_id": (obj.get("bucket") or {}).get("id") if isinstance(obj.get("bucket"), dict) else None,
        "bucket_name": (obj.get("bucket") or {}).get("name") if isinstance(obj.get("bucket"), dict) else None,
        "parent_root_id": parent_root_id,
        "description_html": obj.get("description") or "",
        "status": obj.get("status") or "",
        "completed_ratio": obj.get("completed_ratio") or "",
        "updated_at": obj.get("updated_at") or "",
    }


def normalize_todo(obj: dict[str, Any], *, list_id: int) -> dict[str, Any]:
    assignees = []
    for a in obj.get("assignees") or []:
        if isinstance(a, dict) and a.get("name"):
            assignees.append(a.get("name"))
    return {
        "id": int(obj.get("id")) if obj.get("id") is not None else None,
        "list_id": int(list_id),
        "status": obj.get("status") or "",
        "content": (obj.get("content") or "").strip(),
        "description_html": obj.get("description") or "",
        "due_on": obj.get("due_on"),
        "assignees": assignees,
        "created_at": obj.get("created_at"),
        "updated_at": obj.get("updated_at"),
        "url": obj.get("url") or "",
        "app_url": obj.get("app_url") or "",
    }


def render_digest(context: dict[str, Any]) -> str:
    today = _dt.date.today().isoformat()
    roots: list[dict[str, Any]] = list(context.get("sources") or [])
    lists: list[dict[str, Any]] = list(context.get("lists") or [])
    todos: list[dict[str, Any]] = list(context.get("todos") or [])

    todos_by_list: dict[int, list[dict[str, Any]]] = {}
    for t in todos:
        lid = int(t.get("list_id") or 0)
        todos_by_list.setdefault(lid, []).append(t)

    lines: list[str] = []
    lines.append(f"# Basecamp Context Digest")
    lines.append("")
    lines.append(f"- generated_at: {today}")
    lines.append("")
    lines.append("## 1. Roots")
    lines.append("")
    for s in roots:
        lines.append(f"- {s.get('name','').strip()} ({s.get('app_url','')})")
    lines.append("")

    lines.append("## 2. Lists And Todos")
    lines.append("")
    for li in sorted(lists, key=lambda x: (x.get("parent_root_id") or 0, x.get("id") or 0)):
        lid = li.get("id")
        if not isinstance(lid, int):
            continue
        title = (li.get("name") or "").strip()
        app_url = li.get("app_url") or ""
        lines.append(f"### {title}")
        if app_url:
            lines.append(f"- app_url: {app_url}")
        items = todos_by_list.get(lid, [])
        if not items:
            lines.append("- todos: (empty)")
            lines.append("")
            continue
        for t in items:
            content = (t.get("content") or "").strip()
            status = t.get("status") or ""
            tid = t.get("id")
            if len(content) > 160:
                content = content[:157] + "..."
            lines.append(f"- [{status}] {tid} {content}")
        lines.append("")

    # heuristic constraints
    hay = "\n".join((t.get("content") or "") for t in todos)
    constraint_signals = [
        ("InVideo competitor", ["Invideo", "InVideo"]),
        ("Landing page", ["落地页", "landing page", "landpage"]),
        ("Use case library", ["Use Case", "use case", "案例"]),
        ("Official creative centers", ["Creative Center", "创意中心", "Tiktok", "TikTok", "Instagram", "YouTube"]),
        ("UGC ads mode / demo", ["UGC Ads Mode", "UGC Ads", "demo", "模式"]),
        ("Pricing / unit economics", ["单价", "价格", "benchmarks", "CPM", "CPA", "ROI"]),
    ]
    matched: list[str] = []
    for label, keys in constraint_signals:
        for k in keys:
            if k.lower() in hay.lower():
                matched.append(label)
                break
    matched = sorted(set(matched))

    lines.append("## 3. Extracted Research Constraints")
    lines.append("")
    if matched:
        for m in matched:
            lines.append(f"- {m}")
    else:
        lines.append("- (none detected)")
    lines.append("")

    # gaps
    empty_lists = []
    for li in lists:
        lid = li.get("id")
        if isinstance(lid, int) and not todos_by_list.get(lid):
            empty_lists.append(li)
    lines.append("## 4. Gaps / Empty Lists")
    lines.append("")
    if empty_lists:
        for li in empty_lists:
            lines.append(f"- {li.get('name','').strip()} ({li.get('app_url','')})")
    else:
        lines.append("- (none)")
    lines.append("")

    return "\n".join(lines)


def build_context_pack(
    *,
    app_url: str,
    out_dir: Path,
    follow_linked: bool,
    follow_depth: int,
    allow_buckets: set[str] | None,
    max_linked: int,
    env_file: str | None,
) -> int:
    if env_file:
        load_env_file_if_present(env_file)

    access_token = (os.environ.get("BC_ACCESS_TOKEN") or "").strip()
    user_agent = (os.environ.get("BC_USER_AGENT") or "").strip()
    if not access_token or not user_agent:
        print("❌ Missing BC_ACCESS_TOKEN / BC_USER_AGENT. Load Basecamp OAuth env first.", file=sys.stderr)
        return 2

    raw_root = out_dir / "01-basecamp-raw"
    norm_dir = out_dir / "02-basecamp-normalized"
    digest_dir = out_dir / "03-basecamp-digest"
    ensure_dir(raw_root)
    ensure_dir(norm_dir)
    ensure_dir(digest_dir)

    queue: list[tuple[str, int]] = [(app_url, 0)]
    visited: set[str] = set()
    linked_seen = 0

    sources: list[dict[str, Any]] = []
    lists_out: list[dict[str, Any]] = []
    todos_out: list[dict[str, Any]] = []
    cross_links: list[dict[str, Any]] = []

    while queue:
        current, depth = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        account, bucket, todolist_id = parse_app_todolist_url(current)
        if allow_buckets is not None and bucket not in allow_buckets:
            continue
        api_base = f"https://3.basecampapi.com/{account}/buckets/{bucket}"

        root_dir = raw_root / f"root_{bucket}_{todolist_id}"
        ensure_dir(root_dir)

        todolist = fetch_single(
            url=f"{api_base}/todolists/{todolist_id}.json",
            access_token=access_token,
            user_agent=user_agent,
            raw_dir=root_dir,
            filename="todolist",
        )
        if not isinstance(todolist, dict):
            print(f"❌ Failed to fetch todolist: {current}", file=sys.stderr)
            continue

        sources.append(
            {
                "account": int(account),
                "bucket": int(bucket),
                "todolist_id": int(todolist_id),
                "name": (todolist.get("name") or todolist.get("title") or "").strip(),
                "app_url": todolist.get("app_url") or current,
                "description_html": todolist.get("description") or "",
            }
        )

        # root todos (often empty for "hub" lists)
        root_todos = fetch_paged_array(
            first_url=f"{api_base}/todolists/{todolist_id}/todos.json",
            access_token=access_token,
            user_agent=user_agent,
            raw_dir=root_dir,
            basename="todos",
        )
        lists_out.append(normalize_todolist(todolist, parent_root_id=int(todolist_id)))
        for t in root_todos:
            todos_out.append(normalize_todo(t, list_id=int(todolist_id)))

        # groups -> child todolists
        groups = fetch_single(
            url=f"{api_base}/todolists/{todolist_id}/groups.json",
            access_token=access_token,
            user_agent=user_agent,
            raw_dir=root_dir,
            filename="groups",
        )
        if isinstance(groups, list):
            for child in groups:
                if not isinstance(child, dict) or child.get("id") is None:
                    continue
                cid = int(child.get("id"))
                child_dir = raw_root / f"list_{bucket}_{cid}"
                ensure_dir(child_dir)
                child_list = fetch_single(
                    url=f"{api_base}/todolists/{cid}.json",
                    access_token=access_token,
                    user_agent=user_agent,
                    raw_dir=child_dir,
                    filename="todolist",
                )
                if isinstance(child_list, dict):
                    lists_out.append(normalize_todolist(child_list, parent_root_id=int(todolist_id)))
                child_todos = fetch_paged_array(
                    first_url=f"{api_base}/todolists/{cid}/todos.json",
                    access_token=access_token,
                    user_agent=user_agent,
                    raw_dir=child_dir,
                    basename="todos",
                )
                for t in child_todos:
                    todos_out.append(normalize_todo(t, list_id=cid))

        # follow linked todolists referenced in description
        linked = extract_linked_todolists(todolist.get("description") or "")
        for link in linked:
            cross_links.append({"from": current, "to": link})
            if not follow_linked:
                continue
            if depth >= follow_depth:
                continue
            if linked_seen >= max_linked:
                continue
            # Only follow within same account for safety.
            try:
                acc2, bucket2, _ = parse_app_todolist_url(link)
            except ValueError:
                continue
            if acc2 != account:
                continue
            if allow_buckets is not None and bucket2 not in allow_buckets:
                continue
            if link not in visited and all(link != u for u, _d in queue):
                queue.append((link, depth + 1))
                linked_seen += 1

    # de-dup lists/todos by id
    lists_by_id: dict[int, dict[str, Any]] = {}
    for li in lists_out:
        lid = li.get("id")
        if isinstance(lid, int):
            lists_by_id[lid] = li
    todos_by_id: dict[int, dict[str, Any]] = {}
    for td in todos_out:
        tid = td.get("id")
        if isinstance(tid, int):
            todos_by_id[tid] = td

    context = {
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "seed_hint": "UGC ads",
        "sources": sources,
        "lists": list(lists_by_id.values()),
        "todos": list(todos_by_id.values()),
        "cross_links": cross_links,
    }
    write_json(norm_dir / "context.json", context)
    write_text(digest_dir / "context.md", render_digest(context))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Download a Basecamp todolist and build a local context pack.")
    parser.add_argument("--app-url", required=True, help="Basecamp App todolist URL (https://3.basecamp.com/.../todolists/<id>)")
    parser.add_argument("--out", required=True, help="Output directory for the context pack")
    parser.add_argument(
        "--env-file",
        default="skills/utilities/basecamp-link-ops/.env.basecamp",
        help="Env file to load (default: basecamp-link-ops .env.basecamp)",
    )
    parser.add_argument("--follow-linked-todolists", action="store_true", help="Follow todolist links found in description HTML")
    parser.add_argument(
        "--follow-linked-depth",
        type=int,
        default=1,
        help="How deep to follow linked todolists (default: 1, only the initial list's links)",
    )
    parser.add_argument(
        "--allow-bucket",
        action="append",
        default=None,
        help="Restrict fetching to these bucket IDs (repeatable). If omitted, fetch any bucket in-scope.",
    )
    parser.add_argument("--max-linked", type=int, default=5, help="Max linked todolists to follow (default: 5)")
    args = parser.parse_args(argv)

    out_dir = Path(args.out).expanduser().resolve()
    allow_buckets = None
    if args.allow_bucket:
        allow_buckets = {str(x).strip() for x in args.allow_bucket if str(x).strip()}
    return build_context_pack(
        app_url=args.app_url,
        out_dir=out_dir,
        follow_linked=bool(args.follow_linked_todolists),
        follow_depth=int(args.follow_linked_depth),
        allow_buckets=allow_buckets,
        max_linked=int(args.max_linked),
        env_file=str(args.env_file) if args.env_file else None,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
