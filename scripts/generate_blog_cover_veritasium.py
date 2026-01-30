#!/usr/bin/env python3
"""
Generate a blog cover (16:9) inspired by a "presenter + chart + big headline" composition.

Design goals:
- English text rendered deterministically (AI models often mangle typography).
- Alici green-forward background (no white background).
- High-contrast, thumbnail-like readability.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def _try_fonts():
    return [
        "/System/Library/Fonts/Supplemental/Helvetica Neue Condensed Black.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Black.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]


def _font(size: int, bold: bool = True):
    for p in _try_fonts():
        try:
            return ImageFont.truetype(p, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _rgb(t) -> Tuple[int, int, int]:
    return t[:3]


def _rounded(draw: ImageDraw.ImageDraw, xy, r, fill, outline=None, w=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


def _shadow_card(base: Image.Image, xy, r=34, alpha=70, blur=18, dy=10):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    x0, y0, x1, y1 = xy
    d.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=r, fill=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh)


def _linear_gradient(size, c1, c2, angle_deg=20):
    w, h = size
    img = Image.new("RGB", (w, h), c1)
    px = img.load()
    ang = math.radians(angle_deg)
    ux, uy = math.cos(ang), math.sin(ang)
    for y in range(h):
        for x in range(w):
            t = (x * ux + y * uy) / (w * ux + h * uy)
            t = max(0.0, min(1.0, t))
            px[x, y] = (
                int(c1[0] + (c2[0] - c1[0]) * t),
                int(c1[1] + (c2[1] - c1[1]) * t),
                int(c1[2] + (c2[2] - c1[2]) * t),
            )
    return img


def _add_grain(img: Image.Image, strength=18):
    # Subtle film grain so the green doesn't look flat.
    import random

    w, h = img.size
    g = Image.new("L", (w, h), 128)
    gp = g.load()
    for y in range(h):
        for x in range(w):
            gp[x, y] = max(0, min(255, 128 + random.randint(-strength, strength)))
    grain = g.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.composite(img, Image.new("RGB", (w, h), (0, 0, 0)), grain.point(lambda v: int((v - 128) * 0.06 + 128)))
    return img


def _draw_presenter_silhouette(base: Image.Image, anchor_xy=(260, 520)):
    """
    Draw a stylized presenter silhouette with a strong shadow, pointing to the chart.
    This is intentionally "generic" (no real-person likeness).
    """
    w, h = base.size
    x, y = anchor_xy
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    suit = (13, 28, 22, 255)
    edge = (255, 255, 255, 40)

    # Head
    d.ellipse((x - 70, y - 340, x + 10, y - 260), fill=suit)
    # Neck
    _rounded(d, (x - 40, y - 270, x - 20, y - 235), 10, fill=suit)
    # Torso
    _rounded(d, (x - 120, y - 240, x + 60, y + 120), 50, fill=suit)
    # Shoulder / upper arm (pointing)
    arm = [(x + 10, y - 170), (x + 250, y - 240), (x + 285, y - 205), (x + 35, y - 135)]
    d.polygon(arm, fill=suit)
    # Forearm / hand
    fore = [(x + 260, y - 240), (x + 390, y - 260), (x + 405, y - 225), (x + 285, y - 205)]
    d.polygon(fore, fill=suit)
    # Tiny finger "point"
    d.polygon([(x + 398, y - 255), (x + 455, y - 262), (x + 457, y - 242)], fill=suit)

    # Lower body
    _rounded(d, (x - 95, y + 110, x + 30, y + 320), 40, fill=suit)

    # Strong shadow behind (offset left/up like the reference)
    sh = layer.copy()
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    # Tint shadow a bit lighter to read on green.
    sh = Image.eval(sh, lambda v: int(v * 0.75))
    base.alpha_composite(sh, (-80, -20))
    base.alpha_composite(layer)

    # Subtle edge highlight so it doesn't blend into green.
    edge_layer = layer.filter(ImageFilter.GaussianBlur(1.4))
    edge_layer = Image.eval(edge_layer, lambda v: int(v * 0.25))
    base.alpha_composite(edge_layer, (2, 2))


def _draw_chart(base: Image.Image, xy):
    x0, y0, x1, y1 = xy
    d = ImageDraw.Draw(base)
    border = (231, 238, 234)
    card = (255, 255, 255)
    accent = (25, 197, 144)
    cyan = (62, 210, 235)
    arrow = (255, 88, 84)

    _shadow_card(base, xy, r=38, alpha=95, blur=20, dy=14)
    d = ImageDraw.Draw(base)
    _rounded(d, xy, 38, fill=card, outline=border, w=2)

    pad = 46
    gx0, gy0, gx1, gy1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad

    # Grid lines
    for i in range(1, 5):
        yy = int(gy0 + (gy1 - gy0) * (i / 5))
        d.line((gx0, yy, gx1, yy), fill=(232, 238, 235), width=2)

    # Curve (stylized)
    pts = [
        (gx0 + 0, gy1 - 30),
        (gx0 + 220, gy1 - 60),
        (gx0 + 420, gy1 - 85),
        (gx0 + 560, gy1 - 260),  # kink
        (gx0 + 720, gy1 - 340),
        (gx0 + 900, gy1 - 390),
        (gx1 - 20, gy1 - 430),
    ]

    # Fill under curve
    poly = pts + [(pts[-1][0], gy1), (gx0, gy1)]
    fill = Image.new("RGBA", base.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fill)
    fd.polygon(poly, fill=(cyan[0], cyan[1], cyan[2], 90))
    base.alpha_composite(fill)

    # Curve stroke
    d.line(pts, fill=accent, width=10, joint="curve")

    # Highlight point + arrow
    hx, hy = pts[3]
    d.ellipse((hx - 12, hy - 12, hx + 12, hy + 12), fill=(255, 255, 255), outline=accent, width=4)
    d.polygon([(hx - 60, hy + 150), (hx + 60, hy + 150), (hx, hy + 60)], fill=arrow)


def build_cover(out_path: Path) -> None:
    W, H = 1600, 900
    # Alici green-forward background (noticeable, not neon).
    bg = _linear_gradient((W, H), (8, 88, 60), (21, 197, 144), angle_deg=24)
    bg = _add_grain(bg, strength=14)
    base = bg.convert("RGBA")

    d = ImageDraw.Draw(base)

    # Headline (English, high-contrast)
    title = "WHY YOU CLICK"
    subtitle = "The Veritasium Thumbnail Method"

    title_f = _font(118, bold=True)
    sub_f = _font(44, bold=False)

    # Title shadow for punch
    tx, ty = 130, 70
    d.text((tx + 4, ty + 6), title, font=title_f, fill=(0, 0, 0, 85))
    d.text((tx, ty), title, font=title_f, fill=(255, 255, 255, 245))

    d.text((tx, ty + 128), subtitle, font=sub_f, fill=(232, 255, 248, 225))

    # Presenter silhouette on left
    _draw_presenter_silhouette(base, anchor_xy=(300, 590))

    # Chart card on right
    _draw_chart(base, (560, 220, 1510, 820))

    # Small brand tag
    tag_f = _font(30, bold=True)
    d = ImageDraw.Draw(base)
    d.text((W - 120, H - 70), "alici.ai", font=tag_f, fill=(232, 255, 248, 210), anchor="ra")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "PNG", optimize=True)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output PNG path")
    args = ap.parse_args()
    build_cover(Path(args.out).expanduser().resolve())
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()

