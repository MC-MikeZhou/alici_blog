#!/usr/bin/env python3
"""
Video CDN Uploader
Uploads local video files from a directory to CDN via rsync.

Config can be provided via environment variables or CLI overrides:
- CDN_SERVER_IP (default: 45.76.70.215)
- CDN_SERVER_USER (default: root)
- CDN_VIDEO_REMOTE_PATH (default: /var/www/static/static/video/other/gen_videos/)
- CDN_VIDEO_URL_PREFIX (default: https://ct2.alici.ai/static/video/other/gen_videos/)

Usage:
  python scripts/convert_to_video_json/upload_videos.py --dir ./video_resources
  python scripts/convert_to_video_json/upload_videos.py --dir ./video_resources --dry-run
  python scripts/convert_to_video_json/upload_videos.py --dir ./video_resources --verify-only
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List


VIDEO_EXTS = (".mp4", ".webm", ".mov", ".mkv")


def get_config_from_env():
    server_ip = os.environ.get("CDN_SERVER_IP", "45.76.70.215")
    server_user = os.environ.get("CDN_SERVER_USER", "root")
    remote_path = os.environ.get(
        "CDN_VIDEO_REMOTE_PATH",
        "/var/www/static/static/video/other/gen_videos/",
    )
    url_prefix = os.environ.get(
        "CDN_VIDEO_URL_PREFIX",
        "https://ct2.alici.ai/static/video/other/gen_videos/",
    )
    return server_user, server_ip, remote_path, url_prefix


def list_videos(dir_path: Path) -> List[Path]:
    return [p for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS]


def verify_ssh(server_user: str, server_ip: str) -> bool:
    print("🔍 Verifying SSH access…")
    cmd = ["ssh", "-o", "ConnectTimeout=5", f"{server_user}@{server_ip}", "echo 'Connection OK'"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        if "Connection OK" in result.stdout:
            print("✅ SSH access verified")
            return True
        print("⚠️  SSH connection established but unexpected response")
        return False
    except subprocess.TimeoutExpired:
        print("❌ SSH connection timeout")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ SSH connection failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ ssh command not found (install OpenSSH)")
        return False


def upload(dir_path: Path, server_user: str, server_ip: str, remote_path: str, dry_run: bool = False) -> bool:
    videos = list_videos(dir_path)
    if not videos:
        print(f"⚠️  No videos found in {dir_path}")
        return True

    print(f"📦 Found {len(videos)} videos to upload:")
    for v in videos:
        print(f"  - {v.name}")

    if dry_run:
        print("\n🔍 DRY RUN mode - no actual upload")
        return True

    cmd = [
        "rsync",
        "-avz",
        "--progress",
        f"{str(dir_path)}/",
        f"{server_user}@{server_ip}:{remote_path}",
    ]

    print("\n⬆️  Uploading to CDN via rsync…")
    print("   Command:", " ".join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ Upload complete!")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Upload failed:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("❌ rsync not found. Install it (e.g., brew install rsync)")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload local videos to CDN via rsync")
    parser.add_argument("--dir", default="./video_resources", help="Directory that contains video files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    parser.add_argument("--verify-only", action="store_true", help="Verify SSH only; do not upload")

    # Optional overrides
    parser.add_argument("--server-ip", help="Override CDN server IP")
    parser.add_argument("--server-user", help="Override CDN server user")
    parser.add_argument("--remote-path", help="Override remote directory path")
    parser.add_argument("--url-prefix", help="Override CDN URL prefix")

    args = parser.parse_args()

    server_user, server_ip, remote_path, url_prefix = get_config_from_env()
    if args.server_ip:
        server_ip = args.server_ip
    if args.server_user:
        server_user = args.server_user
    if args.remote_path:
        remote_path = args.remote_path
    if args.url_prefix:
        url_prefix = args.url_prefix

    dir_path = Path(args.dir)
    if not dir_path.exists():
        print(f"❌ Directory not found: {dir_path}")
        return 1

    print("=" * 70)
    print("📤 Video CDN Uploader")
    print("=" * 70)
    print(f"Source dir      : {dir_path}")
    print(f"Server          : {server_user}@{server_ip}")
    print(f"Remote path     : {remote_path}")
    print(f"URL prefix (ref): {url_prefix}")
    print("=" * 70)

    if not verify_ssh(server_user, server_ip):
        return 1
    if args.verify_only:
        print("✅ SSH verification done")
        return 0

    ok = upload(dir_path, server_user, server_ip, remote_path, dry_run=args.dry_run)
    if ok:
        # Print calculated CDN URLs for uploaded files
        for v in list_videos(dir_path):
            print(f"🌐 {url_prefix}{v.name}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

