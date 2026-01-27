#!/usr/bin/env python3
"""
Generate Klimt-style cover image using FAL.ai API
"""
import json
import os
import sys
import base64
import urllib.request
import urllib.error

# FAL.ai API configuration
FAL_API_KEY = os.environ.get('FAL_API_KEY', '')
OUTPUT_DIR = './gen_images'
OUTPUT_FILENAME = 'klimt_ai_human_paradox.png'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
IMAGE_JSON_PATH = './tmp_image.json'

# Klimt prompt (simplified version for faster generation)
KLIMT_PROMPT = """In the style of Gustav Klimt's symbolic art, create a composition that represents the paradox of technological progress.

Central image: A radiology scan (X-ray or CT scan) is being analyzed - half by a glowing AI machine with intricate circuitry patterns, and half by delicate human hands. The machine side is rendered in cold silver and blue metallic geometries, while the human side is rendered in warm gold leaf and organic flowing patterns typical of Klimt's work.

Background: Byzantine-inspired golden patterns and symbols representing growth, transformation, and interconnected knowledge.

Color palette: Rich golds, deep blues, subtle purples, and metallic silvers with ornamental decorative elements throughout.

Style: Gustav Klimt's symbolism, with Art Nouveau decorative elements, ornamental details, and gold leaf effects.

Composition: Symmetrical yet dynamic, representing duality and paradox."""

def submit_fal_request(prompt, width=1920, height=400):
    """Submit image generation request to FAL.ai"""

    if not FAL_API_KEY:
        print("❌ Error: FAL_API_KEY environment variable not set")
        print("Please set: export FAL_API_KEY='your-api-key'")
        return None

    # Use FAL.ai image generation endpoint
    url = "https://api.fal.ai/v1/flux/dev"

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "image_size": {
            "width": width,
            "height": height
        },
        "num_inference_steps": 28,
        "guidance_scale": 7.5,
        "enable_safety_checker": True
    }

    try:
        print(f"🎨 Submitting image generation request to FAL.ai...")
        print(f"   Dimensions: {width}x{height}")

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

            if 'images' in result and len(result['images']) > 0:
                return result['images'][0]['url']
            elif 'image' in result:
                return result['image']['url']
            else:
                print("❌ Unexpected response format from FAL.ai")
                print(json.dumps(result, indent=2))
                return None

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"   Response: {error_body}")
        except:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def download_image(url, output_path):
    """Download image from URL and save locally"""
    try:
        print(f"⬇️  Downloading image...")
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
        print(f"✅ Image saved: {output_path} ({file_size:.1f} KB)")
        return True

    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False

def update_image_json(image_name, image_path):
    """Update tmp_image.json with new image entry"""
    try:
        # Load existing JSON
        if os.path.exists(IMAGE_JSON_PATH):
            with open(IMAGE_JSON_PATH, 'r', encoding='utf-8') as f:
                image_data = json.load(f)
        else:
            image_data = {}

        # Add new image entry
        image_url = f"https://ct2.alici.ai/static/image/other/gen_images/{os.path.basename(image_path)}"
        image_data[image_name] = image_url

        # Save updated JSON
        with open(IMAGE_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(image_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Updated {IMAGE_JSON_PATH}")
        print(f"   {image_name}: {image_url}")
        return True

    except Exception as e:
        print(f"❌ Failed to update image JSON: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🎨 Klimt-Style Cover Image Generator")
    print("=" * 60)

    # Check if API key is set
    if not FAL_API_KEY:
        print("\n⚠️  No FAL_API_KEY found. Please set it:")
        print("   export FAL_API_KEY='your-fal-api-key'")
        print("\nAlternatively, you can:")
        print("1. Use a pre-generated image")
        print("2. Generate using a different tool")
        print("3. Use a placeholder image for testing")
        return 1

    # Generate image via FAL.ai
    print("\n📝 Using prompt:")
    print(f"   {KLIMT_PROMPT[:100]}...")

    image_url = submit_fal_request(KLIMT_PROMPT)

    if not image_url:
        print("\n❌ Failed to generate image via FAL.ai")
        return 1

    print(f"✨ Generated image URL: {image_url}")

    # Download and save locally
    if not download_image(image_url, OUTPUT_PATH):
        print("\n❌ Failed to download generated image")
        return 1

    # Update JSON metadata
    if not update_image_json('klimt_cover', OUTPUT_PATH):
        print("\n❌ Failed to update image metadata")
        return 1

    print("\n" + "=" * 60)
    print("✅ Image generation complete!")
    print("=" * 60)
    print(f"📁 Image location: {OUTPUT_PATH}")
    print(f"📊 Metadata updated in: {IMAGE_JSON_PATH}")
    print("\n✨ Next steps:")
    print("1. Update HTML file with image reference")
    print("2. Proceed with English translation")
    print("3. Generate final JSON output")

    return 0

if __name__ == '__main__':
    sys.exit(main())
