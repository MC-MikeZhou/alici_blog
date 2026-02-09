#!/bin/zsh
set -euo pipefail

# Fetch step for Virvid AEO Incrementality pack.
#
# Why this exists:
# - In this Codex environment, Python network/DNS calls to DataForSEO can be unreliable.
# - Direct `curl` from the shell is more reliable here.
#
# This script:
# - reads queries from `research 竞品分析/virvid-ai/aeo-incremental/data/query_universe.csv`
# - fetches SERP advanced + keyword volumes via DataForSEO REST API (batch mode)
# - saves raw JSON responses under `.../data/raw/` for offline build by:
#   `./.venv/bin/python scripts/virvid_aeo_incremental.py run --offline-build`
#
# It does NOT print credentials.

ROOT="${ROOT:-research 竞品分析/virvid-ai}"
OUT_DIR="${OUT_DIR:-${ROOT}/aeo-incremental}"
CONFIG="${CONFIG:-${OUT_DIR}/config.yaml}"
MCP_JSON="${MCP_JSON:-.mcp.json}"
MAX_QUERIES="${MAX_QUERIES:-}"
REFRESH="${REFRESH:-0}"
USER_AGENT="Mozilla/5.0 (compatible; AliciBlogResearchBot/1.0; +https://alici.ai)"

usage() {
  cat <<'EOF'
Usage:
  scripts/virvid_aeo_incremental_fetch.sh [--max-queries N] [--refresh]

Env vars (optional):
  ROOT, OUT_DIR, CONFIG, MCP_JSON, MAX_QUERIES, REFRESH

Examples:
  MAX_QUERIES=60 scripts/virvid_aeo_incremental_fetch.sh
  scripts/virvid_aeo_incremental_fetch.sh --max-queries 300 --refresh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-queries)
      MAX_QUERIES="${2:-}"
      shift 2
      ;;
    --refresh)
      REFRESH=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

QUERY_CSV="${OUT_DIR}/data/query_universe.csv"
if [[ ! -f "$QUERY_CSV" ]]; then
  echo "Missing $QUERY_CSV. Run:" >&2
  echo "  ./.venv/bin/python scripts/virvid_aeo_incremental.py run --skip-serp --skip-volumes" >&2
  exit 1
fi

AUTH_B64="$(
  python3 - <<'PY' "$MCP_JSON"
import base64, json, sys
p = sys.argv[1]
m = json.load(open(p, encoding="utf-8"))
env = m.get("mcpServers", {}).get("dataforseo", {}).get("env", {})
u = (env.get("DATAFORSEO_USERNAME") or "").strip()
pw = (env.get("DATAFORSEO_PASSWORD") or "").strip()
if not u or not pw:
    raise SystemExit("Missing DataForSEO creds in .mcp.json")
print(base64.b64encode(f"{u}:{pw}".encode("utf-8")).decode("ascii"))
PY
)"

read -r LOCATION_CODE LANGUAGE_CODE DEVICE OS <<EOF
$(python3 - <<'PY' "$CONFIG"
import sys, re
p = sys.argv[1]
txt = open(p, encoding="utf-8", errors="replace").read().splitlines()
def get_scalar(key, default):
    for line in txt:
        if line.strip().startswith("#"):
            continue
        m = re.match(rf"^\s*{re.escape(key)}\s*:\s*(.+)\s*$", line)
        if m:
            return m.group(1).strip()
    return default
print(get_scalar("location_code","2840"), get_scalar("language_code","en"), get_scalar("device","desktop"), get_scalar("os","windows"))
PY
)
EOF

RAW_SERP_DIR="${OUT_DIR}/data/raw/dataforseo_serp_batches"
RAW_VOL_DIR="${OUT_DIR}/data/raw/dataforseo_keywords_data"
mkdir -p "$RAW_SERP_DIR" "$RAW_VOL_DIR"

echo "[fetch] OUT_DIR=$OUT_DIR"
echo "[fetch] location=$LOCATION_CODE lang=$LANGUAGE_CODE device=$DEVICE os=$OS"

QUERIES_JSON="$(
  python3 - <<'PY' "$QUERY_CSV" "$MAX_QUERIES"
import csv, json, sys
p = sys.argv[1]
max_q = sys.argv[2].strip()
max_n = int(max_q) if max_q else None
rows = list(csv.DictReader(open(p, encoding="utf-8")))
qs = [r["query"] for r in rows if r.get("query")]
if max_n is not None:
    qs = qs[:max_n]
print(json.dumps(qs))
PY
)"

SERP_BATCH_SIZE=1
VOL_BATCH_SIZE=100

TMP_DIR="$(mktemp -d /tmp/virvid_aeo_fetch.XXXXXX)"
QUERIES_TXT="${TMP_DIR}/queries.txt"

python3 - <<'PY' "$QUERIES_JSON" "$QUERIES_TXT"
import json, sys
qs = json.loads(sys.argv[1])
out = sys.argv[2]
with open(out, "w", encoding="utf-8") as f:
    for q in qs:
        f.write(str(q).strip() + "\n")
PY

TOTAL="$(wc -l < "$QUERIES_TXT" | tr -d ' ')"
echo "[fetch] queries=$TOTAL"

SERP_URL="https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
VOL_URL="https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"

make_serp_payload() {
  local query="$1"
  local out="$2"
  python3 - <<'PY' "$query" "$LOCATION_CODE" "$LANGUAGE_CODE" "$DEVICE" "$OS" "$out"
import sys, json
q = sys.argv[1]
loc = int(sys.argv[2])
lang = sys.argv[3]
device = sys.argv[4]
os_name = sys.argv[5]
out = sys.argv[6]
payload = [{
    "keyword": q,
    "location_code": loc,
    "language_code": lang,
    "device": device,
    "os": os_name,
    "depth": 100,
}]
open(out, "w", encoding="utf-8").write(json.dumps(payload))
PY
}

make_vol_payload() {
  local start="$1"
  local count="$2"
  local out="$3"
  python3 - <<'PY' "$QUERIES_TXT" "$start" "$count" "$LOCATION_CODE" "$LANGUAGE_CODE" "$out"
import sys, json
path = sys.argv[1]
start = int(sys.argv[2])
count = int(sys.argv[3])
loc = int(sys.argv[4])
lang = sys.argv[5]
out = sys.argv[6]
qs = [l.strip() for l in open(path, encoding="utf-8") if l.strip()]
batch = qs[start:start+count]
payload = [{
    "keywords": batch,
    "location_code": loc,
    "language_code": lang,
    "search_partners": False,
}]
open(out, "w", encoding="utf-8").write(json.dumps(payload))
PY
}

hash_file() {
  python3 - <<'PY' "$1"
import hashlib, sys
print(hashlib.sha1(open(sys.argv[1],"rb").read()).hexdigest())
PY
}

serp_cache_path_for_query() {
  python3 - <<'PY' "$1" "$LOCATION_CODE" "$LANGUAGE_CODE" "$DEVICE" "$OS" "$OUT_DIR"
import hashlib, json, re, sys
q = sys.argv[1]
cfg = {
    "query": q,
    "location_code": int(sys.argv[2]),
    "language_code": sys.argv[3],
    "device": sys.argv[4],
    "os": sys.argv[5],
}
out_dir = sys.argv[6]
def slugify(s: str, max_len: int = 80) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-") or "x"
    return s[:max_len]
key = json.dumps(cfg, sort_keys=True)
h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
name = f"{slugify(q)}__{h}.json"
print(f"{out_dir}/data/raw/dataforseo_serp/{name}")
PY
}

is_serp_ok() {
  local file="$1"
  python3 - <<'PY' "$file" >/dev/null 2>&1
import json, sys
p=sys.argv[1]
try:
    r=json.load(open(p,encoding="utf-8"))
except Exception:
    raise SystemExit(1)
if r.get("status_code")!=20000:
    raise SystemExit(1)
tasks=r.get("tasks") or []
if not isinstance(tasks,list) or not tasks:
    raise SystemExit(1)
if (tasks[0] or {}).get("status_code")!=20000:
    raise SystemExit(1)
raise SystemExit(0)
PY
}

echo "[fetch] SERP batches..."
idx=1
while [[ "$idx" -le "$TOTAL" ]]; do
  q="$(sed -n "${idx}p" "$QUERIES_TXT" | tr -d '\r')"
  payload="${TMP_DIR}/serp_payload_${idx}.json"
  make_serp_payload "$q" "$payload"
  out="$(serp_cache_path_for_query "$q")"
  mkdir -p "$(dirname "$out")"
  if [[ -f "$out" && "$REFRESH" -eq 0 ]]; then
    if is_serp_ok "$out"; then
      idx=$(( idx + 1 ))
      continue
    fi
  fi
  curl -sS --retry 8 --retry-all-errors --retry-delay 1 \
    --connect-timeout 20 --max-time 180 \
    -X POST "$SERP_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic ${AUTH_B64}" \
    -H "User-Agent: ${USER_AGENT}" \
    --data-binary "@${payload}" \
    -o "$out"
  if (( idx % 25 == 0 )); then
    echo "[fetch] SERP progress: ${idx}/${TOTAL}"
  fi
  idx=$(( idx + 1 ))
  sleep 0.15
done

echo "[fetch] Keyword volumes..."
start=0
while [[ "$start" -lt "$TOTAL" ]]; do
  payload="${TMP_DIR}/vol_payload_${start}.json"
  make_vol_payload "$start" "$VOL_BATCH_SIZE" "$payload"
  h="$(hash_file "$payload")"
  out="${RAW_VOL_DIR}/keyword_volumes__${h:0:12}.json"
  if [[ -f "$out" && "$REFRESH" -eq 0 ]]; then
    start=$(( start + VOL_BATCH_SIZE ))
    continue
  fi
  curl -sS --retry 8 --retry-all-errors --retry-delay 1 \
    --connect-timeout 20 --max-time 180 \
    -X POST "$VOL_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic ${AUTH_B64}" \
    -H "User-Agent: ${USER_AGENT}" \
    --data-binary "@${payload}" \
    -o "$out"
  start=$(( start + VOL_BATCH_SIZE ))
  sleep 0.2
done

rm -rf "$TMP_DIR"

echo "[fetch] done. Now build offline:"
echo "  ./.venv/bin/python scripts/virvid_aeo_incremental.py run --offline-build"
