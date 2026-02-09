#!/usr/bin/env python3
"""Basecamp OAuth helper with local callback capture.

Goal:
- Non-developers can finish OAuth without manually finding `code`.
- Open browser -> click allow -> script auto-captures code and exchanges token.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

AUTH_BASE = "https://launchpad.37signals.com/authorization/new"
TOKEN_URL = "https://launchpad.37signals.com/authorization/token"
AUTH_INFO_URL = "https://launchpad.37signals.com/authorization.json"
DEFAULT_USER_AGENT = "BasecampSkillOAuth (team@example.com)"


def post_form(url: str, data: Dict[str, str]) -> Dict[str, object]:
    payload = urlencode(data).encode("utf-8")
    req = Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} token request failed: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def verify_access_token(token: str, user_agent: str) -> Dict[str, object]:
    req = Request(
        AUTH_INFO_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} token verify failed: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def upsert_export(content: str, key: str, value: str) -> str:
    line = f"export {key}='{value}'"
    lines = content.splitlines()
    found = False
    out = []
    for item in lines:
        if item.strip().startswith(f"export {key}="):
            out.append(line)
            found = True
        else:
            out.append(item)
    if not found:
        out.append(line)
    return "\n".join(out).strip() + "\n"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    expected_state: str = ""
    result_code: Optional[str] = None
    result_error: Optional[str] = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        params = parse_qs(parsed.query)
        state = (params.get("state") or [""])[0]
        code = (params.get("code") or [""])[0]
        err = (params.get("error") or [""])[0]

        if state != self.expected_state:
            self.result_error = "state mismatch"
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"State mismatch")
            return

        if err:
            self.result_error = err
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"OAuth error: {err}".encode("utf-8"))
            return

        if not code:
            self.result_error = "missing code"
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code")
            return

        self.result_code = code
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
<!doctype html>
<html><body style="font-family:Arial,sans-serif;padding:24px;">
  <h2>Basecamp 授权成功</h2>
  <p>可以关闭这个页面，回到终端。</p>
</body></html>
"""
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
        return


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Basecamp OAuth helper: capture code automatically via localhost callback."
    )
    parser.add_argument("--client-id", help="Basecamp integration client_id")
    parser.add_argument("--client-secret", help="Basecamp integration client_secret")
    parser.add_argument("--host", default="127.0.0.1", help="Callback host, default 127.0.0.1")
    parser.add_argument("--port", type=int, default=17800, help="Callback port, default 17800")
    parser.add_argument("--timeout", type=int, default=180, help="OAuth wait timeout seconds")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="API user agent")
    parser.add_argument("--env-file", default="", help="Optional env file path to write export lines")
    parser.add_argument("--no-open", action="store_true", help="Do not auto-open browser")
    args = parser.parse_args()

    client_id = (args.client_id or input("Client ID: ").strip())
    if not client_id:
        print("Client ID required", file=sys.stderr)
        return 2

    client_secret = args.client_secret
    if not client_secret:
        import getpass

        client_secret = getpass.getpass("Client Secret: ").strip()
    if not client_secret:
        print("Client Secret required", file=sys.stderr)
        return 2

    redirect_uri = f"http://{args.host}:{args.port}/callback"
    state = secrets.token_urlsafe(24)

    OAuthCallbackHandler.expected_state = state
    OAuthCallbackHandler.result_code = None
    OAuthCallbackHandler.result_error = None

    try:
        server = HTTPServer((args.host, args.port), OAuthCallbackHandler)
    except OSError as exc:
        print(f"Cannot start local callback server: {exc}", file=sys.stderr)
        return 1

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    auth_url = AUTH_BASE + "?" + urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
        }
    )

    print("\nOpen this URL and click allow:\n")
    print(auth_url)
    print("")
    if not args.no_open:
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

    deadline = time.time() + max(args.timeout, 30)
    while time.time() < deadline:
        if OAuthCallbackHandler.result_code or OAuthCallbackHandler.result_error:
            break
        time.sleep(0.2)

    server.shutdown()
    server.server_close()

    if OAuthCallbackHandler.result_error:
        print(f"OAuth failed: {OAuthCallbackHandler.result_error}", file=sys.stderr)
        return 1

    code = OAuthCallbackHandler.result_code
    if not code:
        print("Timeout: did not receive code. Retry or use manual code flow.", file=sys.stderr)
        return 1

    token_data = post_form(
        TOKEN_URL,
        {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    access_token = str(token_data.get("access_token") or "").strip()
    refresh_token = str(token_data.get("refresh_token") or "").strip()
    expires_in = token_data.get("expires_in")
    if not access_token:
        print(f"No access_token in response: {token_data}", file=sys.stderr)
        return 1

    info = verify_access_token(access_token, args.user_agent)
    accounts = info.get("accounts")
    count = len(accounts) if isinstance(accounts, list) else 0

    print("OAuth success")
    print(f"Visible accounts: {count}")
    print("Export in current shell:")
    print(f"export BC_ACCESS_TOKEN='{access_token}'")
    print(f"export BC_USER_AGENT='{args.user_agent}'")
    if refresh_token:
        print(f"export BC_REFRESH_TOKEN='{refresh_token}'")
    if expires_in:
        print(f"# expires_in={expires_in}s")

    if args.env_file:
        env_path = Path(args.env_file).expanduser().resolve()
        content = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
        content = upsert_export(content, "BC_ACCESS_TOKEN", access_token)
        content = upsert_export(content, "BC_USER_AGENT", args.user_agent)
        if refresh_token:
            content = upsert_export(content, "BC_REFRESH_TOKEN", refresh_token)
        env_path.write_text(content, encoding="utf-8")
        try:
            os.chmod(env_path, 0o600)
        except OSError:
            pass
        print(f"Saved env file: {env_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
