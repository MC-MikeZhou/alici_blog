#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/research 竞品分析/creatify-ai"
DATA_DIR="${OUT_DIR}/data"
SERP_DIR="${DATA_DIR}/serp_snapshots"
WAYBACK_DIR="${DATA_DIR}/wayback_cache"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

mkdir -p "${DATA_DIR}" "${SERP_DIR}" "${WAYBACK_DIR}"

CURL_BASE=(curl -4 -sS -L --retry 25 --retry-all-errors --retry-delay 1 --connect-timeout 8 --max-time 40 -A "${UA}")

fetch_cdx () {
  local hostpath="$1"   # e.g. creatify.ai/blog/
  local sort="$2"       # asc|desc
  local out="$3"

  local url="https://web.archive.org/cdx/search/cdx?url=${hostpath}&matchType=prefix&output=json&fl=timestamp,original&filter=statuscode:200&collapse=urlkey&from=2020&to=2026&limit=8000&sort=${sort}"
  echo "[CDX] ${hostpath} (${sort}) -> ${out}"
  "${CURL_BASE[@]}" "${url}" -o "${out}"
}

fetch_cdx "creatify.ai/blog/" "asc"  "${DATA_DIR}/wayback_cdx_creatify_ai_blog_asc.json"
fetch_cdx "creatify.ai/blog/" "desc" "${DATA_DIR}/wayback_cdx_creatify_ai_blog_desc.json"
fetch_cdx "www.creatify.ai/blog/" "asc"  "${DATA_DIR}/wayback_cdx_www_creatify_ai_blog_asc.json"
fetch_cdx "www.creatify.ai/blog/" "desc" "${DATA_DIR}/wayback_cdx_www_creatify_ai_blog_desc.json"

echo "[PREPARE] inventory + fetch plans"
python3 "${ROOT_DIR}/scripts/creatify_research/top10_seo_aeo.py" prepare

echo "[SERP] fetching DuckDuckGo Lite snapshots"
SERP_PLAN="${DATA_DIR}/serp_fetch_plan.tsv"
if [[ ! -f "${SERP_PLAN}" ]]; then
  echo "Missing ${SERP_PLAN}; prepare step failed." >&2
  exit 2
fi

while IFS=$'\\t' read -r qhash query; do
  [[ -z "${qhash}" || -z "${query}" ]] && continue
  out="${SERP_DIR}/serp_${qhash}.html"
  if [[ -s "${out}" ]]; then
    continue
  fi
  tmpdir="$(mktemp -d)"
  p1="${tmpdir}/p1.html"

  "${CURL_BASE[@]}" -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "q=${query}" \
    "https://lite.duckduckgo.com/lite/" \
    -o "${p1}"

  cat "${p1}" > "${out}"

  # Aim for ~Top 50 (DDG lite is usually 10 results/page).
  for i in 2 3 4 5; do
    prev="${tmpdir}/p$((i-1)).html"
    post="$(python3 "${ROOT_DIR}/scripts/creatify_research/ddg_lite_extract_next.py" "${prev}")"
    if [[ -z "${post}" ]]; then
      break
    fi
    pi="${tmpdir}/p${i}.html"
    "${CURL_BASE[@]}" -H "Content-Type: application/x-www-form-urlencoded" \
      --data-raw "${post}" \
      "https://lite.duckduckgo.com/lite/" \
      -o "${pi}"
    printf "\\n\\n<!--PAGE-->\\n\\n" >> "${out}"
    cat "${pi}" >> "${out}"
    sleep 0.5
  done

  rm -rf "${tmpdir}"
  sleep 0.3
done < "${SERP_PLAN}"

echo "[WAYBACK] fetching cached HTML snapshots"
WB_PLAN="${DATA_DIR}/wayback_fetch_plan.tsv"
if [[ ! -f "${WB_PLAN}" ]]; then
  echo "Missing ${WB_PLAN}; prepare step failed." >&2
  exit 2
fi

while IFS=$'\\t' read -r uhash url ts; do
  [[ -z "${uhash}" || -z "${url}" || -z "${ts}" ]] && continue
  out="${WAYBACK_DIR}/wayback_${uhash}.html"
  if [[ -s "${out}" ]]; then
    continue
  fi
  snap="https://web.archive.org/web/${ts}id_/${url}"
  "${CURL_BASE[@]}" "${snap}" -o "${out}"
  sleep 0.4
done < "${WB_PLAN}"

echo "[SCORE] build Top10 report"
python3 "${ROOT_DIR}/scripts/creatify_research/top10_seo_aeo.py" score

echo "OK: ${OUT_DIR}/04-top10-seo-aeo.md"
