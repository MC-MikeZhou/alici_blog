#!/usr/bin/env bash
set -euo pipefail

# Requirements:
# - FAL_API_KEY set or present in .mcp.json (mcpServers.fal.env.FAL_API_KEY)
# - deps: curl, jq
# Aligns with AGENTS.md: FAL.ai nano-banana via queue API

QUEUE_ENDPOINT="https://queue.fal.run/fal-ai/nano-banana"
OUT_DIR="reports 待发文章/2026-01-28-thumbnail-design-2025"
PLAN="$OUT_DIR/asset_plan.json"
MANIFEST="$OUT_DIR/asset_manifest.json"

# Resolve API key: env var first, then .mcp.json
if [[ -z "${FAL_API_KEY:-}" ]]; then
  if [[ -f ".mcp.json" ]]; then
    FAL_API_KEY=$(jq -r '.mcpServers.fal.env.FAL_API_KEY // empty' .mcp.json)
  else
    FAL_API_KEY=""
  fi
fi

if [[ -z "${FAL_API_KEY:-}" ]]; then
  echo "FAL_API_KEY is not set. Configure it in environment or .mcp.json." >&2
  exit 1
fi

# Ensure manifest file exists
if [[ ! -f "$MANIFEST" ]]; then
  echo '{"images":[]}' > "$MANIFEST"
fi

generate_one() {
  local id="$1"
  local prompt="$2"

  echo "Generating $id via FAL queue..." >&2

  # Submit to queue
  local submit_resp
  submit_resp=$(curl -sS -X POST "$QUEUE_ENDPOINT" \
    -H "Authorization: Key $FAL_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"$prompt\", \"aspect_ratio\": \"16:9\", \"resolution\": \"2K\"}")

  echo "$submit_resp" | jq '.' > "$OUT_DIR/${id}_submit.json"
  local req_id
  req_id=$(echo "$submit_resp" | jq -r '.request_id // empty')
  if [[ -z "$req_id" ]]; then
    echo "❌ No request_id returned for $id" >&2
    return 1
  fi

  # Polling
  local status_url="$QUEUE_ENDPOINT/requests/$req_id/status"
  local tries=0
  local max_tries=30
  local status="queued"
  local response_url=""
  while (( tries < max_tries )); do
    sleep 5
    tries=$((tries+1))
    local st
    st=$(curl -sS -H "Authorization: Key $FAL_API_KEY" "$status_url")
    echo "$st" | jq '.' > "$OUT_DIR/${id}_status.json"
    status=$(echo "$st" | jq -r '(.status // "unknown") | ascii_downcase')
    if [[ "$status" == "completed" ]]; then
      response_url=$(echo "$st" | jq -r '.response_url // empty')
      break
    elif [[ "$status" == "failed" ]]; then
      echo "❌ Generation failed for $id" >&2
      return 1
    fi
  done

  if [[ -z "$response_url" ]]; then
    echo "❌ No response_url for $id after polling" >&2
    return 1
  fi

  # Fetch final result
  local final
  final=$(curl -sS -H "Authorization: Key $FAL_API_KEY" "$response_url")
  echo "$final" | jq '.' > "$OUT_DIR/${id}_final.json"
  local url
  url=$(echo "$final" | jq -r '.images[0].url // .image.url // .image // empty')
  if [[ -z "$url" ]]; then
    echo "❌ Could not extract image URL for $id" >&2
    return 1
  fi

  # Update manifest
  local tmp
  tmp=$(mktemp)
  jq --arg id "$id" --arg url "$url" \
     '.images += [{id: $id, cdn_url: $url, status: "success", generation_model: "fal-ai/nano-banana", file_path: null}]' \
     "$MANIFEST" > "$tmp" && mv "$tmp" "$MANIFEST"

  echo "✅ $id -> $url" >&2
}

# Iterate covers from plan
while IFS=$'\t' read -r ID PROMPT; do
  generate_one "$ID" "$PROMPT" || {
    tmp=$(mktemp)
    jq --arg id "$ID" \
       '.images += [{id: $id, cdn_url: null, status: "failed", generation_model: "fal-ai/nano-banana", file_path: null}]' \
       "$MANIFEST" > "$tmp" && mv "$tmp" "$MANIFEST"
  }
done < <(jq -r '.images[] | select(.id | test("^blog-cover-0[12]$")) | [.id, .prompt] | @tsv' "$PLAN")

echo "Manifest written: $MANIFEST" >&2
