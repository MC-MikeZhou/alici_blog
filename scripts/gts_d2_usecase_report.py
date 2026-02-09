#!/usr/bin/env python3
"""
Generate a one-shot D1 vs D2 validation report for Seed Mode D2 (Diversity Engine).

This script is intentionally offline-friendly:
- It DOES NOT call DataForSEO (network may be restricted in this environment).
- It consumes existing validated artifacts already saved in the repo.
- It reconstructs a "D2-like" portfolio selection by applying cosine similarity
  on TF-IDF vectors (pure Python) + diversity gates.

Outputs:
  reports/2026-02-03-growth-topic-scout-v2.3-d2-usecase-validation/
    - 00-validation-report.md
    - 01-results.csv
    - uc1.json / uc2.json / uc3.json (machine-readable intermediate)
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
REPORT_DATE = date(2026, 2, 3)
OUT_DIR = ROOT / "reports" / "2026-02-03-growth-topic-scout-v2.3-d2-usecase-validation"


def _strip_control_chars(s: str) -> str:
    # Keep common whitespace; drop other C0 controls that break JSON parsing.
    kept = []
    for ch in s:
        code = ord(ch)
        if code in (9, 10, 13) or code >= 32:
            kept.append(ch)
        else:
            kept.append(" ")
    return "".join(kept)


def load_json_loose(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = _strip_control_chars(raw)
        return json.loads(cleaned)


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "unknown"


def tokenize(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [t for t in tokens if len(t) >= 2]


def tfidf_vectors(texts: Sequence[str]) -> List[Dict[str, float]]:
    docs = [tokenize(t) for t in texts]
    n = len(docs)
    df: Dict[str, int] = {}
    for doc in docs:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1

    idf: Dict[str, float] = {}
    for term, dfi in df.items():
        idf[term] = math.log((n + 1) / (dfi + 1)) + 1.0

    vectors: List[Dict[str, float]] = []
    for doc in docs:
        if not doc:
            vectors.append({})
            continue
        tf: Dict[str, float] = {}
        for term in doc:
            tf[term] = tf.get(term, 0.0) + 1.0
        inv_len = 1.0 / len(doc)
        vec: Dict[str, float] = {}
        for term, cnt in tf.items():
            vec[term] = (cnt * inv_len) * idf.get(term, 0.0)
        vectors.append(vec)
    return vectors


def cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    dot = 0.0
    if len(a) > len(b):
        a, b = b, a
    for k, v in a.items():
        dot += v * b.get(k, 0.0)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def pairwise_sims(vectors: Sequence[Dict[str, float]]) -> Tuple[float, float]:
    n = len(vectors)
    if n < 2:
        return (0.0, 0.0)
    total = 0.0
    max_sim = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine(vectors[i], vectors[j])
            total += s
            max_sim = max(max_sim, s)
            count += 1
    return (total / count, max_sim)


def infer_intent_type(text: str) -> str:
    t = text.lower()
    if " vs " in t or t.startswith("vs ") or "versus" in t:
        return "comparison"
    if t.startswith("how to ") or " how to " in t:
        return "how-to"
    if t.startswith("best ") or t.startswith("top ") or " best " in t or " top " in t:
        return "list"
    if any(w in t for w in ("fix", "why", "looks", "error", "mistake", "broken")):
        return "troubleshooting"
    if any(w in t for w in ("workflow", "playbook", "step", "template", "checklist")):
        return "workflow"
    return "use-case"


def heuristic_strategy(intent_type: str, text: str) -> str:
    t = text.lower()
    if intent_type == "comparison" or " vs " in t:
        return "serp_gap"
    if intent_type == "troubleshooting":
        return "persona_rotation"
    return "seed_xpollination"


@dataclass(frozen=True)
class Direction:
    id: str
    title: str
    primary_keyword: str
    theme: str
    intent_type: str
    seo_score: float
    aeo_score: float
    volume: float
    strategy_source: Optional[str] = None
    cluster_id: Optional[str] = None

    @property
    def value_score(self) -> float:
        return (self.seo_score + self.aeo_score) / 2.0

    def signature_text(self) -> str:
        parts = [self.title, self.primary_keyword, self.theme, self.intent_type]
        return " | ".join([p for p in parts if p])


def greedy_cluster(items: Sequence[Direction], threshold: float) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """
    Returns:
      item_id -> cluster_id
      cluster_id -> [item_id]
    """
    vectors = tfidf_vectors([it.signature_text() for it in items])
    clusters: List[Tuple[str, int]] = []  # (cluster_id, representative_index)
    assignments: Dict[str, str] = {}
    members: Dict[str, List[str]] = {}

    def new_cluster_id(k: int) -> str:
        return f"C{k:02d}"

    for idx, it in enumerate(items):
        assigned: Optional[str] = None
        for k, rep_idx in clusters:
            s = cosine(vectors[idx], vectors[rep_idx])
            if s >= threshold:
                assigned = k
                break
        if assigned is None:
            assigned = new_cluster_id(len(clusters) + 1)
            clusters.append((assigned, idx))
            members[assigned] = []
        assignments[it.id] = assigned
        members.setdefault(assigned, []).append(it.id)

    return assignments, members


def select_d2_portfolio(
    candidates: Sequence[Direction],
    cluster_threshold: float,
    target_avg_similarity: float,
    final_pairwise_max: float,
    min_final_clusters: int,
    min_intent_types_final: int,
    must_include_intents: Optional[Sequence[str]] = None,
    require_non_competitor_source: bool = True,
) -> Tuple[List[Direction], Dict[str, Any]]:
    """
    Select final 3 directions under diversity constraints, and build a diversity_report-like dict.
    """
    if not candidates:
        return [], {
            "engine_version": "2.3-diversity-offline",
            "thresholds": {
                "cluster_threshold": cluster_threshold,
                "target_avg_similarity": target_avg_similarity,
                "final_pairwise_max": final_pairwise_max,
            },
            "metrics": {},
            "strategy_mix": {},
            "gate_passed": False,
            "rejection_log": [{"reason": "no candidates"}],
        }

    sorted_candidates = sorted(candidates, key=lambda d: (d.value_score, d.volume), reverse=True)
    assignments, cluster_members = greedy_cluster(sorted_candidates, threshold=cluster_threshold)

    with_clusters: List[Direction] = []
    for it in sorted_candidates:
        with_clusters.append(
            Direction(
                id=it.id,
                title=it.title,
                primary_keyword=it.primary_keyword,
                theme=it.theme,
                intent_type=it.intent_type,
                seo_score=it.seo_score,
                aeo_score=it.aeo_score,
                volume=it.volume,
                strategy_source=it.strategy_source,
                cluster_id=assignments.get(it.id),
            )
        )

    selected: List[Direction] = []
    rejection_log: List[Dict[str, str]] = []

    def selected_vectors(items: Sequence[Direction]) -> List[Dict[str, float]]:
        return tfidf_vectors([it.signature_text() for it in items])

    def max_similarity_to_selected(candidate: Direction, current: Sequence[Direction]) -> float:
        if not current:
            return 0.0
        vecs = tfidf_vectors([candidate.signature_text()] + [it.signature_text() for it in current])
        c = vecs[0]
        return max(cosine(c, v) for v in vecs[1:])

    must_include_intents = list(must_include_intents or [])

    # First pass: pick top items that satisfy pairwise max constraint and (soft) intent coverage.
    for it in with_clusters:
        if len(selected) >= 3:
            break

        # Hard constraint: pairwise similarity to existing picks.
        sim_to_sel = max_similarity_to_selected(it, selected)
        if sim_to_sel >= final_pairwise_max:
            rejection_log.append({"topic_id": it.id, "reason": f"too similar to selected (sim={sim_to_sel:.2f} >= {final_pairwise_max:.2f})"})
            continue

        selected.append(it)

    # Second pass: enforce must_include_intents if specified (swap in).
    if must_include_intents:
        present = {d.intent_type for d in selected}
        missing = [i for i in must_include_intents if i not in present]
        if missing:
            for needed in missing:
                # Find best candidate of that intent not yet selected and not too similar.
                for it in with_clusters:
                    if it.id in {d.id for d in selected}:
                        continue
                    if it.intent_type != needed:
                        continue
                    sim_to_sel = max_similarity_to_selected(it, selected)
                    if sim_to_sel >= final_pairwise_max:
                        continue
                    # Replace the weakest (by value_score) if it improves intent coverage.
                    weakest_idx = min(range(len(selected)), key=lambda k: selected[k].value_score)
                    selected[weakest_idx] = it
                    present = {d.intent_type for d in selected}
                    break

    # Ensure minimum distinct intent types (best-effort).
    def ensure_min_intents() -> None:
        nonlocal selected
        for _ in range(6):
            intents = {d.intent_type for d in selected}
            if len(intents) >= min_intent_types_final:
                return
            weakest_idx = min(range(len(selected)), key=lambda k: selected[k].value_score)
            weakest = selected[weakest_idx]
            for it in with_clusters:
                if it.id in {d.id for d in selected}:
                    continue
                if it.intent_type in intents:
                    continue
                sim_to_sel = max_similarity_to_selected(it, selected)
                if sim_to_sel >= final_pairwise_max:
                    continue
                selected[weakest_idx] = it
                break

    if len(selected) == 3:
        ensure_min_intents()

    # Ensure minimum clusters among finals (best-effort).
    def ensure_min_clusters() -> None:
        nonlocal selected
        for _ in range(6):
            clusters = {d.cluster_id for d in selected if d.cluster_id}
            if len(clusters) >= min_final_clusters:
                return
            weakest_idx = min(range(len(selected)), key=lambda k: selected[k].value_score)
            weakest = selected[weakest_idx]
            for it in with_clusters:
                if it.id in {d.id for d in selected}:
                    continue
                if it.cluster_id in clusters:
                    continue
                sim_to_sel = max_similarity_to_selected(it, selected)
                if sim_to_sel >= final_pairwise_max:
                    continue
                selected[weakest_idx] = it
                break

    if len(selected) == 3:
        ensure_min_clusters()

    # Strategy mix constraint: at least one from persona_rotation or serp_gap (heuristic; best-effort).
    if require_non_competitor_source and len(selected) == 3:
        if not any((d.strategy_source or "") in ("persona_rotation", "serp_gap") for d in selected):
            weakest_idx = min(range(len(selected)), key=lambda k: selected[k].value_score)
            for it in with_clusters:
                if it.id in {d.id for d in selected}:
                    continue
                if (it.strategy_source or "") not in ("persona_rotation", "serp_gap"):
                    continue
                sim_to_sel = max_similarity_to_selected(it, selected)
                if sim_to_sel >= final_pairwise_max:
                    continue
                selected[weakest_idx] = it
                break

    # Compute similarities among finals and diversity bonus.
    finals_vecs = tfidf_vectors([d.signature_text() for d in selected])
    avg_sim, max_sim = pairwise_sims(finals_vecs)
    intent_count = len({d.intent_type for d in selected})
    final_cluster_count = len({d.cluster_id for d in selected if d.cluster_id})
    strategy_counts: Dict[str, int] = {}
    for d in selected:
        k = d.strategy_source or "unknown"
        strategy_counts[k] = strategy_counts.get(k, 0) + 1

    gate_passed = (
        avg_sim < target_avg_similarity
        and final_cluster_count >= min_final_clusters
        and intent_count >= min_intent_types_final
    )

    # Similarity-to-other-finals table + diversity bonus per direction.
    sim_matrix: Dict[str, List[Dict[str, Any]]] = {d.id: [] for d in selected}
    for i, di in enumerate(selected):
        for j, dj in enumerate(selected):
            if i == j:
                continue
            s = cosine(finals_vecs[i], finals_vecs[j])
            sim_matrix[di.id].append({"direction_id": dj.id, "similarity": round(s, 4)})

    def bonus_for(max_sim_to_others: float) -> int:
        if max_sim_to_others < 0.40:
            return 15
        if max_sim_to_others < 0.50:
            return 10
        if max_sim_to_others < 0.60:
            return 5
        return 0

    enriched: List[Direction] = []
    for d in selected:
        max_to_others = max((x["similarity"] for x in sim_matrix[d.id]), default=0.0)
        bonus = bonus_for(max_to_others)
        portfolio_score = d.value_score + bonus
        enriched.append(
            Direction(
                id=d.id,
                title=d.title,
                primary_keyword=d.primary_keyword,
                theme=d.theme,
                intent_type=d.intent_type,
                seo_score=d.seo_score,
                aeo_score=d.aeo_score,
                volume=d.volume,
                strategy_source=d.strategy_source,
                cluster_id=d.cluster_id,
            )
        )

    diversity_report = {
        "engine_version": "2.3-diversity-offline",
        "thresholds": {
            "cluster_threshold": cluster_threshold,
            "target_avg_similarity": target_avg_similarity,
            "final_pairwise_max": final_pairwise_max,
            "min_final_clusters": min_final_clusters,
            "min_intent_types_final": min_intent_types_final,
        },
        "metrics": {
            "avg_pairwise_similarity": round(avg_sim, 4),
            "max_pairwise_similarity": round(max_sim, 4),
            "cluster_count": final_cluster_count,
            "intent_type_count": intent_count,
        },
        "strategy_mix": {
            "counts": strategy_counts,
        },
        "gate_passed": gate_passed,
        "rejection_log": rejection_log[:50],
        "similarity_to_other_finals": sim_matrix,
        "notes": [
            "This diversity report is reconstructed offline using TF-IDF cosine similarity (lexical proxy).",
            "Strategy sources are heuristic labels derived from intent types; not from an actual D2 runtime.",
        ],
    }

    return enriched, diversity_report


def _direction_from_seed_d1(d: Dict[str, Any], idx: int) -> Direction:
    locked = (d.get("locked_title") or {})
    title = locked.get("title") or d.get("title") or ""
    pk = locked.get("primary_keyword") or d.get("primary_keyword") or ""
    theme = d.get("theme") or ""
    seo = float(d.get("seo_score") or 0)
    aeo = float(d.get("aeo_score") or 0)
    vol = float((d.get("evidence_chain") or {}).get("volume") or 0)
    intent = infer_intent_type(title or pk or theme)
    return Direction(
        id=d.get("direction_id") or f"D1-{idx+1}",
        title=title,
        primary_keyword=pk,
        theme=theme,
        intent_type=intent,
        seo_score=seo,
        aeo_score=aeo,
        volume=vol,
        strategy_source="competitor_diverge",
        cluster_id=None,
    )


def build_uc1() -> Dict[str, Any]:
    """
    UC1: UGC 广告/UGC 创作者起步（使用已有 Seed D1 漏斗产物）。
    """
    base = ROOT / "reports 待发文章" / "2026-02-03-ugc-creator-guide-2026"
    d1_brief = load_json_loose(base / "00-topic-brief.json")
    d1_dirs_raw = d1_brief.get("final_directions", [])
    d1_dirs = [_direction_from_seed_d1(x, i) for i, x in enumerate(d1_dirs_raw)]

    top_dirs = load_json_loose(base / "03-top-directions.json")
    cand_raw = top_dirs.get("directions_top10", [])
    candidates: List[Direction] = []
    for i, x in enumerate(cand_raw):
        title = x.get("theme") or x.get("primary_keyword") or f"candidate-{i+1}"
        pk = x.get("primary_keyword") or title
        intent = infer_intent_type(pk)
        strat = heuristic_strategy(intent, pk)
        candidates.append(
            Direction(
                id=f"UC1-C{i+1:02d}",
                title=title,
                primary_keyword=pk,
                theme=x.get("theme") or "",
                intent_type=intent,
                seo_score=float(x.get("seo_score") or 0),
                aeo_score=float(x.get("aeo_score") or 0),
                volume=float(x.get("total_volume") or 0),
                strategy_source=strat,
            )
        )

    d2_dirs, diversity_report = select_d2_portfolio(
        candidates=candidates,
        cluster_threshold=0.60,
        target_avg_similarity=0.50,
        final_pairwise_max=0.60,
        min_final_clusters=3,
        min_intent_types_final=2,
        must_include_intents=["how-to", "troubleshooting", "list"],
        require_non_competitor_source=True,
    )

    return {
        "use_case_id": "UC1",
        "zh_prompt": "UGC 广告，用 AI 怎么做？",
        "seed": "ugc creator (proxy for ai ugc ads)",
        "source_dir": str(base),
        "d1": {
            "directions": [d.__dict__ for d in d1_dirs],
        },
        "d2": {
            "directions": [d.__dict__ for d in d2_dirs],
            "diversity_report": diversity_report,
        },
        "notes": [
            "UC1 uses an existing Seed D1 run ('ugc creator') as a proxy for the UGC ads use case.",
        ],
    }


def build_uc2() -> Dict[str, Any]:
    """
    UC2: Top 10 AI Video Generators（使用 keyword_matrix + gap/aeo 数据，离线重构 D2 selection）。
    """
    base = ROOT / "reports 待发文章" / "2026-01-24-ai-video-tools-2026"
    km = load_json_loose(base / "keyword_matrix.json")
    aeo = load_json_loose(base / "aeo_validation.json")
    brief = load_json_loose(base / "00-topic-brief.json")
    gap = load_json_loose(base / "gap_analysis.json")

    # Build helper maps.
    seo_aeo_by_keyword: Dict[str, Tuple[float, float]] = {}
    for t in brief.get("priority_topics", []) or []:
        seo_aeo_by_keyword[t.get("primary_keyword")] = (float(t.get("seo_score") or 0), float(t.get("aeo_score") or 0))

    ai_op_by_keyword: Dict[str, float] = {}
    for item in (aeo.get("phase_c1_ai_keyword_data") or {}).get("keywords", []) or []:
        ai_op_by_keyword[item.get("keyword")] = float(item.get("ai_opportunity_score") or 0)

    serp_by_keyword: Dict[str, Dict[str, Any]] = {}
    for item in gap.get("topics", []) or []:
        serp_by_keyword[item.get("keyword")] = item.get("serp_analysis") or {}

    candidates: List[Direction] = []
    keywords = km.get("keywords", []) or []
    for i, item in enumerate(keywords):
        kw = item.get("keyword") or f"kw-{i+1}"
        content_type = item.get("content_type") or ""
        intent = infer_intent_type(kw)
        strat = heuristic_strategy(intent, kw)
        vol = float(item.get("search_volume") or 0)
        opp = float(item.get("opportunity_score") or 0)
        seo_score = seo_aeo_by_keyword.get(kw, (opp, 0.0))[0]

        # AEO score proxy: prefer existing aeo_score, else AI opportunity score, else SERP features heuristic.
        aeo_score = seo_aeo_by_keyword.get(kw, (0.0, 0.0))[1]
        if aeo_score == 0.0:
            if kw in ai_op_by_keyword:
                aeo_score = ai_op_by_keyword[kw]
            else:
                serp = serp_by_keyword.get(kw, {})
                aeo_score = 0.0
                if serp.get("ai_overview"):
                    aeo_score += 35
                if serp.get("featured_snippet") is False and serp.get("ai_overview") is True:
                    aeo_score += 10
                paa = int(serp.get("paa_count") or 0)
                if paa >= 5:
                    aeo_score += 25
                elif paa > 0:
                    aeo_score += 15
                aeo_score = min(100.0, aeo_score)

        title = kw
        theme = "AI Video Tools"
        candidates.append(
            Direction(
                id=f"UC2-C{i+1:02d}",
                title=title,
                primary_keyword=kw,
                theme=theme,
                intent_type=intent,
                seo_score=float(seo_score),
                aeo_score=float(aeo_score),
                volume=vol,
                strategy_source=strat,
            )
        )

    # D1 baseline proxy: top 2 by value score.
    d1_sorted = sorted(candidates, key=lambda d: (d.value_score, d.volume), reverse=True)
    d1_dirs = d1_sorted[:2]

    d2_dirs, diversity_report = select_d2_portfolio(
        candidates=candidates,
        cluster_threshold=0.60,
        target_avg_similarity=0.50,
        final_pairwise_max=0.60,
        min_final_clusters=3,
        min_intent_types_final=2,
        must_include_intents=["list", "comparison"],
        require_non_competitor_source=True,
    )

    return {
        "use_case_id": "UC2",
        "zh_prompt": "10个最佳 AI Video Generator 是什么？",
        "seed": "best ai video generator (proxy via ai video tools 2026 dataset)",
        "source_dir": str(base),
        "d1": {
            "directions": [d.__dict__ for d in d1_dirs],
            "note": "D1 baseline is reconstructed as top-2 by (SEO+AEO)/2 from existing validated keyword matrix outputs.",
        },
        "d2": {
            "directions": [d.__dict__ for d in d2_dirs],
            "diversity_report": diversity_report,
        },
        "notes": [
            "UC2 uses the existing ai-video-tools-2026 keyword matrix (validated) as the candidate pool.",
        ],
    }


def build_uc3() -> Dict[str, Any]:
    """
    UC3: AI Influencer 起步（使用已有 DataForSEO 验证产物；注意该 seed 在历史数据中 volume=0 属于 emerging）。"""
    base = ROOT / "reports" / "2026-01-27-batch-ai-influencer"
    validation = load_json_loose(base / "00-dataforseo-validation.json")

    candidates: List[Direction] = []
    for i, item in enumerate(validation.get("keywords", []) or []):
        kw = item.get("keyword") or f"kw-{i+1}"
        sm = item.get("search_metrics") or {}
        serp = item.get("serp_features") or {}

        vol = float(sm.get("monthly_search_volume") or 0)
        cpc = float(sm.get("cpc_usd") or 0)
        # Proxy SEO/AEO scores from limited fields.
        seo_score = 0.0
        if vol >= 10000:
            seo_score += 80
        elif vol >= 1000:
            seo_score += 65
        elif vol >= 100:
            seo_score += 50
        else:
            seo_score += 35  # emerging baseline

        if sm.get("competition_level") == "LOW":
            seo_score += 10
        seo_score = min(100.0, seo_score)

        aeo_score = 0.0
        if serp.get("featured_snippet_present"):
            aeo_score += 30
        if serp.get("people_also_ask"):
            aeo_score += 20
        if serp.get("ai_overview_present"):
            aeo_score += 35
        if serp.get("video_results"):
            aeo_score += 10
        aeo_score = min(100.0, aeo_score)

        intent = infer_intent_type(kw)
        strat = heuristic_strategy(intent, kw)
        candidates.append(
            Direction(
                id=f"UC3-C{i+1:02d}",
                title=kw,
                primary_keyword=kw,
                theme="AI Influencer",
                intent_type=intent,
                seo_score=seo_score,
                aeo_score=aeo_score,
                volume=vol,
                strategy_source=strat,
            )
        )

    d1_sorted = sorted(candidates, key=lambda d: (d.value_score, d.volume), reverse=True)
    d1_dirs = d1_sorted[:2]

    d2_dirs, diversity_report = select_d2_portfolio(
        candidates=candidates,
        cluster_threshold=0.60,
        target_avg_similarity=0.50,
        final_pairwise_max=0.60,
        min_final_clusters=3,
        min_intent_types_final=2,
        must_include_intents=["how-to", "list"],
        require_non_competitor_source=True,
    )

    return {
        "use_case_id": "UC3",
        "zh_prompt": "我想做一个 AI Influencer 的账号，我该怎么准备？用什么工具起步？有没有什么教程能让我快速赚到钱？",
        "seed": "ai influencer tools (proxy via batch-ai-influencer dataset)",
        "source_dir": str(base),
        "d1": {
            "directions": [d.__dict__ for d in d1_dirs],
            "note": "D1 baseline is reconstructed from a small validated keyword set (4 keywords).",
        },
        "d2": {
            "directions": [d.__dict__ for d in d2_dirs],
            "diversity_report": diversity_report,
        },
        "notes": [
            "UC3 dataset is niche/emerging (monthly_search_volume=0 for all validated keywords in saved artifacts).",
            "Treat value comparisons as direction-quality proxy (SERP features) rather than demand validation.",
        ],
    }


def _avg_value(directions: Sequence[Dict[str, Any]]) -> float:
    if not directions:
        return 0.0
    vals = []
    for d in directions:
        vals.append((float(d.get("seo_score") or 0) + float(d.get("aeo_score") or 0)) / 2.0)
    return sum(vals) / len(vals)


def _cosine_between_titles(directions: Sequence[Dict[str, Any]]) -> float:
    if len(directions) < 2:
        return 0.0
    texts = [str(d.get("title") or "") for d in directions[:2]]
    vecs = tfidf_vectors(texts)
    return cosine(vecs[0], vecs[1])


def _d2_avg_similarity(diversity_report: Dict[str, Any]) -> float:
    return float(((diversity_report.get("metrics") or {}).get("avg_pairwise_similarity")) or 0.0)


def write_outputs(uc_results: List[Dict[str, Any]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write intermediate JSONs for reproducibility.
    for uc in uc_results:
        (OUT_DIR / f"{uc['use_case_id'].lower()}.json").write_text(
            json.dumps(uc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # CSV summary.
    csv_path = OUT_DIR / "01-results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "use_case_id",
            "seed",
            "d1_avg_score",
            "d2_avg_score",
            "d1_final_sim",
            "d2_avg_sim",
            "d2_cluster_count",
            "d2_intent_count",
            "pass_diversity",
            "pass_value",
            "notes",
        ])

        for uc in uc_results:
            d1_dirs = (uc.get("d1") or {}).get("directions") or []
            d2_dirs = (uc.get("d2") or {}).get("directions") or []
            dr = (uc.get("d2") or {}).get("diversity_report") or {}

            d1_avg = _avg_value(d1_dirs)
            d2_avg = _avg_value(d2_dirs)
            d1_sim = _cosine_between_titles(d1_dirs)
            d2_sim = _d2_avg_similarity(dr)

            metrics = dr.get("metrics") or {}
            cluster_count = metrics.get("cluster_count") or 0
            intent_count = metrics.get("intent_type_count") or 0
            pass_div = bool(dr.get("gate_passed"))
            pass_val = bool(d2_avg >= (d1_avg - 5.0))

            w.writerow([
                uc.get("use_case_id"),
                uc.get("seed"),
                f"{d1_avg:.2f}",
                f"{d2_avg:.2f}",
                f"{d1_sim:.4f}",
                f"{d2_sim:.4f}",
                cluster_count,
                intent_count,
                "PASS" if pass_div else "FAIL",
                "PASS" if pass_val else "FAIL",
                "; ".join(uc.get("notes") or []),
            ])

    # Markdown report.
    md_path = OUT_DIR / "00-validation-report.md"

    lines: List[str] = []
    lines.append("# Seed Mode D2（Diversity Engine）三用例对比验证报告\n")
    lines.append(f"**Date**: {REPORT_DATE.isoformat()}  \n")
    lines.append("**Scope**: 3 use cases × (D1 baseline vs D2 diversity selection)  \n")
    lines.append("**Data constraint**: 本环境网络受限，本报告使用仓库内已落盘的验证产物，离线重构 D2 的“聚类/去重/门禁/选 3”流程。\n")
    lines.append("\n---\n\n")

    lines.append("## 方法说明（重要）\n\n")
    lines.append("- **D1 baseline**：优先使用已存在的 Seed D1 `final_directions`；若缺失，则用候选池按 (SEO+AEO)/2 取 Top2 作为“D1 proxy”。\n")
    lines.append("- **D2 reconstruction**：对同一候选池应用 **TF-IDF 余弦相似度（词面 proxy）** 做 greedy clustering + diversity gate + 最终 3 方向组合约束。\n")
    lines.append("- **相似度口径**：D1 的 `d1_final_sim` 是最终 2 个标题的 TF-IDF cosine；D2 的 `avg_pairwise_similarity` 来自 final 3 的平均两两相似度。\n")
    lines.append("- **注意**：这不是“真正线上 D2 执行”（LLM 语义 embedding / WebSearch）；因此结果用于评估 *机制可行性* 与 *门禁可操作性*，不等同于最终线上效果。\n")
    lines.append("\n---\n\n")

    lines.append("## 结果总览（PASS/FAIL）\n\n")
    lines.append("| Use Case | D1 平均分 | D2 平均分 | D1 相似度 | D2 平均相似度 | D2 Clusters | D2 Intents | 多样性门禁 | 价值门禁 |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|---|\n")
    for uc in uc_results:
        d1_dirs = (uc.get("d1") or {}).get("directions") or []
        d2_dirs = (uc.get("d2") or {}).get("directions") or []
        dr = (uc.get("d2") or {}).get("diversity_report") or {}
        metrics = dr.get("metrics") or {}

        d1_avg = _avg_value(d1_dirs)
        d2_avg = _avg_value(d2_dirs)
        d1_sim = _cosine_between_titles(d1_dirs)
        d2_sim = _d2_avg_similarity(dr)
        pass_div = bool(dr.get("gate_passed"))
        pass_val = bool(d2_avg >= (d1_avg - 5.0))

        lines.append(
            f"| {uc['use_case_id']} | {d1_avg:.2f} | {d2_avg:.2f} | {d1_sim:.4f} | {d2_sim:.4f} | "
            f"{metrics.get('cluster_count',0)} | {metrics.get('intent_type_count',0)} | "
            f"{'PASS' if pass_div else 'FAIL'} | {'PASS' if pass_val else 'FAIL'} |\n"
        )

    lines.append("\n---\n\n")

    for uc in uc_results:
        lines.append(f"## {uc['use_case_id']}: {uc['zh_prompt']}\n\n")
        lines.append(f"- Seed（用于候选池）: `{uc['seed']}`  \n")
        lines.append(f"- 数据来源目录: `{uc['source_dir']}`\n\n")

        d1_dirs = (uc.get("d1") or {}).get("directions") or []
        d2_dirs = (uc.get("d2") or {}).get("directions") or []
        dr = (uc.get("d2") or {}).get("diversity_report") or {}

        lines.append("### D1 Baseline（2 个方向）\n\n")
        if (uc.get("d1") or {}).get("note"):
            lines.append(f"> 注：{(uc.get('d1') or {}).get('note')}\n\n")
        for i, d in enumerate(d1_dirs, start=1):
            lines.append(
                f"{i}. **{d.get('title','').strip()}**  \n"
                f"   - keyword: `{d.get('primary_keyword','')}`  \n"
                f"   - intent: `{d.get('intent_type','')}`  \n"
                f"   - SEO/AEO: {float(d.get('seo_score') or 0):.0f} / {float(d.get('aeo_score') or 0):.0f}  \n"
                f"   - volume: {float(d.get('volume') or 0):.0f}\n"
            )
        lines.append("\n")

        lines.append("### D2 Reconstructed（3 个方向 + 多样性门禁）\n\n")
        metrics = (dr.get("metrics") or {})
        lines.append(
            f"- Diversity metrics: avg_sim={metrics.get('avg_pairwise_similarity')}, "
            f"max_sim={metrics.get('max_pairwise_similarity')}, "
            f"clusters={metrics.get('cluster_count')}, intents={metrics.get('intent_type_count')}  \n"
        )
        lines.append(f"- Gate: **{'PASS' if dr.get('gate_passed') else 'FAIL'}**\n\n")

        for i, d in enumerate(d2_dirs, start=1):
            lines.append(
                f"{i}. **{d.get('title','').strip()}**  \n"
                f"   - keyword: `{d.get('primary_keyword','')}`  \n"
                f"   - intent: `{d.get('intent_type','')}`  \n"
                f"   - strategy: `{d.get('strategy_source')}`  \n"
                f"   - cluster: `{d.get('cluster_id')}`  \n"
                f"   - SEO/AEO: {float(d.get('seo_score') or 0):.0f} / {float(d.get('aeo_score') or 0):.0f}  \n"
                f"   - volume: {float(d.get('volume') or 0):.0f}\n"
            )
        lines.append("\n")

        lines.append("### 备注 / 风险\n\n")
        for note in (uc.get("notes") or []):
            lines.append(f"- {note}\n")
        lines.append("\n---\n\n")

    lines.append("## 总结结论（当前数据条件下）\n\n")
    lines.append("- 这份报告验证了：在**无需新增外部依赖**的情况下，D2 的“聚类去重 + 多样性门禁 + 组合约束”可以被工程化执行，并能输出可审计的指标。\n")
    lines.append("- 但由于本次相似度使用的是 **TF-IDF 词面 cosine**（不是 embedding 语义 cosine），以及部分用例候选池/需求数据不足（例如 UC3 volume=0），结论更适合作为“机制可行性”验证。\n")
    lines.append("- 下一步建议：在可联网环境中用真实的 Seed D1/D2 执行产物（含 `03-diversity-report.json` 与 DataForSEO）重跑同样的三用例，替换本报告中的 offline proxy。\n")

    md_path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    uc1 = build_uc1()
    uc2 = build_uc2()
    uc3 = build_uc3()
    write_outputs([uc1, uc2, uc3])
    print(f"Wrote report to: {OUT_DIR}")


if __name__ == "__main__":
    main()

