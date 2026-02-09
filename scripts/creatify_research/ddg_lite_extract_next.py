#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import sys
import urllib.parse
from pathlib import Path


def extract_next_fields(html_text: str) -> dict | None:
    m = re.search(r'(?is)<form[^>]+class="next_form"[^>]*>(.*?)</form>', html_text or "")
    if not m:
        return None
    form = m.group(1)
    fields: dict[str, str] = {}
    for im in re.finditer(r'(?is)<input[^>]+type="hidden"[^>]+name="([^"]+)"[^>]+value="([^"]*)"', form):
        fields[html.unescape(im.group(1))] = html.unescape(im.group(2))
    if not fields.get("q"):
        return None
    return fields


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ddg_lite_extract_next.py <html_file>", file=sys.stderr)
        raise SystemExit(2)
    p = Path(sys.argv[1])
    text = p.read_text(encoding="utf-8", errors="ignore")
    fields = extract_next_fields(text)
    if not fields:
        print("")
        return
    print(urllib.parse.urlencode(fields))


if __name__ == "__main__":
    main()

