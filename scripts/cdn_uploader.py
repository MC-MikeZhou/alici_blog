#!/usr/bin/env python3
"""
CDN Uploader Script
Upload generated images to alici.ai CDN via rsync
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

CDN_SERVER = "root@45.76.70.215"
CDN_REMOTE_PATH = "/var/www/static/static/image/other/gen_images/"
CDN_URL_PREFIX = "https://ct2.alici.ai/static/image/other/gen_images/"


# ============================================================================
# Core Functions
# ============================================================================

def upload_images(local_dir: str, dry_run: bool = False) -> bool:
    """
    Upload images from local directory to CDN

    Args:
        local_dir: Local directory containing images
        dry_run: If True, only show what would be uploaded

    Returns:
        True if successful, False otherwise
    """
    local_path = Path(local_dir)

    if not local_path.exists():
        print(f"❌ Error: Directory not found: {local_dir}")
        return False

    # Find PNG images
    images = list(local_path.glob("*.png")) + list(local_path.glob("*.jpg"))

    if not images:
        print(f"⚠️  No images found in {local_dir}")
        return True

    print(f"📦 Found {len(images)} images to upload:")
    for img in images:
        print(f"   - {img.name}")

    if dry_run:
        print("\n🔍 DRY RUN mode - no actual upload")
        return True

    # Build rsync command
    cmd = [
        "rsync",
        "-avz",  # archive, verbose, compress
        "--progress",
        f"{local_dir}/",
        f"{CDN_SERVER}:{CDN_REMOTE_PATH}"
    ]

    print(f"\n⬆️  Uploading to CDN...")
    print(f"   Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

        print("\n✅ Upload complete!")
        print("\n📋 CDN URLs:")
        for img in images:
            cdn_url = f"{CDN_URL_PREFIX}{img.name}"
            print(f"   {cdn_url}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Upload failed:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("\n❌ rsync command not found")
        print("   Please install rsync: brew install rsync")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def verify_ssh_access() -> bool:
    """Verify SSH access to CDN server"""
    print("🔍 Verifying SSH access...")

    cmd = ["ssh", "-o", "ConnectTimeout=5", CDN_SERVER, "echo 'Connection OK'"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        if "Connection OK" in result.stdout:
            print("✅ SSH access verified")
            return True
        else:
            print("⚠️  SSH connection established but unexpected response")
            return False

    except subprocess.TimeoutExpired:
        print("❌ SSH connection timeout")
        print("   Please check network connection")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ SSH connection failed: {e.stderr}")
        print("\n💡 Setup instructions:")
        print("   1. Ensure SSH key is added: ssh-add ~/.ssh/id_rsa")
        print("   2. Test connection: ssh root@45.76.70.215")
        return False
    except FileNotFoundError:
        print("❌ ssh command not found")
        return False


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Upload generated images to alici.ai CDN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload all images from ./gen_images/
  python cdn_uploader.py --dir ./gen_images

  # Dry run (show what would be uploaded)
  python cdn_uploader.py --dir ./gen_images --dry-run

  # Verify SSH access only
  python cdn_uploader.py --verify-only
        """
    )

    parser.add_argument('--dir', type=str, default='./gen_images',
                        help='Directory containing images to upload')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be uploaded without actual upload')
    parser.add_argument('--verify-only', action='store_true',
                        help='Only verify SSH access, no upload')

    args = parser.parse_args()

    print("=" * 70)
    print("📤 CDN Uploader for alici.ai")
    print("=" * 70)
    print(f"Server: {CDN_SERVER}")
    print(f"Remote path: {CDN_REMOTE_PATH}")
    print(f"URL prefix: {CDN_URL_PREFIX}")
    print("=" * 70)

    # Verify SSH access first
    if not verify_ssh_access():
        return 1

    if args.verify_only:
        print("\n✅ Verification complete")
        return 0

    # Upload images
    if upload_images(args.dir, dry_run=args.dry_run):
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
