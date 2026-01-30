#!/usr/bin/env python3
"""
FAL.ai Nano Banana Pro Image Generator
统一的图片生成脚本，供 Editor Skill v2.6 调用
Updated for v2.6: Added Asset Pack roles (character, character_portrait, storyboard_frame, video_poster)
"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
import hashlib
import csv
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# Configuration
# ============================================================================

def get_fal_api_key():
    """
    Get FAL API Key from multiple sources, priority order:
    1. Environment variable FAL_API_KEY
    2. .mcp.json file (mcpServers.fal.env.FAL_API_KEY)

    Returns:
        str: API key or empty string if not found
    """
    # Priority 1: Check environment variable
    key = os.environ.get('FAL_API_KEY')
    if key:
        return key

    # Priority 2: Read from .mcp.json configuration file
    mcp_paths = [
        '/Users/H/Documents/AliciBlog/.mcp.json',
        os.path.join(os.path.dirname(__file__), '..', '.mcp.json')
    ]

    for path in mcp_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    fal_config = config.get('mcpServers', {}).get('fal', {})
                    fal_env = fal_config.get('env', {})
                    if 'FAL_API_KEY' in fal_env:
                        return fal_env['FAL_API_KEY']
            except Exception as e:
                # Silently continue to next path if read fails
                continue

    return ''

FAL_ENDPOINT = "https://queue.fal.run/fal-ai/nano-banana"
FAL_API_KEY = get_fal_api_key()

# Default parameters matching Editor Skill v2.0 spec
DEFAULT_SIZE = {"width": 1920, "height": 1080}
DEFAULT_STEPS = 35
DEFAULT_GUIDANCE = 7.5

# Image role configurations (Editor Skill v2.6 - correct API format)
# nano-banana uses aspect_ratio + resolution, not width/height
ROLE_CONFIGS = {
    "hero": {"aspect_ratio": "16:9", "resolution": "2K"},      # 16:9 high-res
    "concept": {"aspect_ratio": "16:9", "resolution": "1K"},   # 16:9 standard
    "comparison": {"aspect_ratio": "16:9", "resolution": "1K"},# 16:9 standard
    "cta": {"aspect_ratio": "16:9", "resolution": "1K"},       # 16:9 standard
    # NEW in v2.6: Asset Pack roles for micro_roundup articles
    "character": {"aspect_ratio": "1:1", "resolution": "2K"},            # Character cards (square)
    "character_portrait": {"aspect_ratio": "4:5", "resolution": "2K"},   # Character portrait (vertical)
    "storyboard_frame": {"aspect_ratio": "16:9", "resolution": "1K"},    # Motion breakdown frames
    "video_poster": {"aspect_ratio": "16:9", "resolution": "2K"}         # Video thumbnails
}

# Polling configuration for async queue
MAX_POLL_ATTEMPTS = 60  # 5 minutes max (60 * 5s)
POLL_INTERVAL = 5  # seconds

# Request deduplication cache
_request_cache: Dict[str, str] = {}  # prompt_hash -> request_id

# API usage logging
API_LOG_FILE = os.path.join(os.path.dirname(__file__), "api_usage.csv")


# ============================================================================
# Core Functions
# ============================================================================

def get_prompt_hash(prompt: str, config: Dict[str, str]) -> str:
    """
    Generate unique hash for prompt + config combination

    Args:
        prompt: Image generation prompt
        config: Dict with 'aspect_ratio' and 'resolution'

    Returns:
        12-character hash string
    """
    content = f"{prompt}|{config['aspect_ratio']}@{config['resolution']}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def log_api_call(
    action: str,
    model: str,
    prompt_hash: str,
    config: Dict[str, str],
    status: str,
    duration_ms: int = 0
):
    """
    Log API call to CSV file for cost tracking

    Args:
        action: "submit" | "poll" | "download"
        model: Model name (e.g., "nano-banana")
        prompt_hash: Hash of the prompt
        config: Dict with 'aspect_ratio' and 'resolution'
        status: "success" | "failed"
        duration_ms: Duration in milliseconds
    """
    row = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "model": model,
        "prompt_hash": prompt_hash,
        "size": f"{config['aspect_ratio']}@{config['resolution']}",
        "status": status,
        "duration_ms": duration_ms
    }

    file_exists = os.path.exists(API_LOG_FILE)
    try:
        with open(API_LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"⚠️  Failed to log API call: {e}")

def submit_image_request(prompt: str, config: Dict[str, str]) -> Optional[str]:
    """
    Submit image generation request to FAL.ai nano-banana

    Args:
        prompt: ICS-framework structured prompt
        config: Dict with 'aspect_ratio' and 'resolution'

    Returns:
        Request ID for polling, or None if failed
    """
    if not FAL_API_KEY:
        print("❌ Error: FAL_API_KEY environment variable not set")
        print("   Please run: export FAL_API_KEY='your-api-key'")
        return None

    # Check deduplication cache
    prompt_hash = get_prompt_hash(prompt, config)
    if prompt_hash in _request_cache:
        print(f"♻️  Using cached request (hash: {prompt_hash})")
        return _request_cache[prompt_hash]

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "aspect_ratio": config['aspect_ratio'],
        "resolution": config['resolution'],
        "num_inference_steps": DEFAULT_STEPS,
        "guidance_scale": DEFAULT_GUIDANCE,
        "enable_safety_checker": True
    }

    start_time = time.time()
    try:
        print(f"🎨 Submitting request to {FAL_ENDPOINT}")
        print(f"   Aspect Ratio: {config['aspect_ratio']}, Resolution: {config['resolution']}")

        request = urllib.request.Request(
            FAL_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

            # nano-banana returns request_id for polling
            if 'request_id' in result:
                request_id = result['request_id']
                # Cache the request
                _request_cache[prompt_hash] = request_id
                # Log successful submission
                duration_ms = int((time.time() - start_time) * 1000)
                log_api_call("submit", "nano-banana", prompt_hash, config, "success", duration_ms)
                return request_id
            # Some endpoints return image immediately
            elif 'images' in result and len(result['images']) > 0:
                image_url = result['images'][0]['url']
                _request_cache[prompt_hash] = image_url
                duration_ms = int((time.time() - start_time) * 1000)
                log_api_call("submit", "nano-banana", prompt_hash, config, "success", duration_ms)
                return image_url
            else:
                print(f"❌ Unexpected response format: {result}")
                duration_ms = int((time.time() - start_time) * 1000)
                log_api_call("submit", "nano-banana", prompt_hash, config, "failed", duration_ms)
                return None

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"   Response: {error_body}")
        except:
            pass
        duration_ms = int((time.time() - start_time) * 1000)
        log_api_call("submit", "nano-banana", prompt_hash, config, "failed", duration_ms)
        return None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        duration_ms = int((time.time() - start_time) * 1000)
        log_api_call("submit", "nano-banana", prompt_hash, config, "failed", duration_ms)
        return None


def get_poll_interval(attempt: int) -> int:
    """
    Calculate exponential backoff interval

    Args:
        attempt: Current attempt number (0-indexed)

    Returns:
        Wait interval in seconds
    """
    base = 5  # Base interval: 5 seconds
    max_interval = 60  # Maximum interval: 60 seconds
    # Double interval every 5 attempts: 5s → 10s → 20s → 40s → 60s
    factor = 2 ** (attempt // 5)
    return min(base * factor, max_interval)


def poll_result(request_id: str) -> Optional[str]:
    """
    Poll for image generation result

    Args:
        request_id: Request ID from submit_image_request

    Returns:
        Image URL or None if failed
    """
    status_url = f"{FAL_ENDPOINT}/requests/{request_id}/status"

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(MAX_POLL_ATTEMPTS):
        try:
            request = urllib.request.Request(status_url, headers=headers)

            with urllib.request.urlopen(request, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))

                status = result.get('status', 'unknown').lower()  # Convert to lowercase for comparison

                if status == 'completed':
                    # Check if there's a response_url to fetch the actual result
                    if 'response_url' in result:
                        print(f"📥 Fetching result from response_url...")
                        try:
                            response_request = urllib.request.Request(
                                result['response_url'],
                                headers={"Authorization": f"Key {FAL_API_KEY}"}
                            )
                            with urllib.request.urlopen(response_request, timeout=10) as resp:
                                final_result = json.loads(resp.read().decode('utf-8'))

                                # Now extract image URL from final result
                                if 'images' in final_result and len(final_result['images']) > 0:
                                    image_url = final_result['images'][0]['url']
                                    print(f"✅ Generation complete!")
                                    return image_url
                                elif 'image' in final_result:
                                    if isinstance(final_result['image'], dict):
                                        image_url = final_result['image'].get('url')
                                    else:
                                        image_url = final_result['image']
                                    if image_url:
                                        print(f"✅ Generation complete!")
                                        return image_url

                        except Exception as e:
                            print(f"❌ Error fetching response_url: {e}")
                            return None

                    # Direct image URL in response (non-queue mode)
                    if 'images' in result and len(result['images']) > 0:
                        image_url = result['images'][0]['url']
                        print(f"✅ Generation complete!")
                        return image_url
                    elif 'image' in result:
                        if isinstance(result['image'], dict):
                            image_url = result['image'].get('url')
                        else:
                            image_url = result['image']
                        if image_url:
                            print(f"✅ Generation complete!")
                            return image_url

                    # If we get here, couldn't find URL - print response for debugging
                    print(f"❌ Completed but no image URL in response")
                    print(f"   Response keys: {list(result.keys())}")
                    return None

                elif status == 'failed':
                    error_msg = result.get('error', 'Unknown error')
                    print(f"❌ Generation failed: {error_msg}")
                    return None

                elif status in ['queued', 'processing', 'in_progress']:
                    interval = get_poll_interval(attempt)
                    print(f"⏳ Status: {status} (attempt {attempt + 1}/{MAX_POLL_ATTEMPTS}, wait {interval}s)")
                    time.sleep(interval)
                    continue

                else:
                    interval = get_poll_interval(attempt)
                    print(f"⚠️  Unknown status: {status} (wait {interval}s)")
                    time.sleep(interval)
                    continue

        except Exception as e:
            interval = get_poll_interval(attempt)
            print(f"❌ Polling error: {str(e)} (wait {interval}s)")
            time.sleep(interval)
            continue

    print(f"❌ Polling timeout after {MAX_POLL_ATTEMPTS} attempts")
    return None


def download_image(url: str, output_path: str) -> bool:
    """Download image from URL and save locally"""
    try:
        print(f"⬇️  Downloading: {url}")

        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            image_data = response.read()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(image_data)

        file_size = len(image_data) / 1024
        print(f"✅ Saved: {output_path} ({file_size:.1f} KB)")
        return True

    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False


def generate_image(
    prompt: str,
    role: str = "hero",
    output_dir: str = "./gen_images",
    filename: Optional[str] = None
) -> Optional[Dict]:
    """
    Generate single image with nano-banana

    Args:
        prompt: ICS-framework prompt
        role: Image role (hero|concept|comparison|cta)
        output_dir: Directory to save image
        filename: Custom filename (optional, auto-generated if None)

    Returns:
        Dict with 'local_path' and 'cdn_url', or None if failed
    """
    config = ROLE_CONFIGS.get(role, {"aspect_ratio": "16:9", "resolution": "2K"})

    print("\n" + "=" * 70)
    print(f"🎨 Generating {role.upper()} image")
    print("=" * 70)
    print(f"Prompt: {prompt[:100]}...")

    # Step 1: Submit request
    request_id = submit_image_request(prompt, config)
    if not request_id:
        return None

    # Step 2: Handle response (immediate URL or request ID for polling)
    if request_id.startswith('http'):
        # Direct image URL returned
        image_url = request_id
    else:
        # Poll for result
        image_url = poll_result(request_id)
        if not image_url:
            return None

    # Step 3: Download image
    if not filename:
        timestamp = int(time.time())
        filename = f"{role}_{timestamp}.png"

    local_path = os.path.join(output_dir, filename)

    if not download_image(image_url, local_path):
        return None

    # Step 4: Construct CDN URL
    cdn_url = f"https://ct2.alici.ai/static/image/other/gen_images/{filename}"

    return {
        "role": role,
        "local_path": local_path,
        "cdn_url": cdn_url,
        "config": config
    }


def batch_generate(prompts: List[Dict], output_dir: str = "./gen_images") -> List[Dict]:
    """
    Batch generate multiple images

    Args:
        prompts: List of dicts with 'prompt', 'role', 'filename' (optional)

    Returns:
        List of result dicts
    """
    results = []

    print("\n" + "=" * 70)
    print(f"📦 Batch Generation: {len(prompts)} images")
    print("=" * 70)

    for i, item in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}]")

        result = generate_image(
            prompt=item['prompt'],
            role=item.get('role', 'hero'),
            output_dir=output_dir,
            filename=item.get('filename')
        )

        if result:
            results.append(result)
        else:
            print(f"⚠️  Image {i} failed, skipping...")

    return results


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="FAL.ai Nano Banana Pro Image Generator (Editor Skill v2.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single hero image
  python fal_image_generator.py --prompt "Magazine cover..." --role hero

  # Generate from batch JSON
  python fal_image_generator.py --batch prompts.json

  # Test mode (without actual generation)
  python fal_image_generator.py --test

Batch JSON format:
  [
    {"prompt": "...", "role": "hero", "filename": "ai-tools-hero.png"},
    {"prompt": "...", "role": "concept", "filename": "ai-tools-concept.png"}
  ]
        """
    )

    parser.add_argument('--prompt', type=str, help='ICS-framework prompt')
    parser.add_argument('--role', type=str, default='hero',
                        choices=['hero', 'concept', 'comparison', 'cta'],
                        help='Image role (determines size)')
    parser.add_argument('--output-dir', type=str, default='./gen_images',
                        help='Output directory')
    parser.add_argument('--filename', type=str, help='Custom filename')
    parser.add_argument('--batch', type=str, help='Batch mode: JSON file with prompts')
    parser.add_argument('--test', action='store_true', help='Test mode (check config)')
    parser.add_argument('--show-log', action='store_true',
                        help='Show recent API usage log (last 10 entries)')
    parser.add_argument('--clear-cache', action='store_true',
                        help='Clear request deduplication cache')

    args = parser.parse_args()

    # Show API usage log
    if args.show_log:
        if os.path.exists(API_LOG_FILE):
            print("📊 Recent API Usage (last 10 entries):")
            print("=" * 70)
            try:
                with open(API_LOG_FILE, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    for row in rows[-10:]:
                        print(f"{row['timestamp'][:19]} | {row['action']:8} | "
                              f"{row['status']:7} | {row['size']:10} | "
                              f"{row['prompt_hash']}")
            except Exception as e:
                print(f"❌ Error reading log: {e}")
        else:
            print("📊 No API usage log found yet")
        return 0

    # Clear request cache
    if args.clear_cache:
        _request_cache.clear()
        print("🗑️  Request cache cleared")
        return 0

    # Test mode
    if args.test:
        print("🔍 Testing FAL.ai configuration...")
        print(f"   Endpoint: {FAL_ENDPOINT}")
        print(f"   API Key: {'✅ Set' if FAL_API_KEY else '❌ Not set'}")
        print(f"   Default size: {DEFAULT_SIZE}")
        return 0 if FAL_API_KEY else 1

    # Batch mode
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                prompts = json.load(f)

            results = batch_generate(prompts, args.output_dir)

            print("\n" + "=" * 70)
            print(f"✅ Batch complete: {len(results)}/{len(prompts)} succeeded")
            print("=" * 70)

            # Save results to JSON
            results_path = args.batch.replace('.json', '_results.json')
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"📊 Results saved to: {results_path}")

            return 0 if len(results) == len(prompts) else 1

        except Exception as e:
            print(f"❌ Batch generation failed: {str(e)}")
            return 1

    # Single image mode
    if not args.prompt:
        parser.print_help()
        return 1

    result = generate_image(
        prompt=args.prompt,
        role=args.role,
        output_dir=args.output_dir,
        filename=args.filename
    )

    if result:
        print("\n" + "=" * 70)
        print("✅ Image generation complete!")
        print("=" * 70)
        print(f"📁 Local path: {result['local_path']}")
        print(f"🌐 CDN URL: {result['cdn_url']}")
        print(f"📐 Config: {result['config']['aspect_ratio']} @ {result['config']['resolution']}")
        return 0
    else:
        print("\n❌ Image generation failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
