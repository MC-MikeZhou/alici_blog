#!/usr/bin/env python3
"""
Generate overlapping-cards collage cover for AliciBlog.

5 photos arranged as fanned, rotated cards on a black canvas
with teal-colored shadows and borders (Alici AI brand identity).

Output: 1200x630 JPEG
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

# === Configuration ===

CANVAS_W, CANVAS_H = 1200, 630
BG_COLOR = (0, 0, 0)

# Card dimensions (portrait 3:4)
CARD_W = 180
CARD_H = int(CARD_W * 4 / 3)  # 240
HERO_SCALE = 1.3
CORNER_RADIUS = 6

# Teal brand color
TEAL = (79, 209, 197)  # #4FD1C5

# Border
BORDER_WIDTH = 2
BORDER_OPACITY = int(255 * 0.40)  # 40%

# Shadow
SHADOW_OFFSET = (4, 6)
SHADOW_BLUR = 12
SHADOW_OPACITY = int(255 * 0.25)  # 25%

# Background glow
GLOW_RADIUS = 300
GLOW_OPACITY = int(255 * 0.08)  # 8%

# Layout
ROTATION_ANGLES = [-14, -7, 0, 7, 14]
HORIZONTAL_SPAN = 700  # tighter span for more overlap between cards
VERTICAL_CENTER_Y = 300  # slightly above center
ARC_DROP = 25  # how much outer cards drop (arc effect)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(
    BASE_DIR,
    "reports",
    "1.29 How to Create an AI Influencer-10 Prompt",
    "images",
)
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "reports",
    "1.29 How to Create an AI Influencer-10 Prompt",
    "06-cover-collage.jpeg",
)

# Card order (left to right)
IMAGE_FILES = [
    "04-man-ray.jpeg",        # Card 0: B&W surreal
    "01-guy-bourdin.jpeg",    # Card 1: Saturated RED
    "05-david-lachapelle.jpeg",  # Card 2: HERO - candy POP
    "02-helmut-newton.jpeg",  # Card 3: B&W urban
    "06-mario-testino.jpeg",  # Card 4: Gold warm
]


def round_corners(img, radius):
    """Apply rounded corners using an alpha mask."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.putalpha(mask)
    return img


def add_teal_border(img, border_width=BORDER_WIDTH, opacity=BORDER_OPACITY):
    """Draw a teal border inside the card edges."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    color = (*TEAL, opacity)
    draw.rounded_rectangle(
        [0, 0, w - 1, h - 1],
        radius=CORNER_RADIUS,
        outline=color,
        width=border_width,
    )
    return Image.alpha_composite(img, overlay)


def create_shadow(card_size, rotation, offset=SHADOW_OFFSET,
                  blur=SHADOW_BLUR, opacity=SHADOW_OPACITY):
    """Create a teal drop shadow for a rotated card."""
    w, h = card_size
    # Pad for blur spread
    pad = blur * 3
    shadow_canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    shadow_rect = Image.new("RGBA", (w, h), (*TEAL, opacity))
    # Apply rounded corners to shadow shape
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=CORNER_RADIUS, fill=255)
    shadow_rect.putalpha(mask)
    shadow_canvas.paste(shadow_rect, (pad + offset[0], pad + offset[1]))
    # Blur
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(radius=blur))
    # Rotate
    shadow_canvas = shadow_canvas.rotate(-rotation, resample=Image.BICUBIC, expand=True)
    return shadow_canvas


def create_radial_glow(canvas_size, center=None, radius=GLOW_RADIUS,
                       opacity=GLOW_OPACITY):
    """Create a subtle radial teal glow on the canvas center."""
    w, h = canvas_size
    if center is None:
        center = (w // 2, h // 2)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx, cy = center
    # Draw concentric circles with decreasing opacity
    for r in range(radius, 0, -1):
        alpha = int(opacity * (1 - (r / radius) ** 2))
        if alpha < 1:
            continue
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(*TEAL, alpha),
        )
        glow = Image.alpha_composite(glow, layer)
    return glow


def create_radial_glow_fast(canvas_size, center=None, radius=GLOW_RADIUS,
                            opacity=GLOW_OPACITY):
    """Faster radial glow using a small source scaled up + blurred."""
    w, h = canvas_size
    if center is None:
        center = (w // 2, h // 2)

    # Create a small dot and scale it up
    dot_size = 64
    dot = Image.new("RGBA", (dot_size, dot_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dot)
    r = dot_size // 4
    cx, cy = dot_size // 2, dot_size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*TEAL, opacity))

    # Scale to desired glow diameter
    glow_diam = radius * 2
    dot = dot.resize((glow_diam, glow_diam), Image.LANCZOS)
    dot = dot.filter(ImageFilter.GaussianBlur(radius=radius // 2))

    # Paste onto full canvas
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    paste_x = center[0] - glow_diam // 2
    paste_y = center[1] - glow_diam // 2
    glow.paste(dot, (paste_x, paste_y))
    return glow


def prepare_card_image(path, target_w, target_h):
    """Load, center-crop to target aspect ratio, and resize."""
    img = Image.open(path).convert("RGBA")
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider: crop width
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    elif src_ratio < target_ratio:
        # Source is taller: crop height
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)
    return img


def generate_collage_cover(image_paths, output_path):
    """Main composition function."""
    # 1. Create black RGBA canvas
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (*BG_COLOR, 255))

    # 2. Add subtle teal glow at center
    glow = create_radial_glow_fast(
        (CANVAS_W, CANVAS_H),
        center=(CANVAS_W // 2, VERTICAL_CENTER_Y),
    )
    canvas = Image.alpha_composite(canvas, glow)

    # 3. Prepare card positions and sizes
    cards = []
    for i in range(5):
        is_hero = (i == 2)
        scale = HERO_SCALE if is_hero else 1.0
        w = int(CARD_W * scale)
        h = int(CARD_H * scale)

        # Horizontal position: evenly spaced across HORIZONTAL_SPAN
        x_center = (CANVAS_W - HORIZONTAL_SPAN) // 2 + int(
            HORIZONTAL_SPAN * i / 4
        )
        # Vertical: arc effect (outer cards sit lower)
        dist_from_center = abs(i - 2)
        y_offset = int(ARC_DROP * dist_from_center)
        y_center = VERTICAL_CENTER_Y + y_offset

        angle = ROTATION_ANGLES[i]
        cards.append({
            "index": i,
            "path": image_paths[i],
            "w": w,
            "h": h,
            "x": x_center,
            "y": y_center,
            "angle": angle,
            "is_hero": is_hero,
        })

    # 4. Render order: outermost first, hero last (on top)
    render_order = [0, 4, 1, 3, 2]

    for idx in render_order:
        card = cards[idx]
        # Load and prepare image
        img = prepare_card_image(card["path"], card["w"], card["h"])
        # Round corners
        img = round_corners(img, CORNER_RADIUS)
        # Add teal border
        img = add_teal_border(img)

        # Create shadow
        shadow = create_shadow(
            (card["w"], card["h"]),
            card["angle"],
        )

        # Rotate card
        rotated = img.rotate(
            -card["angle"],
            resample=Image.BICUBIC,
            expand=True,
        )

        # Calculate paste position (centered on x,y)
        # Shadow
        sx = card["x"] - shadow.size[0] // 2
        sy = card["y"] - shadow.size[1] // 2
        canvas.paste(shadow, (sx, sy), shadow)

        # Card
        cx = card["x"] - rotated.size[0] // 2
        cy = card["y"] - rotated.size[1] // 2
        canvas.paste(rotated, (cx, cy), rotated)

    # 5. Convert to RGB and save
    final = canvas.convert("RGB")
    final.save(output_path, "JPEG", quality=92)
    print(f"Saved collage cover: {output_path}")
    print(f"Size: {final.size[0]}x{final.size[1]}")


def main():
    image_paths = [os.path.join(IMAGE_DIR, f) for f in IMAGE_FILES]
    # Verify all images exist
    for p in image_paths:
        if not os.path.exists(p):
            print(f"ERROR: Image not found: {p}")
            return
    generate_collage_cover(image_paths, OUTPUT_PATH)


if __name__ == "__main__":
    main()
