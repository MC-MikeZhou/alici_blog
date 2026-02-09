#!/usr/bin/env python3
"""
Map art-scout directions -> Basecamp todos (context pack).

Inputs:
- context.json produced by scripts/basecamp_pull_todolist.py
- directions.json (03-team-directions.json style)

Output:
- mapping.json with matched_todos per direction (with confidence + rationale)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORD_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text("utf-8"))


def write_json(path: str, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tokenize_ascii(text: str) -> set[str]:
    return {m.group(0).lower() for m in WORD_RE.finditer(text or "")}


def char_bigrams(text: str) -> set[str]:
    s = re.sub(r"\s+", "", text or "")
    if len(s) < 2:
        return set()
    return {s[i : i + 2] for i in range(len(s) - 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def score_match(direction_text: str, todo_text: str) -> tuple[float, str]:
    d_ascii = tokenize_ascii(direction_text)
    t_ascii = tokenize_ascii(todo_text)
    ascii_sim = jaccard(d_ascii, t_ascii)

    d_bg = char_bigrams(direction_text)
    t_bg = char_bigrams(todo_text)
    bg_sim = jaccard(d_bg, t_bg)

    # keyword boosts (hand-tuned for this domain)
    boosts = 0.0
    boost_hits: list[str] = []
    keywords = [
        "invideo",
        "landing",
        "落地页",
        "use case",
        "案例",
        "creative center",
        "创意中心",
        "demo",
        "模板",
        "prompt",
        "pricing",
        "单价",
        "tiktok",
        "instagram",
        "youtube",
        "veo",
        "kling",
        "seedance",
        "opus",
    ]
    low_d = (direction_text or "").lower()
    low_t = (todo_text or "").lower()
    for k in keywords:
        if k in low_d and (k in low_t or k.replace(" ", "") in low_t):
            boosts += 0.08
            boost_hits.append(k)

    # weighted blend; clamp
    raw = 0.55 * bg_sim + 0.35 * ascii_sim + boosts
    score = max(0.0, min(1.0, raw))
    rationale = f"bg={bg_sim:.2f}, ascii={ascii_sim:.2f}, boosts={boosts:.2f}"
    if boost_hits:
        rationale += f", hits={','.join(sorted(set(boost_hits)))}"
    return score, rationale


def build_direction_text(d: dict[str, Any]) -> str:
    parts: list[str] = []
    for k in ("direction_id", "angle_cn", "angle_en", "summary_cn", "summary_en"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
    titles = d.get("english_titles")
    if isinstance(titles, list):
        for t in titles:
            if isinstance(t, str) and t.strip():
                parts.append(t.strip())
    tags = d.get("tags")
    if isinstance(tags, list):
        parts.extend(str(x) for x in tags if isinstance(x, str))
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Map directions.json to Basecamp todos using a context pack.")
    parser.add_argument("--context", required=True, help="Path to 02-basecamp-normalized/context.json")
    parser.add_argument("--directions", required=True, help="Path to 03-team-directions.json")
    parser.add_argument("--out", required=True, help="Output mapping JSON path")
    parser.add_argument("--min-confidence", type=float, default=0.60, help="Minimum confidence threshold (default: 0.60)")
    parser.add_argument("--top-k", type=int, default=6, help="Max todos per direction (default: 6)")
    args = parser.parse_args(argv)

    context = load_json(args.context)
    directions_doc = load_json(args.directions)

    todos = list(context.get("todos") or [])
    todos_by_id: dict[int, dict[str, Any]] = {}
    for t in todos:
        if isinstance(t, dict) and isinstance(t.get("id"), int):
            todos_by_id[int(t["id"])] = t
    directions = list(directions_doc.get("directions") or [])
    if not directions:
        # tolerate nested schema: {portfolio:{directions:[...]}}
        portfolio = directions_doc.get("portfolio")
        if isinstance(portfolio, dict):
            directions = list(portfolio.get("directions") or [])

    out_rows = []
    for d in directions:
        if not isinstance(d, dict):
            continue
        did = d.get("direction_id") or d.get("id")
        dtext = build_direction_text(d)
        scored = []

        # 1) Pinned matches from directions.json (explicit trace).
        pinned: list[dict[str, Any]] = []
        pinned_set: set[int] = set()
        trace = d.get("basecamp_trace")
        if isinstance(trace, dict) and isinstance(trace.get("todo_ids"), list):
            for tid in trace.get("todo_ids"):
                if not isinstance(tid, int):
                    continue
                t = todos_by_id.get(int(tid))
                if not t:
                    continue
                pinned_set.add(int(tid))
                pinned.append(
                    {
                        "todo_id": t.get("id"),
                        "list_id": t.get("list_id"),
                        "status": t.get("status"),
                        "content": t.get("content"),
                        "confidence": 1.0,
                        "rationale": "pinned_from_basecamp_trace",
                        "app_url": t.get("app_url") or "",
                        "url": t.get("url") or "",
                    }
                )
        for t in todos:
            if not isinstance(t, dict):
                continue
            content = (t.get("content") or "").strip()
            if not content:
                continue
            if isinstance(t.get("id"), int) and int(t["id"]) in pinned_set:
                continue
            score, rationale = score_match(dtext, content)
            scored.append((score, rationale, t))
        scored.sort(key=lambda x: x[0], reverse=True)

        matched = []
        matched.extend(pinned)
        for score, rationale, t in scored[: max(1, int(args.top_k))]:
            if score < float(args.min_confidence):
                continue
            matched.append(
                {
                    "todo_id": t.get("id"),
                    "list_id": t.get("list_id"),
                    "status": t.get("status"),
                    "content": t.get("content"),
                    "confidence": round(float(score), 4),
                    "rationale": rationale,
                    "app_url": t.get("app_url") or "",
                    "url": t.get("url") or "",
                }
            )

        out_rows.append(
            {
                "direction_id": did,
                "matched_todos": matched,
            }
        )

    mapping = {
        "generated_at": context.get("generated_at"),
        "context_sources": context.get("sources"),
        "direction_count": len(out_rows),
        "min_confidence": float(args.min_confidence),
        "items": out_rows,
    }

    write_json(args.out, mapping)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
