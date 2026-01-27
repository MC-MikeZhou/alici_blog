#!/usr/bin/env python3
import csv
import html
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from typing import List, Dict, Tuple

SITEMAP_URL = "https://invideo.io/sitemap-en-blog.xml"
USER_AGENT = "Mozilla/5.0 (compatible; AliciBlogScaleDemo/1.0)"
INTRO_CHAR_LIMIT = 600
MAX_PAGES = 60  # fetch extra to allow filtering to 50
OUTPUT_JSONL = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-harvest.jsonl"
OUTPUT_CSV = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-harvest.csv"
OUTPUT_LOG = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-harvest.log"

STOPWORDS = set(
    "a an the and or but if then else when while of for to in on at by with from into over after before".split()
    + "is are was were be been being this that these those it its as not no yes you your we our they their".split()
    + "how best top vs vs. versus guide tips tricks statistics report reports".split()
)

class SimpleHTMLTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h2 = False
        self.in_h3 = False
        self.in_p = False
        self.title = ""
        self.h2 = []
        self.h3 = []
        self.paragraphs = []
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "h2":
            self.in_h2 = True
        elif tag == "h3":
            self.in_h3 = True
        elif tag == "p":
            self.in_p = True
        elif tag in {"script", "style"}:
            self._buffer = []

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h2":
            self.in_h2 = False
        elif tag == "h3":
            self.in_h3 = False
        elif tag == "p":
            self.in_p = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title += (" " + text)
        elif self.in_h2:
            self.h2.append(text)
        elif self.in_h3:
            self.h3.append(text)
        elif self.in_p:
            self.paragraphs.append(text)


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_sitemap(xml: str) -> List[Tuple[str, str]]:
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", xml)
    # fallback if counts mismatch
    pairs = []
    if len(locs) == len(lastmods):
        for u, lm in zip(locs, lastmods):
            pairs.append((u, lm))
    else:
        for u in locs:
            pairs.append((u, ""))
    return pairs


def clean_text(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def guess_content_type(title: str) -> str:
    t = title.lower()
    if " vs " in t or " versus " in t:
        # showdown if multiple vs
        if t.count(" vs ") + t.count(" versus ") >= 2:
            return "comparison"  # treat showdown as comparison for now
        return "comparison"
    if "alternatives" in t:
        return "alternatives"
    if "statistics" in t or " stats" in t:
        return "statistics"
    if "how to" in t:
        return "how_to"
    if re.search(r"\b\d+\b", t) and ("best" in t or "top" in t):
        return "listicle"
    if "guide" in t:
        return "guide"
    if "trends" in t:
        return "trends"
    return "other"


def guess_intent(content_type: str) -> str:
    if content_type in {"statistics", "trends"}:
        return "awareness"
    if content_type in {"guide", "how_to", "other"}:
        return "interest"
    if content_type in {"listicle", "alternatives"}:
        return "consideration"
    if content_type in {"comparison"}:
        return "decision"
    return "interest"


def extract_keywords(text: str, limit: int = 10) -> List[str]:
    words = re.findall(r"[A-Za-z0-9\-]+", text.lower())
    words = [w for w in words if len(w) > 3 and w not in STOPWORDS]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    # sort by freq then length
    ranked = sorted(freq.items(), key=lambda x: (-x[1], -len(x[0])))
    return [w for w, _ in ranked[:limit]]


def needs_refresh(title: str) -> bool:
    years = re.findall(r"\b(20\d{2})\b", title)
    if not years:
        return False
    # refresh if not 2026
    return any(y != "2026" for y in years)


def build_intro(paragraphs: List[str]) -> str:
    text = clean_text(" ".join(paragraphs))
    if len(text) <= INTRO_CHAR_LIMIT:
        return text
    return text[:INTRO_CHAR_LIMIT].rstrip()


def main():
    max_pages = MAX_PAGES
    if len(sys.argv) > 1:
        try:
            max_pages = int(sys.argv[1])
        except ValueError:
            pass
    log_lines = []
    try:
        sitemap_xml = fetch_url(SITEMAP_URL)
    except Exception as e:
        print(f"ERROR fetching sitemap: {e}")
        return 1
    pairs = parse_sitemap(sitemap_xml)
    urls = [u for u, _ in pairs if "/blog/" in u]
    # de-dup and keep order
    seen = set()
    dedup_urls = []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        dedup_urls.append(u)
    target_urls = dedup_urls[:max_pages]

    records = []
    for idx, url in enumerate(target_urls, 1):
        try:
            html_doc = fetch_url(url)
        except Exception as e:
            log_lines.append(f"FAIL {url} {e}")
            continue
        parser = SimpleHTMLTextParser()
        parser.feed(html_doc)
        title = clean_text(parser.title) or ""
        if not title:
            # fallback to og:title
            m = re.search(r"property=\"og:title\" content=\"(.*?)\"", html_doc)
            if m:
                title = clean_text(m.group(1))
        # publish date (meta)
        pub_date = ""
        m = re.search(r"property=\"article:published_time\" content=\"(.*?)\"", html_doc)
        if m:
            pub_date = m.group(1)[:10]
        # toc from h2/h3
        toc = [clean_text(h) for h in parser.h2][:20]
        if not toc:
            toc = [clean_text(h) for h in parser.h3][:20]
        intro = build_intro(parser.paragraphs)
        if not intro:
            log_lines.append(f"NO_INTRO {url}")
            continue

        content_type = guess_content_type(title)
        intent = guess_intent(content_type)
        keywords = extract_keywords(" ".join([title] + toc + [intro]), limit=10)

        record = {
            "source": "invideo_blog",
            "url": url,
            "title": title,
            "publish_date": pub_date,
            "toc": toc,
            "intro": intro,
            "content_type_guess": content_type,
            "intent_guess": intent,
            "keyword_seed": keywords,
            "needs_refresh": needs_refresh(title),
            "notes": ""
        }
        records.append(record)
        time.sleep(0.1)

    # write outputs
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "source","url","title","publish_date","content_type_guess","intent_guess",
            "needs_refresh","keyword_seed","toc","intro","notes"
        ])
        for r in records:
            writer.writerow([
                r["source"], r["url"], r["title"], r["publish_date"], r["content_type_guess"],
                r["intent_guess"], r["needs_refresh"], "|".join(r["keyword_seed"]),
                "|".join(r["toc"]), r["intro"], r["notes"]
            ])

    with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print(f"records={len(records)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
