#!/usr/bin/env python3
"""
Listicle Validator (Blog List Writer v3.0)

Validates structure-first requirements for `content_type=list` listicles:
- Fixed H2 order by profile (standard/prompt_workflow/mega/alternatives)
- Required tables with exact column headers
- CTA markers in the right sections
- Quick Answer word-count window
- Tool Card required fields and minimum bullet counts
- Freshness statement: "Verified as of YYYY-MM-DD" (must match plan freshness_date)
- Plan Pack + Assets queue exist and meet minimum schema

Evidence rules:
- Official site + pricing URL per tool are FAIL if missing
- Third-party evidence for top5 is WARNING (non-blocking)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def extract_h2_sections(md: str) -> List[Dict[str, Any]]:
    lines = md.splitlines()
    visible = iter_lines_outside_code_fences(lines)

    h2_indices: List[Tuple[int, str]] = []
    for line_no, line in visible:
        if line.startswith("## "):
            h2_indices.append((line_no, line[3:].strip()))

    # Build sections by original line indices.
    sections: List[Dict[str, Any]] = []
    if not h2_indices:
        return sections

    # Map line_no -> index in lines (0-based)
    line_to_idx = {i + 1: i for i in range(len(lines))}

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


def extract_h3_sections_within(lines: Sequence[str]) -> List[Dict[str, Any]]:
    # Input is already a section's content_lines (no H2 headings).
    visible = iter_lines_outside_code_fences(lines)
    h3_indices: List[Tuple[int, str]] = []
    for rel_line_no, line in visible:
        if line.startswith("### "):
            h3_indices.append((rel_line_no, line[4:].strip()))
    if not h3_indices:
        return []

    sections: List[Dict[str, Any]] = []
    for i, (start_rel, title) in enumerate(h3_indices):
        start_idx = start_rel  # content_lines is 0-based after this line
        # Convert rel_line_no (1-based) to index in lines
        start_content_idx = start_rel  # slice starts after heading => start_rel (1-based) is correct for next line index
        end_rel = h3_indices[i + 1][0] - 1 if i + 1 < len(h3_indices) else len(lines)
        end_content_idx = end_rel
        content_lines = list(lines[start_content_idx:end_content_idx])
        sections.append(
            {
                "title": title,
                "start_rel_line": start_rel,
                "end_rel_line": end_rel,
                "content_lines": content_lines,
                "content": "\n".join(content_lines).strip("\n"),
            }
        )
    return sections


def normalize_heading(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()


def count_words(text: str) -> int:
    # English-focused word count; good enough for Quick Answer windows.
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def count_sentences(text: str) -> int:
    # Heuristic: ignore bullets; count sentence-ending punctuation; fallback to paragraph count.
    lines = [ln.strip() for ln in text.splitlines()]
    non_bullet = [ln for ln in lines if ln and not ln.startswith(("-", "*"))]
    cleaned = " ".join(non_bullet)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return 0
    # Split on punctuation boundaries.
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= 2:
        return len(parts)
    # Fallback: paragraph-ish count.
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return max(1, len(paras))


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
    def _norm_cols(cols: List[str]) -> List[str]:
        return [c.replace("’", "'").strip() for c in cols]

    first = _norm_cols(tables[0]["columns"])
    expected_norm = _norm_cols(expected_columns)
    if first != expected_norm:
        errors.append(
            Finding(
                code=code,
                message=f"Table columns mismatch in section: {section_title}",
                details={"section": section_title, "expected": expected_columns, "actual": tables[0]["columns"]},
            )
        )


def find_cta_blocks(section_text: str) -> Dict[str, int]:
    # Counts by CTA id (1/2/3...) based on markers.
    counts: Dict[str, int] = {}
    for m in re.finditer(r"<!--\s*CTA:(\d+)\s*-->", section_text):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    for m in re.finditer(r"<!--\s*/CTA\s*-->", section_text):
        counts["_close"] = counts.get("_close", 0) + 1
    return counts


def validate_cta_in_section(
    errors: List[Finding],
    section_title: str,
    section_text: str,
    cta_id: str,
    required: bool,
    code: str,
) -> None:
    counts = find_cta_blocks(section_text)
    open_count = counts.get(cta_id, 0)
    close_count = counts.get("_close", 0)
    if required and open_count != 1:
        errors.append(
            Finding(
                code=code,
                message=f"CTA:{cta_id} marker missing or duplicated in section: {section_title}",
                details={"section": section_title, "cta_id": cta_id, "open_count": open_count},
            )
        )
    if required and close_count < 1:
        errors.append(
            Finding(
                code=code,
                message=f"CTA block missing closing marker in section: {section_title}",
                details={"section": section_title, "cta_id": cta_id, "close_count": close_count},
            )
        )


def validate_tool_card(
    errors: List[Finding],
    title: str,
    body_lines: Sequence[str],
    code_prefix: str,
) -> None:
    body = "\n".join(body_lines)
    required_labels = [
        "**Best for:**",
        "**Why it stands out:**",
        "**Key features:**",
        "**Pros:**",
        "**Cons:**",
        "**Pricing:**",
        "**Notes / limitations:**",
    ]
    last_pos = -1
    for label in required_labels:
        pos = body.find(label)
        if pos == -1:
            errors.append(
                Finding(
                    code=f"{code_prefix}_MISSING_FIELD",
                    message=f"Tool card missing required field: {label}",
                    details={"tool": title, "missing": label},
                )
            )
            continue
        if pos < last_pos:
            errors.append(
                Finding(
                    code=f"{code_prefix}_FIELD_ORDER",
                    message="Tool card fields are out of order",
                    details={"tool": title, "field": label},
                )
            )
        last_pos = pos

    def _count_bullets(after_label: str, until_labels: List[str]) -> int:
        start = body.find(after_label)
        if start == -1:
            return 0
        start += len(after_label)
        end = len(body)
        for ul in until_labels:
            p = body.find(ul, start)
            if p != -1:
                end = min(end, p)
        chunk = body[start:end]
        # Count bullet lines (support common markers).
        bullet_starts = ("-", "*", "•")
        return len([ln for ln in chunk.splitlines() if ln.strip().startswith(bullet_starts)])

    features = _count_bullets("**Key features:**", ["**Pros:**", "**Cons:**", "**Pricing:**", "**Notes / limitations:**"])
    pros = _count_bullets("**Pros:**", ["**Cons:**", "**Pricing:**", "**Notes / limitations:**"])
    cons = _count_bullets("**Cons:**", ["**Pricing:**", "**Notes / limitations:**"])
    if features < 3:
        errors.append(
            Finding(
                code=f"{code_prefix}_FEATURES_COUNT",
                message="Tool card must have at least 3 key feature bullets",
                details={"tool": title, "count": features},
            )
        )
    if pros < 3:
        errors.append(
            Finding(
                code=f"{code_prefix}_PROS_COUNT",
                message="Tool card must have at least 3 pros bullets",
                details={"tool": title, "count": pros},
            )
        )
    if cons < 2:
        errors.append(
            Finding(
                code=f"{code_prefix}_CONS_COUNT",
                message="Tool card must have at least 2 cons bullets",
                details={"tool": title, "count": cons},
            )
        )

    pricing_line = ""
    for ln in body_lines:
        if "**Pricing:**" in ln:
            pricing_line = ln.strip()
            break
    if pricing_line and "http" not in pricing_line:
        errors.append(
            Finding(
                code=f"{code_prefix}_PRICING_LINK",
                message="Pricing field must include an official pricing URL",
                details={"tool": title, "pricing_line": pricing_line},
            )
        )


def parse_faq_items(faq_lines: Sequence[str]) -> List[Tuple[str, str]]:
    """
    Supports:
    - H3 questions: ### ...?
    - Q marker lines: **Q:** ... or Q: ...
    Returns list of (question, answer_text)
    """
    items: List[Tuple[str, str]] = []
    cur_q: Optional[str] = None
    cur_ans: List[str] = []

    def flush() -> None:
        nonlocal cur_q, cur_ans
        if cur_q:
            items.append((cur_q.strip(), "\n".join(cur_ans).strip()))
        cur_q = None
        cur_ans = []

    in_code = False
    for ln in faq_lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = ln.strip()
        m_h3 = re.match(r"^###\s+(.*)$", s)
        m_q = re.match(r"^(?:\*\*Q:\*\*|Q:)\s*(.+)$", s, flags=re.IGNORECASE)
        if m_h3:
            q = m_h3.group(1).strip()
            if "?" in q or q.lower().startswith(("what", "which", "how", "can", "is ", "are ")):
                flush()
                cur_q = q
                continue
        if m_q:
            flush()
            cur_q = m_q.group(1).strip()
            continue
        if cur_q is not None:
            cur_ans.append(ln)
    flush()
    return items


def validate_methodology_level(
    errors: List[Finding],
    section_text: str,
    methodology_level: str,
) -> None:
    text = section_text.lower()
    if methodology_level == "research_only":
        disclosure_ok = bool(
            re.search(r"(did not|didn't)\s+(run|perform|conduct).{0,30}hands[- ]on", text)
            or re.search(r"no\s+hands[- ]on\s+tests", text)
            or re.search(r"based on public documentation", text)
        )
        if not disclosure_ok:
            errors.append(
                Finding(
                    code="METH_RESEARCH_ONLY_DISCLOSURE",
                    message="research_only methodology_level must disclose no hands-on testing in How We Picked & Tested",
                    details={},
                )
            )
        banned = [
            r"\bwe tested\b",
            r"\blab\b",
            r"\bsample size\b",
        ]
        for pat in banned:
            if re.search(pat, text):
                errors.append(
                    Finding(
                        code="METH_RESEARCH_ONLY_BANNED_CLAIM",
                        message="research_only methodology_level contains banned hands-on/testing claim",
                        details={"pattern": pat},
                    )
                )
    elif methodology_level == "hybrid":
        if not ("limited" in text and ("hands-on" in text or "hands on" in text) and "desk research" in text):
            errors.append(
                Finding(
                    code="METH_HYBRID_DISCLOSURE",
                    message="hybrid methodology_level must mention limited hands-on checks + desk research in How We Picked & Tested",
                    details={},
                )
            )
    elif methodology_level == "hands_on":
        required_terms = [
            ("test period", "Test Period"),
            ("sample size", "Sample Size"),
            ("scenarios", "Scenarios"),
        ]
        missing = [label for key, label in required_terms if key not in text]
        if missing:
            errors.append(
                Finding(
                    code="METH_HANDS_ON_MISSING_DETAILS",
                    message="hands_on methodology_level must include test period, sample size, and scenarios in How We Picked & Tested",
                    details={"missing": missing},
                )
            )
        # Dimension evidence (a table or explicit 'Dimension' mentions)
        if "dimension" not in text and "dimensions" not in text:
            errors.append(
                Finding(
                    code="METH_HANDS_ON_MISSING_DIMENSIONS",
                    message="hands_on methodology_level must include evaluation dimensions in How We Picked & Tested",
                    details={},
                )
            )


def infer_profile_from_plan(meta: Dict[str, Any]) -> str:
    profile = str(meta.get("listicle_profile") or "").strip()
    if profile:
        return profile
    size = meta.get("list_size_target")
    try:
        size_int = int(size)
    except Exception:
        size_int = 12
    keyword = str(meta.get("primary_keyword") or meta.get("target_keyword") or "").lower()
    if "alternative" in keyword:
        return "alternatives"
    if size_int >= 20:
        return "mega"
    if size_int >= 14:
        return "prompt_workflow"
    return "standard"


def validate_plan_pack(
    plan_path: Path, errors: List[Finding], warnings: List[Finding]
) -> Dict[str, Any]:
    if not plan_path.exists():
        errors.append(
            Finding(code="PLAN_MISSING", message="Missing required file: 02-plan.json", details={})
        )
        return {}
    try:
        plan = _load_json(plan_path)
    except Exception as e:
        errors.append(
            Finding(code="PLAN_INVALID_JSON", message="02-plan.json is not valid JSON", details={"error": str(e)})
        )
        return {}

    meta = plan.get("meta") or {}
    required_meta = ["version", "freshness_date", "methodology_level", "listicle_profile", "list_size_target"]
    missing_meta = [k for k in required_meta if k not in meta]
    if missing_meta:
        errors.append(
            Finding(
                code="PLAN_META_MISSING",
                message="02-plan.json.meta missing required fields",
                details={"missing": missing_meta},
            )
        )

    freshness_date = str(meta.get("freshness_date") or "")
    if freshness_date and not DATE_RE.match(freshness_date):
        errors.append(
            Finding(
                code="PLAN_FRESHNESS_DATE_FORMAT",
                message="freshness_date must be YYYY-MM-DD",
                details={"freshness_date": freshness_date},
            )
        )

    selected = plan.get("selected_tools")
    if not isinstance(selected, list) or not selected:
        errors.append(
            Finding(
                code="PLAN_SELECTED_TOOLS_MISSING",
                message="02-plan.json.selected_tools must be a non-empty list",
                details={},
            )
        )
        selected = []

    for tool in selected:
        name = str((tool or {}).get("name") or "").strip()
        if not name:
            errors.append(
                Finding(
                    code="PLAN_TOOL_NAME_MISSING",
                    message="Each selected tool must have a name",
                    details={"tool": tool},
                )
            )
            continue
        if not str(tool.get("official_site_url") or "").strip():
            errors.append(
                Finding(
                    code="PLAN_TOOL_OFFICIAL_URL_MISSING",
                    message="Each selected tool must include official_site_url",
                    details={"tool": name},
                )
            )
        if not str(tool.get("pricing_url") or "").strip():
            errors.append(
                Finding(
                    code="PLAN_TOOL_PRICING_URL_MISSING",
                    message="Each selected tool must include pricing_url",
                    details={"tool": name},
                )
            )

    # Top5 third-party evidence: warning only.
    for tool in selected[:5]:
        name = str((tool or {}).get("name") or "").strip() or "<unknown>"
        ev = (tool or {}).get("evidence") or {}
        third_party = ev.get("third_party") or []
        if not third_party:
            warnings.append(
                Finding(
                    code="EVIDENCE_TOP5_THIRD_PARTY_MISSING",
                    message="Top 5 tool missing third-party evidence (warning only)",
                    details={"tool": name},
                )
            )

    # tool count mismatch -> warning
    try:
        target_n = int(meta.get("list_size_target"))
    except Exception:
        target_n = None
    if target_n is not None and selected and len(selected) != target_n:
        warnings.append(
            Finding(
                code="PLAN_LIST_SIZE_MISMATCH",
                message="selected_tools count differs from list_size_target (warning only)",
                details={"list_size_target": target_n, "selected_tools_count": len(selected)},
            )
        )

    # Required keys existence (schema minimal)
    for key in ["tool_pool", "evaluation_framework", "aeo_pack", "cta_plan", "tables", "assumptions"]:
        if key not in plan:
            errors.append(
                Finding(
                    code="PLAN_SCHEMA_MISSING",
                    message="02-plan.json missing required top-level key",
                    details={"missing": key},
                )
            )

    return plan


def validate_assets_queue(
    assets_path: Path, errors: List[Finding]
) -> Dict[str, Any]:
    if not assets_path.exists():
        errors.append(
            Finding(code="ASSETS_MISSING", message="Missing required file: 03-assets.json", details={})
        )
        return {}
    try:
        assets = _load_json(assets_path)
    except Exception as e:
        errors.append(
            Finding(code="ASSETS_INVALID_JSON", message="03-assets.json is not valid JSON", details={"error": str(e)})
        )
        return {}

    meta = assets.get("meta") or {}
    if "recommended_generate_max" not in meta:
        errors.append(
            Finding(
                code="ASSETS_META_MISSING",
                message="03-assets.json.meta.recommended_generate_max is required",
                details={},
            )
        )
    featured = assets.get("featured_image")
    if not isinstance(featured, dict) or not featured.get("alt") or not featured.get("size") or not featured.get("priority"):
        errors.append(
            Finding(
                code="ASSETS_FEATURED_IMAGE_MISSING",
                message="03-assets.json.featured_image must include alt, size, priority",
                details={},
            )
        )
    diagrams = assets.get("diagrams") or []
    if not isinstance(diagrams, list) or len(diagrams) < 2:
        errors.append(
            Finding(
                code="ASSETS_DIAGRAMS_MIN",
                message="03-assets.json.diagrams must include at least 2 diagram requests",
                details={"count": len(diagrams) if isinstance(diagrams, list) else None},
            )
        )
    return assets


def validate_article(
    article_path: Path,
    plan: Dict[str, Any],
    profile: str,
    errors: List[Finding],
    warnings: List[Finding],
) -> None:
    md_raw = _read_text(article_path)
    md = strip_frontmatter(md_raw)
    h2_sections = extract_h2_sections(md)
    if not h2_sections:
        errors.append(
            Finding(code="ARTICLE_NO_H2", message="Article contains no H2 headings", details={})
        )
        return

    # Map normalized title -> section
    sections_by_norm = {normalize_heading(s["title"]): s for s in h2_sections}

    def get_section(title: str) -> Optional[Dict[str, Any]]:
        return sections_by_norm.get(normalize_heading(title))

    # Common required sections
    required = [
        "Quick Answer",
        "Key Takeaways",
        "Quick Comparison (Table)",
        "How We Picked & Tested",
        "Use Case Matching (Table)",
        "How to Choose",
        "FAQ + Final Verdict",
    ]

    if profile == "alternatives":
        required = [
            "Quick Answer",
            "Key Takeaways",
            "Ideal Solution Criteria",
            "Quick Comparison (Table)",
            "How We Picked & Tested",
            "Use Case Matching (Table)",
            "How to Choose",
            "FAQ + Final Verdict",
        ]
    if profile == "mega":
        required = [
            "Quick Answer",
            "Key Takeaways",
            "Quick Comparison (Table)",
            "How We Picked & Tested",
            "Category Winners",
            "Use Case Matching (Table)",
            "How to Choose",
            "FAQ + Final Verdict",
            "Update Strategy (Keeping This List Fresh)",
        ]
    if profile == "prompt_workflow":
        required = [
            "Quick Answer",
            "Key Takeaways",
            "Quick Comparison (Table)",
            "How We Picked & Tested",
            "Use Case Matching (Table)",
            "How to Prompt (Copy-Paste Templates)",
            "Free vs Paid Breakdown (Table)",
            "How to Choose",
            "FAQ + Final Verdict",
        ]

    for title in required:
        if not get_section(title):
            errors.append(
                Finding(
                    code="ARTICLE_SECTION_MISSING",
                    message="Missing required H2 section",
                    details={"missing": title},
                )
            )

    # Order checks: build H2 titles in order
    h2_titles = [s["title"] for s in h2_sections]
    h2_norm = [normalize_heading(t) for t in h2_titles]

    def idx_of(title: str) -> int:
        try:
            return h2_norm.index(normalize_heading(title))
        except ValueError:
            return -1

    # Profile-specific order enforcement (allow tool items / group headings in between where specified)
    if profile in ("standard", "prompt_workflow", "alternatives"):
        # Fixed anchors:
        anchors = [
            "Quick Answer",
            "Key Takeaways",
            "Quick Comparison (Table)",
            "How We Picked & Tested",
        ]
        if profile == "alternatives":
            anchors = [
                "Quick Answer",
                "Key Takeaways",
                "Ideal Solution Criteria",
                "Quick Comparison (Table)",
                "How We Picked & Tested",
            ]
        tail = [
            "Use Case Matching (Table)",
            "How to Choose",
            "FAQ + Final Verdict",
        ]
        if profile == "prompt_workflow":
            tail = [
                "Use Case Matching (Table)",
                "How to Prompt (Copy-Paste Templates)",
                "Free vs Paid Breakdown (Table)",
                "How to Choose",
                "FAQ + Final Verdict",
            ]

        # Anchors must be in order
        last = -1
        for t in anchors:
            i = idx_of(t)
            if i != -1 and i < last:
                errors.append(
                    Finding(
                        code="ARTICLE_H2_ORDER",
                        message="H2 sections out of order",
                        details={"section": t},
                    )
                )
            if i != -1:
                last = i
        last = -1
        for t in tail:
            i = idx_of(t)
            if i != -1 and i < last:
                errors.append(
                    Finding(
                        code="ARTICLE_H2_ORDER",
                        message="H2 sections out of order",
                        details={"section": t},
                    )
                )
            if i != -1:
                last = i

        # Tool items must be H2 between methodology and use-case sections.
        meth_i = idx_of("How We Picked & Tested")
        use_i = idx_of("Use Case Matching (Table)")
        if meth_i != -1 and use_i != -1 and use_i <= meth_i + 1:
            errors.append(
                Finding(
                    code="TOOL_ITEMS_MISSING",
                    message="Expected tool items between How We Picked & Tested and Use Case Matching (Table)",
                    details={},
                )
            )
        if meth_i != -1 and use_i != -1 and use_i > meth_i:
            between = h2_sections[meth_i + 1 : use_i]
            if not between:
                errors.append(
                    Finding(
                        code="TOOL_ITEMS_MISSING",
                        message="No tool H2 items found in expected region",
                        details={},
                    )
                )
            for sec in between:
                if not re.match(r"^\d+\.\s+", sec["title"]):
                    errors.append(
                        Finding(
                            code="TOOL_ITEM_HEADING_FORMAT",
                            message="Tool item H2 must start with '{rank}.'",
                            details={"heading": sec["title"]},
                        )
                    )

            # Ensure no unknown non-tool H2 exists outside fixed sections.
            fixed_norm = {normalize_heading(t) for t in required}
            for sec in h2_sections:
                t = sec["title"]
                if normalize_heading(t) in fixed_norm:
                    continue
                if re.match(r"^\d+\.\s+", t):
                    continue
                errors.append(
                    Finding(
                        code="ARTICLE_EXTRA_H2",
                        message="Unexpected H2 heading (not fixed section, not tool item)",
                        details={"heading": t},
                    )
                )

    if profile == "mega":
        # Fixed top order
        fixed_top = [
            "Quick Answer",
            "Key Takeaways",
            "Quick Comparison (Table)",
            "How We Picked & Tested",
            "Category Winners",
        ]
        last = -1
        for t in fixed_top:
            i = idx_of(t)
            if i != -1 and i < last:
                errors.append(
                    Finding(code="ARTICLE_H2_ORDER", message="H2 sections out of order", details={"section": t})
                )
            if i != -1:
                last = i

        winners_i = idx_of("Category Winners")
        use_i = idx_of("Use Case Matching (Table)")
        if winners_i != -1 and use_i != -1:
            groups = h2_sections[winners_i + 1 : use_i]
            if not groups:
                errors.append(
                    Finding(
                        code="MEGA_GROUPS_MISSING",
                        message="Mega profile requires at least one group H2 between Category Winners and Use Case Matching (Table)",
                        details={},
                    )
                )
            for g in groups:
                # Group section must contain H3 tool cards.
                h3s = extract_h3_sections_within(g["content_lines"])
                if not h3s:
                    errors.append(
                        Finding(
                            code="MEGA_GROUP_NO_H3",
                            message="Mega group must contain H3 tool cards",
                            details={"group": g["title"]},
                        )
                    )
                for h3 in h3s:
                    validate_tool_card(errors, h3["title"], h3["content_lines"], "TOOL_CARD")

    # Section-level checks
    qa = get_section("Quick Answer")
    if qa:
        qa_words = count_words(qa["content"])
        if qa_words < 120 or qa_words > 180:
            errors.append(
                Finding(
                    code="QUICK_ANSWER_WORD_COUNT",
                    message="Quick Answer must be 120–180 words",
                    details={"count": qa_words},
                )
            )
        validate_cta_in_section(errors, "Quick Answer", qa["content"], "1", True, "CTA1_MISSING")

    final = get_section("FAQ + Final Verdict")
    if final:
        # CTA2 is expected here for non-mega; mega uses CTA2 in Category Winners.
        if profile != "mega":
            validate_cta_in_section(errors, "FAQ + Final Verdict", final["content"], "2", True, "CTA2_MISSING")

        faq_items = parse_faq_items(final["content_lines"])
        if len(faq_items) < 6:
            errors.append(
                Finding(
                    code="FAQ_MIN_COUNT",
                    message="FAQ + Final Verdict must include at least 6 FAQ questions",
                    details={"count": len(faq_items)},
                )
            )
        for q, a in faq_items:
            s_count = count_sentences(a)
            if s_count < 2 or s_count > 4:
                errors.append(
                    Finding(
                        code="FAQ_ANSWER_SENTENCE_COUNT",
                        message="Each FAQ answer must be 2–4 sentences",
                        details={"question": q, "sentence_count": s_count},
                    )
                )

    # Tables + freshness in quick comparison
    qc = get_section("Quick Comparison (Table)")
    if qc:
        expected = ["Tool", "Best For", "Core Positioning", "Price", "Free Plan", "Limitations"]
        require_table_with_columns(errors, "Quick Comparison (Table)", qc["content_lines"], expected, "TABLE_QUICK_COMPARISON")
        freshness_date = str(((plan.get("meta") or {}).get("freshness_date") or "")).strip()
        m = re.search(r"Verified as of (\d{4}-\d{2}-\d{2})", qc["content"])
        if not m:
            errors.append(
                Finding(
                    code="FRESHNESS_STATEMENT_MISSING",
                    message="Quick Comparison section must include 'Verified as of YYYY-MM-DD'",
                    details={},
                )
            )
        elif freshness_date and m.group(1) != freshness_date:
            errors.append(
                Finding(
                    code="FRESHNESS_DATE_MISMATCH",
                    message="Freshness date in article must match 02-plan.json.meta.freshness_date",
                    details={"article": m.group(1), "plan": freshness_date},
                )
            )

    uc = get_section("Use Case Matching (Table)")
    if uc:
        expected = ["Use Case", "Recommended Tools", "Why", "Budget"]
        require_table_with_columns(errors, "Use Case Matching (Table)", uc["content_lines"], expected, "TABLE_USE_CASE")

    if profile == "prompt_workflow":
        fvp = get_section("Free vs Paid Breakdown (Table)")
        if fvp:
            expected = ["Tier", "What You Really Get", "Who It’s For", "Hidden Limits"]
            require_table_with_columns(errors, "Free vs Paid Breakdown (Table)", fvp["content_lines"], expected, "TABLE_FREE_VS_PAID")

    if profile == "alternatives":
        # Each tool section must contain at least one table (mini snapshot).
        meth_i = idx_of("How We Picked & Tested")
        use_i = idx_of("Use Case Matching (Table)")
        if meth_i != -1 and use_i != -1 and use_i > meth_i:
            for sec in h2_sections[meth_i + 1 : use_i]:
                if not find_tables(sec["content_lines"]):
                    errors.append(
                        Finding(
                            code="ALT_MINI_TABLE_MISSING",
                            message="Each alternative tool item must include at least one mini table",
                            details={"tool": sec["title"]},
                        )
                    )

    # Methodology level checks
    meth = get_section("How We Picked & Tested")
    if meth:
        methodology_level = str(((plan.get("meta") or {}).get("methodology_level") or "")).strip()
        validate_methodology_level(errors, meth["content"], methodology_level)

    # Tool cards in standard/prompt_workflow/alternatives
    if profile in ("standard", "prompt_workflow", "alternatives"):
        meth_i = idx_of("How We Picked & Tested")
        use_i = idx_of("Use Case Matching (Table)")
        if meth_i != -1 and use_i != -1 and use_i > meth_i:
            tool_secs = h2_sections[meth_i + 1 : use_i]
            for sec in tool_secs:
                validate_tool_card(errors, sec["title"], sec["content_lines"], "TOOL_CARD")

    # Mega: CTA2 in Category Winners
    if profile == "mega":
        winners = get_section("Category Winners")
        if winners:
            validate_cta_in_section(errors, "Category Winners", winners["content"], "2", True, "CTA2_MISSING_MEGA")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Article directory containing 01-article-draft.md, 02-plan.json, 03-assets.json")
    parser.add_argument("--profile", default="", help="Override profile: standard|prompt_workflow|mega|alternatives")
    args = parser.parse_args()

    base_dir = Path(args.dir).expanduser().resolve()
    errors: List[Finding] = []
    warnings: List[Finding] = []

    if not base_dir.exists() or not base_dir.is_dir():
        errors.append(Finding(code="DIR_INVALID", message="--dir must be an existing directory", details={"dir": str(base_dir)}))
        _write_report(base_dir, args.profile or "", errors, warnings, {})
        return 1

    article_path = base_dir / "01-article-draft.md"
    if not article_path.exists():
        alt = base_dir / "01-article.md"
        if alt.exists():
            article_path = alt
        else:
            errors.append(
                Finding(
                    code="ARTICLE_MISSING",
                    message="Missing required article file: 01-article-draft.md (or 01-article.md)",
                    details={},
                )
            )

    plan_path = base_dir / "02-plan.json"
    assets_path = base_dir / "03-assets.json"

    plan = validate_plan_pack(plan_path, errors, warnings)
    _ = validate_assets_queue(assets_path, errors)

    profile = (args.profile or "").strip()
    if not profile:
        meta = (plan.get("meta") or {}) if isinstance(plan, dict) else {}
        profile = infer_profile_from_plan(meta) if meta else "standard"
    if profile not in ("standard", "prompt_workflow", "mega", "alternatives"):
        errors.append(
            Finding(
                code="PROFILE_INVALID",
                message="Invalid profile; must be standard|prompt_workflow|mega|alternatives",
                details={"profile": profile},
            )
        )

    if article_path.exists() and isinstance(plan, dict) and plan:
        validate_article(article_path, plan, profile, errors, warnings)

    report = _write_report(base_dir, profile, errors, warnings, {"article": str(article_path)})
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def _write_report(
    base_dir: Path, profile: str, errors: List[Finding], warnings: List[Finding], files: Dict[str, Any]
) -> Dict[str, Any]:
    report = {
        "status": "PASS" if not errors else "FAIL",
        "profile": profile,
        "errors": [f.__dict__ for f in errors],
        "warnings": [f.__dict__ for f in warnings],
        "files": files,
    }
    try:
        out_path = base_dir / "04-listicle-validator-report.json"
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        # best-effort
        pass
    return report


if __name__ == "__main__":
    raise SystemExit(main())
