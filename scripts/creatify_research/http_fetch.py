#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import Optional


DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class FetchResult:
    url: str
    ok: bool
    status: Optional[int]
    text: str
    error: str
    attempts: int


def fetch_text_via_curl(
    url: str,
    *,
    user_agent: str = DEFAULT_UA,
    connect_timeout_s: int = 6,
    max_time_s: int = 20,
    retries: int = 10,
    backoff_s: float = 0.6,
    post_data: Optional[str] = None,
) -> FetchResult:
    """
    Fetch a URL via curl with retries.

    Why curl:
      - Python DNS resolution is unreliable in this environment.
      - curl tends to succeed more often here.
    """
    if retries < 1:
        retries = 1

    last_err = ""
    last_out = ""
    last_status: Optional[int] = None

    marker = "___CURL_STATUS___:"
    for attempt in range(1, retries + 1):
        # -4: DNS in this environment is flaky on IPv6; force IPv4.
        # -L: follow redirects
        # -w: append final HTTP status for parsing, without mixing headers into body.
        cmd = [
            "curl",
            "-4",
            "-sS",
            "-L",
            "--connect-timeout",
            str(int(connect_timeout_s)),
            "--max-time",
            str(int(max_time_s)),
            "-A",
            user_agent,
            "-w",
            f"\n{marker}%{{http_code}}\n",
            url,
        ]
        if post_data is not None:
            cmd.extend(["-H", "Content-Type: application/x-www-form-urlencoded", "--data-raw", post_data])
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0 and p.stdout:
            raw = p.stdout
            # Status is in the last marker line.
            status = None
            body = raw
            if marker in raw:
                body, tail = raw.rsplit(marker, 1)
                body = body.rstrip("\n")
                tail = tail.strip()
                try:
                    status = int(tail.splitlines()[0].strip())
                except Exception:
                    status = None
            last_status = status
            return FetchResult(url=url, ok=True, status=status, text=body, error="", attempts=attempt)

        last_err = (p.stderr or p.stdout or "").strip()
        last_out = p.stdout or ""
        time.sleep(min(6.0, backoff_s * attempt))

    return FetchResult(
        url=url,
        ok=False,
        status=last_status,
        text=last_out,
        error=last_err[:400],
        attempts=retries,
    )
