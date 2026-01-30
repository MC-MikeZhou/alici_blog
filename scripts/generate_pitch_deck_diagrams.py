#!/usr/bin/env python3
"""
Generate pitch-deck style blog diagrams as PNGs.

Why this exists:
- Image models are unreliable at rendering precise text.
- These diagrams must contain English labels, so we render them deterministically.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter


def _try_fonts() -> Iterable[str]:
    # Prefer clean UI / deck-like sans fonts available on macOS + common Linux.
    return [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = list(_try_fonts())
    if bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ] + candidates
    for p in candidates:
        try:
            return ImageFont.truetype(p, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _shadow_card(img: Image.Image, xy: Tuple[int, int, int, int], radius: int = 28) -> None:
    # Soft shadow behind a rounded rectangle, deck-like.
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = xy
    d.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow, (0, 0))


def _text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    s: str,
    font: ImageFont.ImageFont,
    fill: str,
    anchor: str = "la",
) -> None:
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)


def _wrap(draw: ImageDraw.ImageDraw, s: str, font: ImageFont.ImageFont, max_w: int) -> list[str]:
    words = s.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


@dataclass
class ManifestImage:
    id: str
    file_path: str
    status: str = "success"
    generation_model: str = "pillow/vector"
    original_prompt: str | None = None
    final_prompt: str | None = None
    cdn_url: str | None = None


def build_clickbait_map(out_path: Path) -> None:
    W, H = 1600, 900
    bg = (250, 252, 251)
    ink = (14, 30, 22)
    sub = (86, 104, 96)
    border = (226, 233, 229)
    card = (255, 255, 255)
    accent = (25, 197, 144)  # Alici-ish green/teal
    warn = (245, 84, 90)  # red
    gold = (244, 185, 76)

    img = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(img)

    title_f = _load_font(56, bold=True)
    h2_f = _load_font(28, bold=True)
    body_f = _load_font(24, bold=False)
    small_f = _load_font(20, bold=False)

    _text(d, (80, 70), "The Clickbait Map", title_f, fill=ink)
    _text(
        d,
        (80, 135),
        "Curiosity works. Deception backfires.",
        body_f,
        fill=sub,
    )

    # Main card
    card_xy = (80, 190, W - 80, H - 90)
    _shadow_card(img, card_xy, radius=34)
    d = ImageDraw.Draw(img)
    _rounded_rect(d, card_xy, radius=34, fill=_rgb(card), outline=_rgb(border), width=2)

    # Grid inside card
    pad = 46
    gx0, gy0, gx1, gy1 = card_xy[0] + pad, card_xy[1] + pad, card_xy[2] - pad, card_xy[3] - pad
    midx, midy = (gx0 + gx1) // 2, (gy0 + gy1) // 2

    # Axes
    axis_w = 6
    d.line((midx, gy0, midx, gy1), fill=_rgb(border), width=axis_w)
    d.line((gx0, midy, gx1, midy), fill=_rgb(border), width=axis_w)

    # Axis labels (match article: x = misleading/emotion, y = information withheld)
    _text(d, (midx, gy1 + 18), "Misleading / Emotional Manipulation  ->", small_f, fill=sub, anchor="ma")
    _text(d, (gx0, gy0 - 32), "Information withheld (more up)", small_f, fill=sub, anchor="la")

    # Quadrant labels + copy
    def quad_label(cx: int, cy: int, label: str, color: Tuple[int, int, int], blurb: str) -> None:
        box_w, box_h = 520, 220
        bx0, by0 = cx - box_w // 2, cy - box_h // 2
        bx1, by1 = bx0 + box_w, by0 + box_h
        # subtle inset card
        _rounded_rect(d, (bx0, by0, bx1, by1), radius=24, fill=(248, 250, 249), outline=_rgb(border), width=2)
        _text(d, (bx0 + 26, by0 + 26), label, h2_f, fill=color)
        lines = _wrap(d, blurb, body_f, max_w=box_w - 52)
        yy = by0 + 74
        for ln in lines[:3]:
            _text(d, (bx0 + 26, yy), ln, body_f, fill=ink)
            yy += 34

    # Quadrant centers
    qdx = (midx - gx0) // 2
    qdy = (midy - gy0) // 2

    # Bottom-left: BLIND SPOT (low withheld, low misleading)
    quad_label(
        gx0 + qdx,
        midy + qdy,
        "BLIND SPOT",
        _rgb(gold),
        "Nothing at stake. Viewers skip because there is no hook.",
    )
    # Bottom-right: HYPE (low withheld, higher emotion)
    quad_label(
        midx + qdx,
        midy + qdy,
        "HYPE",
        _rgb(warn),
        "Big emotion + big claims. Clicks rise, but trust can drop fast.",
    )
    # Top-right: CLICK TRAP (high withheld, high misleading)
    quad_label(
        midx + qdx,
        gy0 + qdy,
        "CLICK TRAP",
        _rgb(warn),
        "High curiosity + high deception. Short-term wins, long-term damage.",
    )
    # Top-left: ETHICAL CLICKBAIT (highlight, high withheld + low misleading)
    # highlight frame
    hi_w, hi_h = 560, 250
    hi_cx, hi_cy = gx0 + qdx, gy0 + qdy
    hx0, hy0 = hi_cx - hi_w // 2, hi_cy - hi_h // 2
    hx1, hy1 = hx0 + hi_w, hy0 + hi_h
    d.rounded_rectangle((hx0 - 8, hy0 - 8, hx1 + 8, hy1 + 8), radius=30, outline=_rgb(accent), width=6)
    quad_label(
        hi_cx,
        hi_cy,
        "ETHICAL CLICKBAIT",
        _rgb(accent),
        "A clear promise + a real payoff. Curiosity without deception.",
    )

    # Sweet spot callout
    call_xy = (W - 600, 110, W - 80, 180)
    _shadow_card(img, call_xy, radius=22)
    d = ImageDraw.Draw(img)
    _rounded_rect(d, call_xy, radius=22, fill=(255, 255, 255), outline=_rgb(border), width=2)
    _text(d, (call_xy[0] + 22, call_xy[1] + 22), "Sweet spot:", h2_f, fill=_rgb(accent))
    _text(d, (call_xy[0] + 190, call_xy[1] + 26), "Curiosity without deception", body_f, fill=ink)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)


def build_3_variant_loop(out_path: Path) -> None:
    W, H = 1600, 900
    bg = (250, 252, 251)
    ink = (14, 30, 22)
    sub = (86, 104, 96)
    border = (226, 233, 229)
    card = (255, 255, 255)
    accent = (25, 197, 144)

    img = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(img)

    title_f = _load_font(56, bold=True)
    h2_f = _load_font(28, bold=True)
    body_f = _load_font(24, bold=False)
    small_f = _load_font(20, bold=False)

    _text(d, (80, 70), "The 3-Variant Loop", title_f, fill=ink)
    _text(d, (80, 135), "A simple workflow for iterative thumbnail gains.", body_f, fill=sub)

    # Main card
    card_xy = (80, 190, W - 80, H - 90)
    _shadow_card(img, card_xy, radius=34)
    d = ImageDraw.Draw(img)
    _rounded_rect(d, card_xy, radius=34, fill=_rgb(card), outline=_rgb(border), width=2)

    cx, cy = (W // 2), (H // 2) + 40
    r = 260

    steps = [
        ("1", "Make 3 Variants", "Different hook, same topic."),
        ("2", "Publish", "Keep the title fixed."),
        ("3", "Watch Metrics", "CTR + AVD + retention."),
        ("4", "Change ONE Thing", "Swap one element only."),
        ("5", "Log & Keep Winner", "Build an asset library."),
    ]

    # Place 5 step cards around a circle
    card_w, card_h = 360, 140
    for i, (num, head, desc) in enumerate(steps):
        ang = (-90 + i * (360 / len(steps))) * math.pi / 180
        px = int(cx + r * math.cos(ang))
        py = int(cy + r * math.sin(ang))
        bx0, by0 = px - card_w // 2, py - card_h // 2
        bx1, by1 = bx0 + card_w, by0 + card_h

        # shadow + card
        _shadow_card(img, (bx0, by0, bx1, by1), radius=24)
        d = ImageDraw.Draw(img)
        _rounded_rect(d, (bx0, by0, bx1, by1), radius=24, fill=(255, 255, 255), outline=_rgb(border), width=2)

        # number pill
        pill_xy = (bx0 + 18, by0 + 18, bx0 + 64, by0 + 52)
        d.rounded_rectangle(pill_xy, radius=16, fill=_rgb(accent))
        _text(d, (bx0 + 41, by0 + 35), num, _load_font(20, bold=True), fill=(255, 255, 255), anchor="mm")

        _text(d, (bx0 + 78, by0 + 20), head, h2_f, fill=ink)
        lines = _wrap(d, desc, body_f, max_w=card_w - 98)
        yy = by0 + 62
        for ln in lines[:2]:
            _text(d, (bx0 + 78, yy), ln, body_f, fill=sub)
            yy += 32

    # Arrows between steps
    d = ImageDraw.Draw(img)
    for i in range(len(steps)):
        ang1 = (-90 + i * (360 / len(steps))) * math.pi / 180
        ang2 = (-90 + ((i + 1) % len(steps)) * (360 / len(steps))) * math.pi / 180
        x1 = cx + (r - 110) * math.cos(ang1)
        y1 = cy + (r - 110) * math.sin(ang1)
        x2 = cx + (r - 110) * math.cos(ang2)
        y2 = cy + (r - 110) * math.sin(ang2)
        d.line((x1, y1, x2, y2), fill=_rgb(accent), width=6)
        # arrow head
        ah = 18
        ax, ay = x2, y2
        # direction from x1,y1 to x2,y2
        dx, dy = x2 - x1, y2 - y1
        norm = math.hypot(dx, dy) or 1.0
        ux, uy = dx / norm, dy / norm
        # perpendicular
        px, py = -uy, ux
        p1 = (ax - ux * ah - px * (ah * 0.6), ay - uy * ah - py * (ah * 0.6))
        p2 = (ax - ux * ah + px * (ah * 0.6), ay - uy * ah + py * (ah * 0.6))
        d.polygon([ (ax, ay), p1, p2 ], fill=_rgb(accent))

    # Center note
    note_xy = (cx - 290, cy - 60, cx + 290, cy + 70)
    _shadow_card(img, note_xy, radius=22)
    d = ImageDraw.Draw(img)
    _rounded_rect(d, note_xy, radius=22, fill=(255, 255, 255), outline=_rgb(border), width=2)
    _text(d, (cx, cy - 12), "Change ONE variable at a time", h2_f, fill=_rgb(accent), anchor="mm")
    _text(d, (cx, cy + 28), "Don't change title + thumbnail together.", body_f, fill=sub, anchor="mm")

    # Footer
    _text(d, (W - 90, H - 50), "alici.ai", small_f, fill=sub, anchor="ra")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)


def _rgb(c) -> Tuple[int, int, int]:
    if isinstance(c, tuple):
        return c[:3]
    raise TypeError("color must be tuple")


def write_manifest(manifest_path: Path, images: list[ManifestImage]) -> None:
    payload = {
        "images": [asdict(i) for i in images],
        "summary": {
            "total_planned": len(images),
            "total_generated": sum(1 for i in images if i.status == "success"),
            "success_rate": f"{int(100 * (sum(1 for i in images if i.status == 'success') / max(1, len(images))))}%",
        },
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True, help="Output directory for PNGs and manifest.")
    ap.add_argument("--slug", default="veritasium-clickbait", help="Asset subfolder name.")
    args = ap.parse_args()

    out_root = Path(args.out_dir).expanduser().resolve()
    asset_dir = out_root / "assets" / args.slug
    asset_dir.mkdir(parents=True, exist_ok=True)

    img1 = asset_dir / "concept-clickbait-map.png"
    img2 = asset_dir / "workflow-3-variant-loop.png"

    build_clickbait_map(img1)
    build_3_variant_loop(img2)

    manifest_path = out_root / "asset_manifest.json"
    write_manifest(
        manifest_path,
        [
            ManifestImage(id="concept-clickbait-map", file_path=str(img1.relative_to(out_root))),
            ManifestImage(id="workflow-3-variant-loop", file_path=str(img2.relative_to(out_root))),
        ],
    )

    print(f"Wrote: {img1}")
    print(f"Wrote: {img2}")
    print(f"Wrote: {manifest_path}")


if __name__ == "__main__":
    main()
