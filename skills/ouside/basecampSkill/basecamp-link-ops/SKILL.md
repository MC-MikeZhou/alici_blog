---
name: basecamp-link-ops
description: Read and write Basecamp 4 content from shared links with OAuth. Use when a user provides a Basecamp URL and asks to fetch/list/analyze docs, todolists, todos, related items, or create/update todos in a specific list. This skill is self-contained and must not depend on local project scripts or screenshots.
---

# Basecamp Link Ops

## Overview

Use this skill to operate Basecamp links directly via Basecamp API.

## Preconditions

1. Require user-provided `client_id` and `client_secret` from their Basecamp integration.
2. Require OAuth access token in env:
- `BC_ACCESS_TOKEN`
3. Require valid user agent in env:
- `BC_USER_AGENT` (example: `MyBasecampTool (name@example.com)`)
4. Never require any project-local file, screenshot, or absolute path.
5. Use bundled helper script for non-developer OAuth flow:
- `scripts/oauth_easy.py`

## URL-to-API Mapping

Map app links like:
- `https://3.basecamp.com/<account>/buckets/<bucket>/todolists/<id>`
- `https://3.basecamp.com/<account>/buckets/<bucket>/documents/<id>`
- `https://3.basecamp.com/<account>/buckets/<bucket>/vaults/<id>`

to API host `https://3.basecampapi.com/<account>/...` and append `.json` for JSON endpoints.

## OAuth Setup (No DevTools Required)

Recommended (auto-capture code via localhost callback):

```bash
python3 scripts/oauth_easy.py --env-file ".env.basecamp"
```

or provide values directly:

```bash
python3 scripts/oauth_easy.py \
  --client-id "<CLIENT_ID>" \
  --client-secret "<CLIENT_SECRET>" \
  --env-file ".env.basecamp"
```

What users do:
1. Run command.
2. Browser opens authorization page.
3. Click `Yes, I'll allow access`.
4. Done. Script captures code automatically and stores token to `.env.basecamp`.

Fallback (manual code flow) is allowed only when localhost callback is unavailable.

## Read Workflow

1. Parse `account`, `bucket`, resource type, and id from provided app URL.
2. Resolve primary API URL and fetch JSON.
3. Follow embedded related API URLs when user asks for deep context.
4. When user asks for all article titles under folder hierarchy:
- read current vault `documents.json`
- read current vault `vaults.json`
- recurse child vaults until no child vault
- output only document titles (exclude folder names)
5. For todolist tasks, read:
- `/buckets/<bucket>/todolists/<id>.json`
- `/buckets/<bucket>/todolists/<id>/todos.json`

## Write Workflow (Todo)

Create todo:

```bash
curl -sS \
  -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
  -H "User-Agent: ${BC_USER_AGENT}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"content":"<todo content>"}' \
  "https://3.basecampapi.com/<account>/buckets/<bucket>/todolists/<todolist_id>/todos.json"
```

Then verify by `GET /buckets/<bucket>/todos/<todo_id>.json`.

Minimal verify:

```bash
curl -sS \
  -H "Authorization: Bearer $BC_ACCESS_TOKEN" \
  -H "User-Agent: ${BC_USER_AGENT}" \
  "https://3.basecampapi.com/<account>/buckets/<bucket>/todos/<todo_id>.json"
```

## Attachment Caveat

When parsing rich text (`content`) with `<bc-attachment>`:
1. Prefer metadata extraction (filename, type, links) from document content.
2. Treat direct storage/preview links as potentially expired.
3. If download fails, report clearly that attachment content may require refreshed attachment endpoint flow or different permissions.

## Safety Rules

1. Do not expose `BC_ACCESS_TOKEN` or `Client Secret` in output.
2. Confirm target before write actions unless user already gave explicit write intent.
3. For write operations, return created object id + app_url + verification result.
