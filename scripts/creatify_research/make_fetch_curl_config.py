#!/usr/bin/env python3
from __future__ import annotations

import argparse
import urllib.parse
from pathlib import Path


def read_tsv(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        rows.append(line.split("\t"))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, help="Path to creatify-ai/data")
    ap.add_argument("--out", required=True, help="Output curl config file")
    ap.add_argument("--max-serp", type=int, default=200)
    ap.add_argument("--max-wayback", type=int, default=200)
    ap.add_argument(
        "--user-agent",
        default=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
    )
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_path = Path(args.out)
    serp_tsv = data_dir / "serp_fetch_plan.tsv"
    wb_tsv = data_dir / "wayback_fetch_plan.tsv"

    serp_rows = read_tsv(serp_tsv)[: args.max_serp]
    wb_rows = read_tsv(wb_tsv)[: args.max_wayback]

    lines: list[str] = []
    # Global defaults
    lines.extend(
        [
            "silent",
            "show-error",
            "location",
            "ipv4",
            "retry = 12",
            "retry-all-errors",
            "retry-delay = 1",
            "connect-timeout = 8",
            "max-time = 45",
            f'user-agent = "{args.user_agent}"',
            "",
        ]
    )

    blocks: list[list[str]] = []

    # SERP snapshots (DDG Lite, first page only)
    for row in serp_rows:
        if len(row) < 2:
            continue
        qhash, query = row[0].strip(), row[1].strip()
        if not qhash or not query:
            continue
        out_file = data_dir / "serp_snapshots" / f"serp_{qhash}.html"
        post = urllib.parse.urlencode({"q": query})
        blocks.append(
            [
                'url = "https://lite.duckduckgo.com/lite/"',
                'header = "Content-Type: application/x-www-form-urlencoded"',
                f'data = "{post}"',
                f'output = "{out_file}"',
            ]
        )

    # Wayback snapshots
    for row in wb_rows:
        if len(row) < 3:
            continue
        uhash, url, ts = row[0].strip(), row[1].strip(), row[2].strip()
        if not uhash or not url or not ts or len(ts) != 14 or not ts.isdigit():
            continue
        out_file = data_dir / "wayback_cache" / f"wayback_{uhash}.html"
        snap = f"https://web.archive.org/web/{ts}id_/{url}"
        blocks.append(
            [
                f'url = "{snap}"',
                f'output = "{out_file}"',
            ]
        )

    for i, b in enumerate(blocks):
        lines.extend(b)
        if i != len(blocks) - 1:
            lines.extend(["--next", ""])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
