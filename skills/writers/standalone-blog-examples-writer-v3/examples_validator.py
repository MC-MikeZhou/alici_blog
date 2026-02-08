#!/usr/bin/env python3
"""
Standalone Examples Validator (Blog Examples & Ideas Writer v3.0)

Validates the 4-file output bundle:
  01-article-draft.md, 02-plan.json, 03-assets.json, 04-examples-validator-report.json

Usage:
  python3 examples_validator.py --dir /path/to/output_dir

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


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

VALID_PROFILES = ("showcase", "ideas_templates", "mega")

WORD_RANGES: Dict[str, Tuple[int, int]] = {
    "showcase": (3500, 7000),
    "ideas_templates": (3000, 5500),
    "mega": (6000, 10000),
}

VALID_FLEX_SLUGS = ("difficulty", "budget", "engagement", "effort", "industry")

# ---------------------------------------------------------------------------
# Shared utility functions (from listicle_validator.py)
# ---------------------------------------------------------------------------


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

    sections: List[Dict[str, Any]] = []
    if not h2_indices:
        return sections

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


def normalize_heading(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()


def count_words(text: str) -> int:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def count_sentences(text: str) -> int:
    lines = [ln.strip() for ln in text.splitlines()]
    non_bullet = [ln for ln in lines if ln and not ln.startswith(("-", "*"))]
    cleaned = " ".join(non_bullet)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return 0
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= 2:
        return len(parts)
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
        return [c.replace("\u2019", "'").strip() for c in cols]

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


def parse_faq_items(faq_lines: Sequence[str]) -> List[Tuple[str, str]]:
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


def extract_comment_blocks(md: str, tag: str) -> List[str]:
    """Extract HTML comment blocks matching <!-- {tag} ... -->"""
    pattern = rf"<!--\s*{re.escape(tag)}[\s\S]*?-->"
    return re.findall(pattern, md)


def parse_block_metadata(block: str) -> Dict[str, str]:
    """Parse key: value or key="value" pairs from an HTML comment block."""
    meta: Dict[str, str] = {}
    # key: "value" or key: value
    for m in re.finditer(r'(\w+)\s*[:=]\s*"([^"]*)"', block):
        meta[m.group(1)] = m.group(2)
    # key: value (unquoted)
    for m in re.finditer(r"(\w+)\s*:\s*([^\n\"]+)", block):
        key = m.group(1)
        if key not in meta:
            meta[key] = m.group(2).strip().strip('"')
    return meta


def extract_citable_blocks(md: str) -> List[Dict[str, str]]:
    """Extract CITABLE_BLOCK markers and return list of {type, id}."""
    blocks: List[Dict[str, str]] = []
    for m in re.finditer(r'<!--\s*CITABLE_BLOCK\s+type="([^"]+)"\s+id="([^"]+)"\s*-->', md):
        blocks.append({"type": m.group(1), "id": m.group(2)})
    return blocks


# ---------------------------------------------------------------------------
# Examples-specific validation
# ---------------------------------------------------------------------------


def validate_plan_pack(
    plan_path: Path, errors: List[Finding], warnings: List[Finding]
) -> Dict[str, Any]:
    if not plan_path.exists():
        errors.append(Finding(code="PLAN_MISSING", message="Missing required file: 02-plan.json", details={}))
        return {}
    try:
        plan = _load_json(plan_path)
    except Exception as e:
        errors.append(Finding(code="PLAN_INVALID_JSON", message="02-plan.json is not valid JSON", details={"error": str(e)}))
        return {}

    meta = plan.get("meta") or {}
    required_meta = ["version", "freshness_date", "examples_profile", "concept_count_target", "primary_keyword", "search_intent"]
    missing_meta = [k for k in required_meta if k not in meta]
    if missing_meta:
        errors.append(Finding(code="PLAN_META_MISSING", message="02-plan.json.meta missing required fields", details={"missing": missing_meta}))

    freshness_date = str(meta.get("freshness_date") or "")
    if freshness_date and not DATE_RE.match(freshness_date):
        errors.append(Finding(code="PLAN_FRESHNESS_DATE_FORMAT", message="freshness_date must be YYYY-MM-DD", details={"freshness_date": freshness_date}))

    profile = str(meta.get("examples_profile") or "").strip()
    if profile and profile not in VALID_PROFILES:
        errors.append(Finding(code="PLAN_PROFILE_INVALID", message=f"examples_profile must be one of {VALID_PROFILES}", details={"profile": profile}))

    selected = plan.get("selected_concepts")
    if not isinstance(selected, list) or not selected:
        errors.append(Finding(code="PLAN_SELECTED_CONCEPTS_MISSING", message="02-plan.json.selected_concepts must be a non-empty list", details={}))
        selected = []

    for concept in selected:
        name = str((concept or {}).get("name") or "").strip()
        if not name:
            errors.append(Finding(code="PLAN_CONCEPT_NAME_MISSING", message="Each selected concept must have a name", details={"concept": concept}))

    try:
        target_n = int(meta.get("concept_count_target"))
    except Exception:
        target_n = None
    if target_n is not None and selected and len(selected) != target_n:
        warnings.append(Finding(code="PLAN_CONCEPT_COUNT_MISMATCH", message="selected_concepts count differs from concept_count_target", details={"target": target_n, "actual": len(selected)}))

    for key in ["concept_pool", "categorization", "aeo_pack", "cta_plan", "tables", "assumptions"]:
        if key not in plan:
            errors.append(Finding(code="PLAN_SCHEMA_MISSING", message="02-plan.json missing required top-level key", details={"missing": key}))

    # Validate aeo_pack
    aeo = plan.get("aeo_pack") or {}
    qa = aeo.get("quick_answer") or ""
    if qa:
        qa_words = count_words(qa)
        if qa_words < 120 or qa_words > 180:
            warnings.append(Finding(code="PLAN_QA_WORD_COUNT", message="aeo_pack.quick_answer should be 120-180 words", details={"count": qa_words}))
    kt = aeo.get("key_takeaways") or []
    if len(kt) < 4:
        warnings.append(Finding(code="PLAN_KT_COUNT", message="aeo_pack.key_takeaways should have at least 4 items", details={"count": len(kt)}))
    faq = aeo.get("faq") or []
    if len(faq) < 6:
        errors.append(Finding(code="PLAN_FAQ_COUNT", message="aeo_pack.faq must have at least 6 questions", details={"count": len(faq)}))

    # Validate flex column for showcase
    if profile == "showcase":
        tables_obj = plan.get("tables") or {}
        flex = tables_obj.get("overview_flex_column") or {}
        slug = str(flex.get("slug") or "").strip()
        if slug and slug not in VALID_FLEX_SLUGS:
            errors.append(Finding(code="PLAN_FLEX_COLUMN_INVALID", message=f"overview_flex_column.slug must be one of {VALID_FLEX_SLUGS}", details={"slug": slug}))

    return plan


def validate_assets_queue(assets_path: Path, errors: List[Finding]) -> Dict[str, Any]:
    if not assets_path.exists():
        errors.append(Finding(code="ASSETS_MISSING", message="Missing required file: 03-assets.json", details={}))
        return {}
    try:
        assets = _load_json(assets_path)
    except Exception as e:
        errors.append(Finding(code="ASSETS_INVALID_JSON", message="03-assets.json is not valid JSON", details={"error": str(e)}))
        return {}

    meta = assets.get("meta") or {}
    if "recommended_generate_max" not in meta:
        errors.append(Finding(code="ASSETS_META_MISSING", message="03-assets.json.meta.recommended_generate_max is required", details={}))

    featured = assets.get("featured_image")
    if not isinstance(featured, dict) or not featured.get("id"):
        errors.append(Finding(code="ASSETS_FEATURED_IMAGE_MISSING", message="03-assets.json.featured_image must exist with an id", details={}))

    diagrams = assets.get("diagrams") or []
    if not isinstance(diagrams, list) or len(diagrams) < 1:
        errors.append(Finding(code="ASSETS_DIAGRAMS_MIN", message="03-assets.json.diagrams must include at least 1 diagram", details={"count": len(diagrams) if isinstance(diagrams, list) else 0}))

    embeds = assets.get("embed_placeholders") or []
    if not isinstance(embeds, list):
        errors.append(Finding(code="ASSETS_EMBEDS_FORMAT", message="03-assets.json.embed_placeholders must be an array", details={}))

    return assets


def validate_concept_cards(
    md: str,
    profile: str,
    errors: List[Finding],
    warnings: List[Finding],
) -> int:
    """Validate CONCEPT_CARD_START/END pairs and required fields per profile."""
    starts = list(re.finditer(r"<!--\s*CONCEPT_CARD_START\b[^>]*-->", md))
    ends = list(re.finditer(r"<!--\s*CONCEPT_CARD_END\s*-->", md))

    if len(starts) != len(ends):
        errors.append(Finding(
            code="CONCEPT_CARD_UNPAIRED",
            message="CONCEPT_CARD_START/END markers are not properly paired",
            details={"starts": len(starts), "ends": len(ends)},
        ))

    card_count = len(starts)
    for i, start_match in enumerate(starts):
        end_pos = ends[i].start() if i < len(ends) else len(md)
        card_text = md[start_match.end():end_pos]

        card_meta = parse_block_metadata(start_match.group())
        card_id = card_meta.get("id", f"concept-{i+1}")

        # Check Scenario field
        has_scenario = bool(re.search(r"\*\*Scenario:\*\*", card_text))
        if not has_scenario:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_SCENARIO",
                message="Concept card missing required field: **Scenario:**",
                details={"card": card_id},
            ))
        else:
            # Validate scenario word count
            scenario_match = re.search(r"\*\*Scenario:\*\*\s*(.*?)(?=\n\n|\*\*\w)", card_text, re.DOTALL)
            if scenario_match:
                sc_words = count_words(scenario_match.group(1))
                if profile in ("showcase", "ideas_templates"):
                    if sc_words < 30 or sc_words > 120:
                        warnings.append(Finding(
                            code="CONCEPT_CARD_SCENARIO_LENGTH",
                            message="Scenario should be 50-100 words for this profile",
                            details={"card": card_id, "words": sc_words},
                        ))
                elif profile == "mega":
                    if sc_words > 50:
                        warnings.append(Finding(
                            code="CONCEPT_CARD_SCENARIO_LENGTH",
                            message="Mega profile scenario should be 20-40 words",
                            details={"card": card_id, "words": sc_words},
                        ))

        # Check Why it works (required for showcase, ideas_templates)
        has_why = bool(re.search(r"\*\*Why it works:\*\*", card_text))
        if profile in ("showcase", "ideas_templates") and not has_why:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_WHY",
                message="Concept card missing required field: **Why it works:**",
                details={"card": card_id, "profile": profile},
            ))

        # Check Key elements (required for showcase, ideas_templates)
        has_key_elements = bool(re.search(r"\*\*Key elements:\*\*", card_text))
        if profile in ("showcase", "ideas_templates") and not has_key_elements:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_KEY_ELEMENTS",
                message="Concept card missing required field: **Key elements:**",
                details={"card": card_id, "profile": profile},
            ))
        elif has_key_elements and profile in ("showcase", "ideas_templates"):
            # Count bullets after Key elements
            ke_match = re.search(r"\*\*Key elements:\*\*\s*(.*?)(?=\n\n|\*\*\w|<!--)", card_text, re.DOTALL)
            if ke_match:
                bullet_count = len(re.findall(r"^[\s]*[-*]\s", ke_match.group(1), re.MULTILINE))
                if bullet_count < 3:
                    errors.append(Finding(
                        code="CONCEPT_CARD_KEY_ELEMENTS_COUNT",
                        message="Key elements must have at least 3 bullets",
                        details={"card": card_id, "count": bullet_count},
                    ))

        # Check Script (required for ideas_templates)
        has_script = bool(re.search(r"\*\*Script:\*\*", card_text))
        if profile == "ideas_templates" and not has_script:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_SCRIPT",
                message="ideas_templates profile requires **Script:** in every concept card",
                details={"card": card_id},
            ))

        # Check Variations (required for ideas_templates)
        has_variations = bool(re.search(r"\*\*Variations:\*\*", card_text))
        if profile == "ideas_templates" and not has_variations:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_VARIATIONS",
                message="ideas_templates profile requires **Variations:** in every concept card",
                details={"card": card_id},
            ))
        elif has_variations and profile == "ideas_templates":
            var_match = re.search(r"\*\*Variations:\*\*\s*(.*?)(?=\n\n|\*\*\w|<!--)", card_text, re.DOTALL)
            if var_match:
                var_count = len(re.findall(r"^[\s]*[-*]\s", var_match.group(1), re.MULTILINE))
                if var_count < 2:
                    errors.append(Finding(
                        code="CONCEPT_CARD_VARIATIONS_COUNT",
                        message="Variations must have at least 2 items",
                        details={"card": card_id, "count": var_count},
                    ))

        # Check Try it CTA (required for all profiles)
        has_cta = bool(re.search(r"\*\*Try it:\*\*", card_text))
        if not has_cta:
            errors.append(Finding(
                code="CONCEPT_CARD_MISSING_CTA",
                message="Concept card missing required field: **Try it:**",
                details={"card": card_id},
            ))

    return card_count


def validate_embed_placeholders(
    md: str,
    concept_count: int,
    profile: str,
    errors: List[Finding],
    warnings: List[Finding],
) -> None:
    """Validate EMBED_PLACEHOLDER markers."""
    embeds = extract_comment_blocks(md, "EMBED_PLACEHOLDER")
    embed_count = len(embeds)

    if profile in ("showcase", "ideas_templates"):
        if embed_count < concept_count:
            errors.append(Finding(
                code="EMBED_COUNT_MISMATCH",
                message=f"Expected {concept_count} EMBED_PLACEHOLDERs (1 per concept), found {embed_count}",
                details={"expected": concept_count, "actual": embed_count, "profile": profile},
            ))
    elif profile == "mega":
        if embed_count == 0:
            warnings.append(Finding(
                code="EMBED_NONE_MEGA",
                message="Mega profile: EMBED_PLACEHOLDERs are recommended but not required",
                details={"count": embed_count},
            ))

    for embed_block in embeds:
        meta = parse_block_metadata(embed_block)
        required_keys = ["id", "type", "alt", "source_hint"]
        for key in required_keys:
            if not meta.get(key):
                warnings.append(Finding(
                    code="EMBED_MISSING_KEY",
                    message=f"EMBED_PLACEHOLDER missing required key: {key}",
                    details={"embed_id": meta.get("id", "unknown"), "missing_key": key},
                ))


def validate_source_attribution(
    md: str,
    plan: Dict[str, Any],
    profile: str,
    errors: List[Finding],
    warnings: List[Finding],
) -> bool:
    """Validate source attribution for brand references. Returns True if adequate."""
    brand_sources = plan.get("brand_sources") or []

    # Check embed placeholders for source_hint
    embeds = extract_comment_blocks(md, "EMBED_PLACEHOLDER")
    missing_hints = 0
    for embed_block in embeds:
        meta = parse_block_metadata(embed_block)
        if not meta.get("source_hint"):
            missing_hints += 1

    if missing_hints > 0:
        warnings.append(Finding(
            code="EMBED_SOURCE_HINT_MISSING",
            message=f"{missing_hints} EMBED_PLACEHOLDER(s) missing source_hint",
            details={"missing_count": missing_hints},
        ))

    # For mega profile or many external brands, check for Sources section
    has_sources_section = bool(re.search(r"##\s+Sources and Credits", md, re.IGNORECASE))

    if profile == "mega" and not has_sources_section:
        warnings.append(Finding(
            code="SOURCE_SECTION_RECOMMENDED",
            message="Mega profile: dedicated 'Sources and Credits' section is recommended",
            details={},
        ))

    if len(brand_sources) > 5 and not has_sources_section:
        warnings.append(Finding(
            code="SOURCE_SECTION_RECOMMENDED_BRANDS",
            message="5+ brand sources: dedicated 'Sources and Credits' section is recommended",
            details={"brand_count": len(brand_sources)},
        ))

    # Attribution is adequate if either inline hints are present or a sources section exists
    return missing_hints == 0 or has_sources_section


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
        errors.append(Finding(code="ARTICLE_NO_H2", message="Article contains no H2 headings", details={}))
        return

    sections_by_norm = {normalize_heading(s["title"]): s for s in h2_sections}

    def get_section(title: str) -> Optional[Dict[str, Any]]:
        return sections_by_norm.get(normalize_heading(title))

    # ---- H2 order validation per profile ----

    if profile == "showcase":
        required_h2 = ["Key Takeaways", "Quick Overview", "How to Recreate", "Pro Tips", "FAQ", "Conclusion"]
    elif profile == "ideas_templates":
        required_h2 = ["Key Takeaways", "Pro Tips", "FAQ", "Conclusion"]
    elif profile == "mega":
        required_h2 = ["Key Takeaways", "Master List", "How to Get Started", "FAQ", "Conclusion"]
    else:
        required_h2 = ["Key Takeaways", "FAQ", "Conclusion"]

    h2_norm_list = [normalize_heading(s["title"]) for s in h2_sections]

    def title_matches(section_title: str, target: str) -> bool:
        return normalize_heading(target) in normalize_heading(section_title)

    def idx_of(target: str) -> int:
        for i, norm in enumerate(h2_norm_list):
            if normalize_heading(target) in norm:
                return i
        return -1

    for title in required_h2:
        if idx_of(title) == -1:
            errors.append(Finding(code="ARTICLE_SECTION_MISSING", message="Missing required H2 section", details={"missing": title}))

    # Check ordering of fixed sections
    if profile == "showcase":
        order_checks = ["Key Takeaways", "Quick Overview", "How to Recreate", "Pro Tips", "FAQ", "Conclusion"]
    elif profile == "ideas_templates":
        order_checks = ["Key Takeaways", "Pro Tips", "FAQ", "Conclusion"]
    elif profile == "mega":
        order_checks = ["Key Takeaways", "Master List", "How to Get Started", "FAQ", "Conclusion"]
    else:
        order_checks = []

    last_idx = -1
    for t in order_checks:
        i = idx_of(t)
        if i != -1 and i < last_idx:
            errors.append(Finding(code="ARTICLE_H2_ORDER", message="H2 sections out of order", details={"section": t}))
        if i != -1:
            last_idx = i

    # ---- Quick Answer / AIDA word count ----
    # Quick Answer is in the content before the first H2
    h1_match = re.search(r"^#\s+.+", md, re.MULTILINE)
    if h1_match and h2_sections:
        qa_text = md[h1_match.end():md.find("\n## ")]
        qa_words = count_words(qa_text)
        if qa_words < 100 or qa_words > 220:
            errors.append(Finding(code="QUICK_ANSWER_WORD_COUNT", message="Quick Answer (AIDA opening) should be 120-180 words", details={"count": qa_words}))

    # ---- Total word count ----
    total_words = count_words(md)
    wmin, wmax = WORD_RANGES.get(profile, (3000, 10000))
    if total_words < wmin or total_words > wmax:
        errors.append(Finding(code="WORD_COUNT_RANGE", message=f"Word count {total_words} outside range {wmin}-{wmax} for profile {profile}", details={"count": total_words, "range": f"{wmin}-{wmax}"}))

    # ---- Key Takeaways ----
    kt = get_section("Key Takeaways")
    key_takeaways_present = kt is not None
    if not key_takeaways_present:
        errors.append(Finding(code="KEY_TAKEAWAYS_MISSING", message="Missing Key Takeaways section", details={}))

    # ---- Concept Cards ----
    concept_count = validate_concept_cards(md, profile, errors, warnings)

    # ---- Embed Placeholders ----
    validate_embed_placeholders(md, concept_count, profile, errors, warnings)

    # ---- Citable Blocks ----
    citable = extract_citable_blocks(md)
    citable_count = len(citable)
    if citable_count < 5:
        errors.append(Finding(code="CITABLE_BLOCKS_COUNT", message="Article must have at least 5 CITABLE_BLOCKs", details={"count": citable_count}))
    citable_types = set(b["type"] for b in citable)
    if len(citable_types) < 3:
        errors.append(Finding(code="CITABLE_BLOCK_TYPES", message="Article must have at least 3 distinct CITABLE_BLOCK types", details={"count": len(citable_types), "types": list(citable_types)}))

    # Check CITABLE_BLOCK pairing
    opens = len(re.findall(r"<!--\s*CITABLE_BLOCK\b", md))
    closes = len(re.findall(r"<!--\s*/CITABLE_BLOCK\s*-->", md))
    if opens != closes:
        errors.append(Finding(code="CITABLE_BLOCK_UNPAIRED", message="CITABLE_BLOCK open/close markers not paired", details={"opens": opens, "closes": closes}))

    # ---- CTA Cards ----
    cta_blocks = extract_comment_blocks(md, "CTA_CARD")
    if len(cta_blocks) < 2:
        errors.append(Finding(code="CTA_CARDS_COUNT", message="Article must have at least 2 CTA_CARD markers", details={"count": len(cta_blocks)}))

    # ---- Image Placeholders ----
    img_blocks = extract_comment_blocks(md, "IMAGE_PLACEHOLDER")
    if len(img_blocks) < 2:
        errors.append(Finding(code="IMAGE_PLACEHOLDER_COUNT", message="Article must have at least 2 IMAGE_PLACEHOLDERs", details={"count": len(img_blocks)}))

    # ---- FAQ ----
    faq_section = get_section("FAQ")
    if faq_section:
        faq_items = parse_faq_items(faq_section["content_lines"])
        if len(faq_items) < 6:
            errors.append(Finding(code="FAQ_MIN_COUNT", message="FAQ must include at least 6 questions", details={"count": len(faq_items)}))
        for q, a in faq_items:
            s_count = count_sentences(a)
            if s_count < 2 or s_count > 4:
                warnings.append(Finding(code="FAQ_ANSWER_SENTENCE_COUNT", message="Each FAQ answer should be 2-4 sentences", details={"question": q, "sentence_count": s_count}))
    else:
        errors.append(Finding(code="FAQ_MISSING", message="Missing FAQ section", details={}))

    # ---- How to Recreate / How to Get Started ----
    how_to_present = False
    if profile in ("showcase", "ideas_templates"):
        for s in h2_sections:
            if "how to recreate" in normalize_heading(s["title"]):
                how_to_present = True
                break
    elif profile == "mega":
        for s in h2_sections:
            if "how to get started" in normalize_heading(s["title"]):
                how_to_present = True
                break
    if not how_to_present:
        label = "How to Recreate" if profile != "mega" else "How to Get Started"
        errors.append(Finding(code="HOW_TO_RECREATE_MISSING", message=f"Missing '{label}' section", details={"profile": profile}))

    # ---- Overview Table (Showcase) ----
    overview_table_valid = True
    if profile == "showcase":
        ov = get_section("Quick Overview")
        if ov:
            tables_obj = (plan.get("tables") or {})
            flex = tables_obj.get("overview_flex_column") or {}
            flex_label = str(flex.get("label") or "Difficulty").strip()
            expected_cols = ["#", "Concept", "Type/Category", "Best For", flex_label]
            tables_found = find_tables(ov["content_lines"])
            if not tables_found:
                errors.append(Finding(code="OVERVIEW_TABLE_MISSING", message="Quick Overview section must contain a table", details={}))
                overview_table_valid = False
            else:
                actual = [c.strip() for c in tables_found[0]["columns"]]
                if actual != expected_cols:
                    errors.append(Finding(code="OVERVIEW_TABLE_COLUMNS", message="Quick Overview table columns mismatch", details={"expected": expected_cols, "actual": actual}))
                    overview_table_valid = False

    # ---- Master List Table (Mega) ----
    if profile == "mega":
        ml = get_section("Master List")
        if ml:
            expected_cols = ["#", "Concept", "Category", "Platform", "Quick Description"]
            require_table_with_columns(errors, "Master List", ml["content_lines"], expected_cols, "MASTER_LIST_TABLE")
        # Mega must have categorization (>=3 categories)
        category_h2s = [s for s in h2_sections
                        if normalize_heading(s["title"]) not in
                        {normalize_heading(t) for t in ["Key Takeaways", "Master List", "Sources and Credits", "How to Get Started", "FAQ", "Conclusion"]}
                        and not s["title"].startswith("#")]
        if len(category_h2s) < 3:
            errors.append(Finding(code="MEGA_CATEGORIES_MIN", message="Mega profile requires at least 3 category H2 sections", details={"count": len(category_h2s)}))

    # ---- Source Attribution ----
    source_adequate = validate_source_attribution(md, plan, profile, errors, warnings)

    # Store results for report
    validate_article._results = {
        "concept_count": concept_count,
        "total_words": total_words,
        "citable_count": citable_count,
        "citable_types": len(citable_types),
        "faq_count": len(faq_items) if faq_section else 0,
        "cta_count": len(cta_blocks),
        "embed_count": len(extract_comment_blocks(md, "EMBED_PLACEHOLDER")),
        "key_takeaways_present": key_takeaways_present,
        "how_to_present": how_to_present,
        "overview_table_valid": overview_table_valid,
        "source_adequate": source_adequate,
        "qa_words": qa_words if h1_match and h2_sections else 0,
    }


def _write_report(
    base_dir: Path,
    profile: str,
    plan: Dict[str, Any],
    errors: List[Finding],
    warnings: List[Finding],
    files: Dict[str, Any],
) -> Dict[str, Any]:
    r = getattr(validate_article, "_results", {})
    meta = (plan.get("meta") or {}) if isinstance(plan, dict) else {}
    target_count = meta.get("concept_count_target", "?")
    wmin, wmax = WORD_RANGES.get(profile, (3000, 10000))

    has_errors = bool(errors)

    report = {
        "status": "FAIL" if has_errors else "PASS",
        "profile": profile,
        "checks": {
            "concept_count": {"expected": target_count, "actual": r.get("concept_count", 0), "pass": not any(e.code.startswith("CONCEPT_CARD") for e in errors)},
            "word_count_in_range": {"range": f"{wmin}-{wmax}", "actual": r.get("total_words", 0), "pass": not any(e.code == "WORD_COUNT_RANGE" for e in errors)},
            "h2_order_correct": not any(e.code == "ARTICLE_H2_ORDER" for e in errors),
            "all_concept_cards_have_required_fields": not any(e.code.startswith("CONCEPT_CARD_MISSING") for e in errors),
            "citable_blocks_count": {"min": 5, "actual": r.get("citable_count", 0), "pass": not any(e.code == "CITABLE_BLOCKS_COUNT" for e in errors)},
            "citable_block_types_distinct": {"min": 3, "actual": r.get("citable_types", 0), "pass": not any(e.code == "CITABLE_BLOCK_TYPES" for e in errors)},
            "faq_count": {"min": 6, "actual": r.get("faq_count", 0), "pass": not any(e.code == "FAQ_MIN_COUNT" for e in errors)},
            "cta_cards_count": {"min": 2, "actual": r.get("cta_count", 0), "pass": not any(e.code == "CTA_CARDS_COUNT" for e in errors)},
            "embed_placeholders_count": {"expected": r.get("concept_count", 0), "actual": r.get("embed_count", 0), "pass": not any(e.code == "EMBED_COUNT_MISMATCH" for e in errors)},
            "concept_card_markers_paired": not any(e.code == "CONCEPT_CARD_UNPAIRED" for e in errors),
            "quick_answer_word_count": {"range": "120-180", "actual": r.get("qa_words", 0), "pass": not any(e.code == "QUICK_ANSWER_WORD_COUNT" for e in errors)},
            "key_takeaways_present": r.get("key_takeaways_present", False),
            "how_to_recreate_present": r.get("how_to_present", False),
            "overview_table_columns_valid": r.get("overview_table_valid", True),
            "source_attribution_adequate": r.get("source_adequate", True),
        },
        "profile_specific_checks": {},
        "errors": [f.__dict__ for f in errors],
        "warnings": [f.__dict__ for f in warnings],
        "files": files,
    }

    # Profile-specific checks
    if profile == "ideas_templates":
        report["profile_specific_checks"]["scripts_present_in_all_cards"] = not any(e.code == "CONCEPT_CARD_MISSING_SCRIPT" for e in errors)
        report["profile_specific_checks"]["variations_present_in_all_cards"] = not any(e.code == "CONCEPT_CARD_MISSING_VARIATIONS" for e in errors)
    if profile == "mega":
        report["profile_specific_checks"]["categorization_present"] = not any(e.code == "MEGA_CATEGORIES_MIN" for e in errors)

    try:
        out_path = base_dir / "04-examples-validator-report.json"
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        pass

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Examples & Ideas Writer v3.0 output bundle")
    parser.add_argument("--dir", required=True, help="Directory containing 01-article-draft.md, 02-plan.json, 03-assets.json")
    parser.add_argument("--profile", default="", help="Override profile: showcase|ideas_templates|mega")
    args = parser.parse_args()

    base_dir = Path(args.dir).expanduser().resolve()
    errors: List[Finding] = []
    warnings: List[Finding] = []

    if not base_dir.exists() or not base_dir.is_dir():
        errors.append(Finding(code="DIR_INVALID", message="--dir must be an existing directory", details={"dir": str(base_dir)}))
        _write_report(base_dir, args.profile or "", {}, errors, warnings, {})
        return 1

    article_path = base_dir / "01-article-draft.md"
    if not article_path.exists():
        alt = base_dir / "01-article.md"
        if alt.exists():
            article_path = alt
        else:
            errors.append(Finding(code="ARTICLE_MISSING", message="Missing required article file: 01-article-draft.md", details={}))

    plan_path = base_dir / "02-plan.json"
    assets_path = base_dir / "03-assets.json"

    plan = validate_plan_pack(plan_path, errors, warnings)
    _ = validate_assets_queue(assets_path, errors)

    profile = (args.profile or "").strip()
    if not profile:
        meta = (plan.get("meta") or {}) if isinstance(plan, dict) else {}
        profile = str(meta.get("examples_profile") or "showcase").strip()
    if profile not in VALID_PROFILES:
        errors.append(Finding(code="PROFILE_INVALID", message=f"Invalid profile; must be one of {VALID_PROFILES}", details={"profile": profile}))

    if article_path.exists() and isinstance(plan, dict) and plan:
        validate_article(article_path, plan, profile, errors, warnings)

    report = _write_report(base_dir, profile, plan, errors, warnings, {"article": str(article_path)})
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
