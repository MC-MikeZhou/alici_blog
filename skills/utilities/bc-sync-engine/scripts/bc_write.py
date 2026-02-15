#!/usr/bin/env python3
"""bc_write.py — Basecamp Push commands for bc-sync-engine.

6 commands:
  create-comment  POST recordings/{id}/comments.json
  create-todo     POST todolists/{id}/todos.json
  create-sublist  POST todolists/{id}/groups.json
  create-doc      POST vaults/{id}/documents.json
  create-folder   POST vaults/{id}/vaults.json
  update-todo     POST/DELETE todos/{id}/completion.json

Usage:
  bc_write.py create-comment <recording_id> "<text or .md/.html file>"
  bc_write.py create-todo <list_id> "<title>" [--notes-file ./notes.md]
  bc_write.py create-sublist <list_id> "<name>"
  bc_write.py create-doc <vault_id> "<title>" <content_file.md>
  bc_write.py create-folder <vault_id> "<folder_name>"
  bc_write.py update-todo <todo_id> --complete|--uncomplete

All commands read BC_ACCOUNT / BC_BUCKET from .env.basecamp by default.
Override with --account and --bucket flags.
"""
from __future__ import annotations

import argparse
import html as _html
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from _bc_env import load_basecamp_env, make_token_refresher
from _bc_http import FetchResult, post_json

API_HOST = "https://3.basecampapi.com"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _env_file_path() -> Path:
    """Return the .env.basecamp next to this skill's root."""
    return Path(__file__).resolve().parents[1] / ".env.basecamp"


def _load_env_defaults() -> Dict[str, str]:
    """Load BC_ACCOUNT and BC_BUCKET from .env.basecamp (alongside token vars)."""
    env_path = _env_file_path()
    defaults: Dict[str, str] = {}
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            if key.startswith("export "):
                key = key[len("export "):].strip()
            val = val.strip().strip("'\"")
            if key in ("BC_ACCOUNT", "BC_BUCKET"):
                defaults[key] = val
    return defaults


def _resolve_account_bucket(args: argparse.Namespace) -> tuple[str, str]:
    """Resolve account/bucket from CLI args or .env.basecamp."""
    defaults = _load_env_defaults()
    account = args.account or defaults.get("BC_ACCOUNT", "")
    bucket = args.bucket or defaults.get("BC_BUCKET", "")
    if not account:
        print("ERROR: BC_ACCOUNT not set. Pass --account or add to .env.basecamp", file=sys.stderr)
        sys.exit(1)
    if not bucket:
        print("ERROR: BC_BUCKET not set. Pass --bucket or add to .env.basecamp", file=sys.stderr)
        sys.exit(1)
    return account, bucket


def _get_token_and_agent() -> tuple[str, str, Any]:
    """Load env, return (access_token, user_agent, refresher)."""
    env = load_basecamp_env()
    access_token = (env.values.get("BC_ACCESS_TOKEN") or "").strip()
    user_agent = (env.values.get("BC_USER_AGENT") or "").strip()
    if not access_token or not user_agent:
        print(
            "ERROR: Missing BC_ACCESS_TOKEN / BC_USER_AGENT. "
            "Run oauth_easy.py first or check .env.basecamp.",
            file=sys.stderr,
        )
        sys.exit(1)
    refresher = make_token_refresher(env)
    return access_token, user_agent, refresher


def _md_to_html(text: str) -> str:
    """Lightweight Markdown-to-HTML converter (pure stdlib, no dependencies).

    Supports: headers, ul/ol, code blocks, bold, italic, inline code, links.
    """
    lines = text.split("\n")
    out: list[str] = []
    in_list = False
    in_ol = False
    in_code = False

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(_html.escape(line))
            continue

        # Close lists if needed
        if in_list and not line.startswith("- ") and not line.startswith("* "):
            out.append("</ul>")
            in_list = False
        if in_ol and not re.match(r"^\d+\. ", line):
            out.append("</ol>")
            in_ol = False

        # Headers
        if line.startswith("### "):
            out.append(f"<h3>{_html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{_html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{_html.escape(line[2:])}</h1>")
        # Unordered list
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_html.escape(line[2:])}</li>")
        # Ordered list
        elif re.match(r"^\d+\. ", line):
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\. ", "", line)
            out.append(f"<li>{_html.escape(item)}</li>")
        # Empty line
        elif line.strip() == "":
            continue
        # Paragraph
        else:
            out.append(f"<p>{_html.escape(line)}</p>")

    if in_list:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")
    if in_code:
        out.append("</code></pre>")

    result = "\n".join(out)
    # Inline formatting (applied after HTML escaping of content)
    result = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", result)
    result = re.sub(r"\*(.+?)\*", r"<em>\1</em>", result)
    result = re.sub(r"`(.+?)`", r"<code>\1</code>", result)
    return result


def _read_content(value: str) -> str:
    """Read content from a string, .md file, .html file, or stdin ('-').

    If value is a path to an existing file:
      - .md  -> convert to HTML
      - .html/.htm -> read as-is
      - other -> read as plain text, wrap in <p>
    If value is '-', read from stdin.
    Otherwise, treat as literal text.
    """
    if value == "-":
        raw = sys.stdin.read()
        return f"<p>{_html.escape(raw)}</p>"

    p = Path(value)
    if p.is_file():
        raw = p.read_text(encoding="utf-8")
        ext = p.suffix.lower()
        if ext == ".md":
            return _md_to_html(raw)
        elif ext in (".html", ".htm"):
            return raw
        else:
            return f"<p>{_html.escape(raw)}</p>"

    # Literal text
    return f"<p>{_html.escape(value)}</p>"


def _success_json(res: FetchResult, resource_type: str) -> str:
    """Format a success JSON output."""
    data = res.data if isinstance(res.data, dict) else {}
    out = {
        "ok": True,
        "id": data.get("id"),
        "app_url": data.get("app_url", ""),
        "type": resource_type,
    }
    return json.dumps(out, ensure_ascii=False, indent=2)


def _check_response(res: FetchResult, action: str) -> None:
    """Check response status and exit on error."""
    if res.status < 200 or res.status >= 300:
        err = {
            "ok": False,
            "status": res.status,
            "action": action,
            "body": res.body_text[:500],
        }
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_create_comment(args: argparse.Namespace) -> None:
    """POST recordings/{id}/comments.json"""
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    content_html = _read_content(args.content)
    url = f"{API_HOST}/{account}/buckets/{bucket}/recordings/{args.recording_id}/comments.json"

    res = post_json(
        url=url,
        access_token=access_token,
        user_agent=user_agent,
        data={"content": content_html},
        method="POST",
        refresher=refresher,
    )
    _check_response(res, "create-comment")
    print(_success_json(res, "comment"))


def cmd_create_todo(args: argparse.Namespace) -> None:
    """POST todolists/{id}/todos.json"""
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    payload: Dict[str, Any] = {"content": args.title}
    if args.notes_file:
        notes_html = _read_content(args.notes_file)
        payload["description"] = notes_html

    url = f"{API_HOST}/{account}/buckets/{bucket}/todolists/{args.list_id}/todos.json"

    res = post_json(
        url=url,
        access_token=access_token,
        user_agent=user_agent,
        data=payload,
        method="POST",
        refresher=refresher,
    )
    _check_response(res, "create-todo")
    print(_success_json(res, "todo"))


def cmd_create_sublist(args: argparse.Namespace) -> None:
    """POST todolists/{id}/groups.json"""
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    url = f"{API_HOST}/{account}/buckets/{bucket}/todolists/{args.list_id}/groups.json"

    res = post_json(
        url=url,
        access_token=access_token,
        user_agent=user_agent,
        data={"name": args.name},
        method="POST",
        refresher=refresher,
    )
    _check_response(res, "create-sublist")
    print(_success_json(res, "todolist_group"))


def cmd_create_doc(args: argparse.Namespace) -> None:
    """POST vaults/{id}/documents.json"""
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    content_html = _read_content(args.content_file)
    url = f"{API_HOST}/{account}/buckets/{bucket}/vaults/{args.vault_id}/documents.json"

    res = post_json(
        url=url,
        access_token=access_token,
        user_agent=user_agent,
        data={
            "title": args.title,
            "content": content_html,
            "status": "active",
        },
        method="POST",
        refresher=refresher,
    )
    _check_response(res, "create-doc")
    print(_success_json(res, "document"))


def cmd_create_folder(args: argparse.Namespace) -> None:
    """POST vaults/{id}/vaults.json — Create a folder inside a vault."""
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    url = f"{API_HOST}/{account}/buckets/{bucket}/vaults/{args.vault_id}/vaults.json"

    res = post_json(
        url=url,
        access_token=access_token,
        user_agent=user_agent,
        data={"title": args.name},
        method="POST",
        refresher=refresher,
    )
    _check_response(res, "create-folder")
    print(_success_json(res, "vault"))


def cmd_update_todo(args: argparse.Namespace) -> None:
    """Complete/uncomplete a todo via the Basecamp completion endpoint.

    Complete:   POST   /buckets/{bucket}/todos/{id}/completion.json
    Uncomplete: DELETE /buckets/{bucket}/todos/{id}/completion.json
    """
    account, bucket = _resolve_account_bucket(args)
    access_token, user_agent, refresher = _get_token_and_agent()

    url = f"{API_HOST}/{account}/buckets/{bucket}/todos/{args.todo_id}/completion.json"

    if args.complete:
        res = post_json(
            url=url,
            access_token=access_token,
            user_agent=user_agent,
            data={},
            method="POST",
            refresher=refresher,
        )
    elif args.uncomplete:
        res = post_json(
            url=url,
            access_token=access_token,
            user_agent=user_agent,
            data={},
            method="DELETE",
            refresher=refresher,
        )
    else:
        print("ERROR: specify --complete or --uncomplete", file=sys.stderr)
        sys.exit(1)

    _check_response(res, "update-todo")
    # Completion endpoint returns 204 No Content on success
    if res.status == 204 or (200 <= res.status < 300):
        out = {"ok": True, "id": int(args.todo_id), "app_url": "", "type": "todo_completion"}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(_success_json(res, "todo_completion"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="bc_write.py — Basecamp Push commands for bc-sync-engine",
    )
    parser.add_argument("--account", default="", help="Basecamp account ID (default: from .env.basecamp BC_ACCOUNT)")
    parser.add_argument("--bucket", default="", help="Basecamp project/bucket ID (default: from .env.basecamp BC_BUCKET)")

    sub = parser.add_subparsers(dest="command", required=True)

    # create-comment
    p_comment = sub.add_parser("create-comment", help="Post a comment on a recording")
    p_comment.add_argument("recording_id", help="Basecamp recording ID")
    p_comment.add_argument("content", help="Comment text, .md file path, .html file path, or '-' for stdin")

    # create-todo
    p_todo = sub.add_parser("create-todo", help="Create a todo in a todolist")
    p_todo.add_argument("list_id", help="Todolist ID")
    p_todo.add_argument("title", help="Todo title/content")
    p_todo.add_argument("--notes-file", default="", help="Optional notes file (.md/.html) for todo description")

    # create-sublist
    p_sublist = sub.add_parser("create-sublist", help="Create a sub-group in a todolist")
    p_sublist.add_argument("list_id", help="Parent todolist ID")
    p_sublist.add_argument("name", help="Sub-list/group name")

    # create-doc
    p_doc = sub.add_parser("create-doc", help="Create a document in a vault")
    p_doc.add_argument("vault_id", help="Vault ID")
    p_doc.add_argument("title", help="Document title")
    p_doc.add_argument("content_file", help="Content file (.md/.html) or literal text")

    # create-folder
    p_folder = sub.add_parser("create-folder", help="Create a folder in a vault")
    p_folder.add_argument("vault_id", help="Parent vault/folder ID")
    p_folder.add_argument("name", help="Folder name")

    # update-todo
    p_update = sub.add_parser("update-todo", help="Update a todo (complete/uncomplete)")
    p_update.add_argument("todo_id", help="Todo ID")
    p_update_group = p_update.add_mutually_exclusive_group(required=True)
    p_update_group.add_argument("--complete", action="store_true", help="Mark todo as completed")
    p_update_group.add_argument("--uncomplete", action="store_true", help="Mark todo as not completed")

    args = parser.parse_args(argv)

    commands = {
        "create-comment": cmd_create_comment,
        "create-todo": cmd_create_todo,
        "create-sublist": cmd_create_sublist,
        "create-doc": cmd_create_doc,
        "create-folder": cmd_create_folder,
        "update-todo": cmd_update_todo,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
