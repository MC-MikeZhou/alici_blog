#!/usr/bin/env python3
"""
Standalone Tutorial Validator (Blog Tutorial Writer v3.0)

Validates a v3.0 tutorial bundle outside the AliciBlog repo.

Required inputs in --dir:
  - 01-article-draft.md
  - 01-article-draft.json

Outputs:
  - 04-tutorial-validator-report.json (written into --dir)

Exit code:
  0 = PASS
  1 = FAIL
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


ALLOWED_CITABLE_TYPES = {
    "definition",
    "statistic",
    "comparison",
    "recommendation",
    "methodology",
    "case_study",
    "key_takeaway",
}

TIER_RANGES = {
    1: (1800, 2200),
    2: (2200, 2800),
    3: (2800, 3500),
}


@dataclass
class Finding:
    code: str
    message: str
    details: Dict[str, Any]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def strip_frontmatter(md: str) -> str:
    if not md.startswith("---"):
        return md
    parts = md.split("---", 2)
    if len(parts) < 3:
        return md
    return parts[2].lstrip("\n")


def iter_lines_outside_code_fences(lines: Sequence[str]) -> Sequence[Tuple[int, str]]:
    in_code = False
    out: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append((idx, line))
            continue
        if not in_code:
            out.append((idx, line))
    return out


def normalize_heading(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()


def count_words(text: str) -> int:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def extract_h2_titles(md: str) -> List[str]:
    lines = md.splitlines()
    visible = iter_lines_outside_code_fences(lines)
    titles: List[str] = []
    for _, line in visible:
        if line.startswith("## "):
            titles.append(line[3:].strip())
    return titles


def find_tables(lines: Sequence[str]) -> List[Dict[str, Any]]:
    tables: List[Dict[str, Any]] = []
    for i in range(len(lines) - 1):
        header = lines[i].strip()
        sep = lines[i + 1].strip()
        if not (header.startswith("|") and header.endswith("|")):
            continue
        if not re.match(r"^\|\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|$", sep):
            continue
        cols = [c.strip() for c in header.strip("|").split("|")]
        tables.append({"start": i + 1, "columns": cols})
    return tables


def require_table_with_columns(
    errors: List[Finding],
    section_title: str,
    section_lines: Sequence[str],
    expected_columns: List[str],
    code: str,
) -> None:
    tables = find_tables(section_lines)
    if not tables:
        errors.append(
            Finding(
                code=code,
                message=f"Missing required table in section: {section_title}",
                details={"section": section_title, "expected_columns": expected_columns},
            )
        )
        return

    def _norm(cols: List[str]) -> List[str]:
        return [c.replace("’", "'").strip() for c in cols]

    first = _norm(tables[0]["columns"])
    expected = _norm(expected_columns)
    if first != expected:
        errors.append(
            Finding(
                code=code,
                message=f"Table columns mismatch in section: {section_title}",
                details={"section": section_title, "expected": expected_columns, "actual": tables[0]["columns"]},
            )
        )


def extract_h2_sections(md: str) -> List[Dict[str, Any]]:
    lines = md.splitlines()
    visible = iter_lines_outside_code_fences(lines)

    h2_indices: List[Tuple[int, str]] = []
    for line_no, line in visible:
        if line.startswith("## "):
            h2_indices.append((line_no, line[3:].strip()))

    if not h2_indices:
        return []

    line_to_idx = {i + 1: i for i in range(len(lines))}
    sections: List[Dict[str, Any]] = []
    for i, (start_line, title) in enumerate(h2_indices):
        start_idx = line_to_idx[start_line] + 1
        end_line = h2_indices[i + 1][0] - 1 if i + 1 < len(h2_indices) else len(lines)
        end_idx = line_to_idx.get(end_line, len(lines) - 1) + 1
        content_lines = lines[start_idx:end_idx]
        sections.append(
            {
                "title": title,
                "start_line": start_line,
                "end_line": end_line,
                "content_lines": content_lines,
                "content": "\n".join(content_lines).strip("\n"),
            }
        )
    return sections


def parse_block_metadata(block_text: str) -> Dict[str, str]:
    """
    Parse YAML-ish lines like: key: "value" or key: value
    """
    meta: Dict[str, str] = {}
    for line in block_text.splitlines():
        line = line.strip()
        if not line or line.startswith("<!--") or line.startswith("-->"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        meta[key] = value
    return meta


def extract_comment_blocks(md: str, opener: str) -> List[str]:
    """
    Extract HTML comment blocks that start with `<!-- {opener}` and end at the next `-->`.
    """
    blocks: List[str] = []
    pattern = re.compile(r"<!--\s*" + re.escape(opener) + r"(.*?)-->", re.DOTALL)
    for m in pattern.finditer(md):
        blocks.append(m.group(0))
    return blocks


def extract_citable_blocks(md: str) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    open_re = re.compile(
        r'<!--\s*CITABLE_BLOCK\s+type="(?P<type>[^"]+)"\s+id="(?P<id>[^"]+)"\s*-->\s*',
        re.IGNORECASE,
    )
    close_re = re.compile(r"<!--\s*/CITABLE_BLOCK\s*-->", re.IGNORECASE)

    idx = 0
    while True:
        m = open_re.search(md, idx)
        if not m:
            break
        start = m.end()
        m_close = close_re.search(md, start)
        if not m_close:
            blocks.append(
                {
                    "type": m.group("type"),
                    "id": m.group("id"),
                    "content": None,
                    "closed": False,
                }
            )
            idx = start
            continue
        content = md[start : m_close.start()].strip()
        blocks.append(
            {
                "type": m.group("type"),
                "id": m.group("id"),
                "content": content,
                "closed": True,
            }
        )
        idx = m_close.end()
    return blocks


def extract_self_test_placeholder(md: str) -> bool:
    return bool(re.search(r"<!--\s*SELF_TEST_PLACEHOLDER\b", md))


def validate_required_h2_order(
    errors: List[Finding],
    md: str,
    expect_market: bool,
    expect_prereq: bool,
    expect_workflow: bool,
    expect_monetization: bool,
) -> None:
    titles = [normalize_heading(t) for t in extract_h2_titles(md)]
    required: List[str] = ["background"]

    if expect_market:
        required.append("market context: why {topic} is exploding right now")
    if expect_prereq:
        required.append("prerequisites check")
    if expect_workflow:
        required.append("choose your path: {n} workflows compared")

    # Steps are checked separately (pattern)
    required.extend(
        [
            "troubleshooting: quick fixes for common issues",
            "conclusion",
            "faq",
        ]
    )
    if expect_monetization:
        # Monetization sits before Conclusion (blueprint), but we allow it anywhere before conclusion
        required.insert(required.index("conclusion"), "monetization framework: how to make money with {topic}")

    # We validate relative ordering by locating each required anchor (fuzzy prefix match).
    def _find_idx(anchor: str) -> Optional[int]:
        if "{topic}" in anchor or "{n}" in anchor:
            anchor_prefix = anchor.split("{", 1)[0].strip()
            for i, t in enumerate(titles):
                if t.startswith(anchor_prefix):
                    return i
            return None
        for i, t in enumerate(titles):
            if t == anchor:
                return i
        return None

    last = -1
    for anchor in required:
        idx = _find_idx(anchor)
        if idx is None:
            errors.append(
                Finding(
                    code="E_H2_MISSING",
                    message=f"Missing required H2 section: {anchor}",
                    details={"anchor": anchor},
                )
            )
            continue
        if idx <= last:
            errors.append(
                Finding(
                    code="E_H2_ORDER",
                    message=f"H2 section order violation at: {anchor}",
                    details={"anchor": anchor, "index": idx, "previous_index": last},
                )
            )
        last = max(last, idx)


def validate_steps(errors: List[Finding], md: str) -> None:
    titles = extract_h2_titles(md)
    step_titles = [t for t in titles if re.match(r"^Step\s+\d+:", t)]
    if len(step_titles) < 5:
        errors.append(
            Finding(
                code="E_STEPS_COUNT",
                message="Expected at least 5 step sections (H2 headings like '## Step 1: ...')",
                details={"found": len(step_titles), "examples": step_titles[:3]},
            )
        )
        return
    # Ensure numbering starts at 1 and is contiguous for the first N found.
    nums = []
    for t in step_titles:
        m = re.match(r"^Step\s+(\d+):", t)
        if m:
            nums.append(int(m.group(1)))
    if not nums or min(nums) != 1:
        errors.append(
            Finding(
                code="E_STEPS_NUMBERING",
                message="Step numbering must start at 1",
                details={"numbers": nums[:10]},
            )
        )
        return
    # Contiguous check (best-effort)
    sorted_nums = sorted(set(nums))
    expected = list(range(1, sorted_nums[0] + len(sorted_nums)))
    if sorted_nums != expected:
        errors.append(
            Finding(
                code="E_STEPS_NUMBERING",
                message="Step numbering should be contiguous (no gaps)",
                details={"numbers": sorted_nums},
            )
        )


def validate_citable_blocks(errors: List[Finding], warnings: List[Finding], md: str) -> Dict[str, Any]:
    blocks = extract_citable_blocks(md)
    if any(not b["closed"] for b in blocks):
        warnings.append(
            Finding(
                code="W_CITABLE_UNCLOSED",
                message="One or more CITABLE_BLOCK markers are missing a closing tag",
                details={"count": sum(1 for b in blocks if not b["closed"])},
            )
        )
    valid = [b for b in blocks if b["closed"]]
    if len(valid) < 5:
        errors.append(
            Finding(
                code="E_CITABLE_COUNT",
                message="Expected at least 5 closed CITABLE_BLOCK blocks",
                details={"found": len(valid)},
            )
        )
    types = [str(b["type"]).strip() for b in valid]
    unique_types = sorted({t for t in types})
    bad_types = sorted({t for t in unique_types if t not in ALLOWED_CITABLE_TYPES})
    if bad_types:
        errors.append(
            Finding(
                code="E_CITABLE_TYPE",
                message="Found invalid CITABLE_BLOCK types",
                details={"invalid": bad_types, "allowed": sorted(ALLOWED_CITABLE_TYPES)},
            )
        )
    if len({t for t in unique_types if t in ALLOWED_CITABLE_TYPES}) < 3:
        errors.append(
            Finding(
                code="E_CITABLE_DIVERSITY",
                message="Expected at least 3 distinct valid CITABLE_BLOCK types",
                details={"types": unique_types},
            )
        )
    return {"count": len(valid), "types": unique_types}


def validate_image_placeholders(errors: List[Finding], md: str) -> List[Dict[str, Any]]:
    blocks = extract_comment_blocks(md, "IMAGE_PLACEHOLDER")
    images: List[Dict[str, Any]] = []
    required = ["id", "type", "priority", "alt", "where"]
    for raw in blocks:
        meta = parse_block_metadata(raw)
        images.append(meta)
        missing = [k for k in required if not meta.get(k)]
        if missing:
            errors.append(
                Finding(
                    code="E_IMAGE_PLACEHOLDER_FIELDS",
                    message="IMAGE_PLACEHOLDER missing required fields",
                    details={"missing": missing, "block": raw[:200]},
                )
            )
    return images


def validate_cta_cards(errors: List[Finding], md: str) -> List[Dict[str, Any]]:
    blocks = extract_comment_blocks(md, "CTA_CARD")
    ctas: List[Dict[str, Any]] = []
    required = ["position", "trigger", "friction_context", "product", "cta_type"]
    for raw in blocks:
        meta = parse_block_metadata(raw)
        ctas.append(meta)
        missing = [k for k in required if not meta.get(k)]
        if missing:
            errors.append(
                Finding(
                    code="E_CTA_CARD_FIELDS",
                    message="CTA_CARD missing required fields",
                    details={"missing": missing, "block": raw[:200]},
                )
            )
    if len(ctas) < 2:
        errors.append(
            Finding(
                code="E_CTA_CARD_COUNT",
                message="Expected at least 2 CTA_CARD blocks (mid + closing)",
                details={"found": len(ctas)},
            )
        )
    return ctas


def section_lines_by_exact_h2(md: str, expected_title: str) -> Optional[List[str]]:
    sections = extract_h2_sections(md)
    for sec in sections:
        if normalize_heading(sec["title"]) == normalize_heading(expected_title):
            return list(sec["content_lines"])
    return None


def section_lines_by_prefix(md: str, prefix: str) -> Optional[List[str]]:
    sections = extract_h2_sections(md)
    prefix_norm = normalize_heading(prefix)
    for sec in sections:
        if normalize_heading(sec["title"]).startswith(prefix_norm):
            return list(sec["content_lines"])
    return None


def require_troubleshooting_table(errors: List[Finding], md: str) -> None:
    title_prefix = "Troubleshooting: Quick Fixes for Common Issues"
    lines = section_lines_by_prefix(md, title_prefix)
    if lines is None:
        errors.append(
            Finding(
                code="E_TROUBLESHOOTING_MISSING",
                message="Missing troubleshooting section",
                details={"expected_prefix": title_prefix},
            )
        )
        return
    require_table_with_columns(
        errors=errors,
        section_title=title_prefix,
        section_lines=lines,
        expected_columns=["Symptom", "Likely Cause", "Fix"],
        code="E_TROUBLESHOOTING_TABLE",
    )
    # Validate at least 5 data rows (best-effort): count pipes lines excluding header+sep
    pipe_lines = [ln for ln in lines if ln.strip().startswith("|") and ln.strip().endswith("|")]
    if len(pipe_lines) >= 2:
        data_rows = max(0, len(pipe_lines) - 2)
        if data_rows < 5:
            errors.append(
                Finding(
                    code="E_TROUBLESHOOTING_ROWS",
                    message="Troubleshooting table must have at least 5 issue rows",
                    details={"rows": data_rows},
                )
            )


def require_prerequisites_table(errors: List[Finding], md: str, required: bool) -> None:
    title = "Prerequisites Check"
    lines = section_lines_by_exact_h2(md, title)
    if not required:
        if lines is not None:
            errors.append(
                Finding(
                    code="E_PREREQ_UNEXPECTED",
                    message="Prerequisites Check section present but not expected",
                    details={"section": title},
                )
            )
        return
    if lines is None:
        errors.append(
            Finding(
                code="E_PREREQ_MISSING",
                message="Missing Prerequisites Check section (Tier 2/3 requirement)",
                details={"section": title},
            )
        )
        return
    require_table_with_columns(
        errors=errors,
        section_title=title,
        section_lines=lines,
        expected_columns=["Item", "Required?", "Why", "Alternatives"],
        code="E_PREREQ_TABLE",
    )


def require_workflow_selector_table(errors: List[Finding], md: str, required: bool) -> None:
    title_prefix = "Choose Your Path:"
    lines = section_lines_by_prefix(md, title_prefix)
    if not required:
        if lines is not None:
            errors.append(
                Finding(
                    code="E_WORKFLOW_UNEXPECTED",
                    message="Workflow Selector section present but not expected",
                    details={"expected_prefix": title_prefix},
                )
            )
        return
    if lines is None:
        errors.append(
            Finding(
                code="E_WORKFLOW_MISSING",
                message="Missing workflow selector section (multi-path requirement)",
                details={"expected_prefix": title_prefix},
            )
        )
        return
    require_table_with_columns(
        errors=errors,
        section_title=title_prefix,
        section_lines=lines,
        expected_columns=["Goal", "Workflow", "Time", "Difficulty", "Jump To"],
        code="E_WORKFLOW_TABLE",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directory containing 01-article-draft.md and 01-article-draft.json")
    args = parser.parse_args()

    out_dir = Path(args.dir).expanduser().resolve()
    md_path = out_dir / "01-article-draft.md"
    json_path = out_dir / "01-article-draft.json"
    report_path = out_dir / "04-tutorial-validator-report.json"

    errors: List[Finding] = []
    warnings: List[Finding] = []

    if not md_path.exists():
        errors.append(Finding(code="E_MISSING_MD", message="Missing 01-article-draft.md", details={"path": str(md_path)}))
    if not json_path.exists():
        errors.append(
            Finding(code="E_MISSING_JSON", message="Missing 01-article-draft.json", details={"path": str(json_path)})
        )

    md = ""
    payload: Dict[str, Any] = {}
    if not errors:
        md = strip_frontmatter(_read_text(md_path))
        payload = _load_json(json_path)

    # JSON meta checks
    tier = None
    experience_evidence = None
    sections = {}
    if payload:
        try:
            meta = payload["meta"]
            tier = int(meta["tier"])
        except Exception:
            errors.append(
                Finding(code="E_JSON_META", message="Invalid or missing meta.tier in 01-article-draft.json", details={})
            )
        try:
            experience_evidence = str(payload["aeo_pre_check"]["experience_evidence"])
        except Exception:
            errors.append(
                Finding(
                    code="E_JSON_AEO",
                    message="Invalid or missing aeo_pre_check.experience_evidence in 01-article-draft.json",
                    details={},
                )
            )
        try:
            sections = dict(payload.get("sections", {}))
        except Exception:
            sections = {}

    # Tier + word count checks
    md_word_count = count_words(md) if md else 0
    if tier in TIER_RANGES:
        lo, hi = TIER_RANGES[tier]
        if not (lo <= md_word_count <= hi):
            errors.append(
                Finding(
                    code="E_WORD_COUNT_TIER",
                    message="Word count not within tier range",
                    details={"tier": tier, "word_count": md_word_count, "expected_range": [lo, hi]},
                )
            )
    elif tier is not None:
        errors.append(
            Finding(code="E_TIER_VALUE", message="Invalid tier value (expected 1/2/3)", details={"tier": tier})
        )

    # Section expectations
    expect_market = bool(sections.get("market_context"))
    expect_prereq = bool(sections.get("prerequisites")) or (tier in (2, 3))
    expect_workflow = bool(sections.get("workflow_selector"))
    expect_monetization = bool(sections.get("monetization_framework"))

    if md:
        validate_required_h2_order(
            errors=errors,
            md=md,
            expect_market=expect_market,
            expect_prereq=expect_prereq,
            expect_workflow=expect_workflow,
            expect_monetization=expect_monetization,
        )
        validate_steps(errors=errors, md=md)

        require_prerequisites_table(errors=errors, md=md, required=expect_prereq)
        require_workflow_selector_table(errors=errors, md=md, required=expect_workflow)
        require_troubleshooting_table(errors=errors, md=md)

        citable_summary = validate_citable_blocks(errors=errors, warnings=warnings, md=md)

        images = validate_image_placeholders(errors=errors, md=md)
        ctas = validate_cta_cards(errors=errors, md=md)

        # Experience evidence enforcement
        has_self_test = extract_self_test_placeholder(md)
        if experience_evidence != "full" and not has_self_test:
            errors.append(
                Finding(
                    code="E_SELF_TEST_REQUIRED",
                    message="Missing SELF_TEST_PLACEHOLDER (required when experiment_pack is not provided)",
                    details={"experience_evidence": experience_evidence},
                )
            )

        # JSON <-> MD consistency (best-effort)
        json_images = payload.get("images", []) if isinstance(payload, dict) else []
        json_ctas = payload.get("ctas", []) if isinstance(payload, dict) else []
        if isinstance(json_images, list) and len(json_images) != len(images):
            errors.append(
                Finding(
                    code="E_JSON_IMAGES_COUNT",
                    message="images[] count in JSON must match IMAGE_PLACEHOLDER blocks in MD",
                    details={"json": len(json_images), "md": len(images)},
                )
            )
        if isinstance(json_ctas, list) and len(json_ctas) != len(ctas):
            errors.append(
                Finding(
                    code="E_JSON_CTAS_COUNT",
                    message="ctas[] count in JSON must match CTA_CARD blocks in MD",
                    details={"json": len(json_ctas), "md": len(ctas)},
                )
            )

        # JSON citable pre-check consistency
        try:
            json_citable_count = int(payload["aeo_pre_check"]["citable_blocks"])
            if json_citable_count != int(citable_summary["count"]):
                errors.append(
                    Finding(
                        code="E_JSON_CITABLE_COUNT",
                        message="aeo_pre_check.citable_blocks must match CITABLE_BLOCK blocks in MD",
                        details={"json": json_citable_count, "md": citable_summary["count"]},
                    )
                )
        except Exception:
            pass

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "profile": "tutorial_v3",
        "errors": [e.__dict__ for e in errors],
        "warnings": [w.__dict__ for w in warnings],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

