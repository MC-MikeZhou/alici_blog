#!/usr/bin/env python3
"""
Create a Klimt-style placeholder image (SVG-based PNG)
This is a temporary solution while FAL.ai image generation is pending.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_klimt_style_image(width=1920, height=400, output_path='./gen_images/klimt_ai_human_paradox.png'):
    """Create a Klimt-inspired placeholder image"""

    # Create image with Klimt-inspired gradient background
    img = Image.new('RGB', (width, height), color=(200, 180, 100))  # Klimt gold base
    draw = ImageDraw.Draw(img, 'RGBA')

    # Create gradient-like effect with semi-transparent layers
    # Golden Byzantine background (left side)
    for i in range(width // 2):
        alpha = int(200 * (1 - i / (width // 2)))
        color = (220, 200, 80, alpha)  # Gold fading
        draw.line([(i, 0), (i, height)], fill=color, width=1)

    # Cool blue/silver side (right side - AI side)
    for i in range(width // 2, width):
        progress = (i - width // 2) / (width // 2)
        alpha = int(180 * progress)
        color = (100, 150, 200, alpha)  # Cool blue
        draw.line([(i, 0), (i, height)], fill=color, width=1)

    # Add ornamental patterns (circles and decorative elements)
    # Left side patterns (warm/golden)
    for _ in range(30):
        x = random.randint(0, width // 2)
        y = random.randint(0, height)
        radius = random.randint(5, 30)
        color = (255, 230, 150, 100)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                     outline=color, width=2)

    # Right side patterns (cool/silver)
    for _ in range(30):
        x = random.randint(width // 2, width)
        y = random.randint(0, height)
        size = random.randint(10, 40)
        color = (180, 200, 220, 100)
        draw.rectangle([x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                      outline=color, width=2)

    # Add center vertical line to represent the meeting point
    mid_x = width // 2
    for y in range(height):
        shade = int(150 + 50 * (y / height))
        draw.line([(mid_x - 1, y), (mid_x + 1, y)], fill=(shade, shade, shade))

    # Add text overlay indicating this is for Klimt image
    try:
        # Try to use a larger font
        font_size = int(height / 6)
        # This will fail gracefully if font not found
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # Add watermark text
    text = "AI & Human Collaboration"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = (height - (text_bbox[3] - text_bbox[1])) // 2

    # Draw semi-transparent background for text
    draw.rectangle(
        [text_x - 20, text_y - 10, text_x + text_width + 20, text_y + (text_bbox[3] - text_bbox[1]) + 10],
        fill=(255, 255, 255, 150)
    )

    # Draw text
    draw.text((text_x, text_y), text, fill=(100, 100, 100, 255), font=font)

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"✅ Placeholder image created: {output_path}")

    return output_path

def update_image_json(image_name, image_path, json_path='./tmp_image.json'):
    """Update tmp_image.json with new image entry"""
    try:
        # Load existing JSON
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                image_data = json.load(f)
        else:
            image_data = {}

        # Add new image entry
        image_url = f"https://ct2.alici.ai/static/image/other/gen_images/{os.path.basename(image_path)}"
        image_data[image_name] = image_url

        # Save updated JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(image_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Updated {json_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to update image JSON: {str(e)}")
        return False

if __name__ == '__main__':
    print("🎨 Creating Klimt-style placeholder image...")

    # Create placeholder
    img_path = create_klimt_style_image()

    # Update metadata
    update_image_json('klimt_cover', img_path)

    print("\n💡 Note: This is a placeholder image.")
    print("   To generate the actual Klimt-style image:")
    print("   1. Set FAL_API_KEY environment variable")
    print("   2. Run: python3 gen_klimt_image.py")
