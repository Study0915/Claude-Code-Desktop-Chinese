#!/usr/bin/env python3
"""Generate simple project icon using Pillow."""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not available. Please install: pip install Pillow")
    raise SystemExit(1)


def create_icon(size: int, output: Path) -> None:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded rect background (Anthropic purple-ish)
    margin = size // 16
    radius = size // 8
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(20, 20, 35, 255),
        outline=(100, 90, 180, 255),
        width=max(2, size // 64),
    )

    # Draw "中" character
    try:
        font = ImageFont.truetype("msyh.ttc", size=int(size * 0.55))
    except OSError:
        font = ImageFont.load_default()

    text = "中"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2
    y = (size - text_h) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=(230, 230, 250, 255))

    # Draw "Claude" mini text at bottom
    mini_font_size = max(8, size // 14)
    try:
        mini_font = ImageFont.truetype("msyh.ttc", mini_font_size)
    except OSError:
        mini_font = ImageFont.load_default()

    label = "Claude"
    lbbox = draw.textbbox((0, 0), label, font=mini_font)
    lw = lbbox[2] - lbbox[0]
    lh = lbbox[3] - lbbox[1]
    lx = (size - lw) // 2
    ly = size - margin - lh - 2
    draw.text((lx, ly), label, font=mini_font, fill=(150, 150, 200, 255))

    img.save(output, "PNG")
    print(f"Created: {output}")


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "resources"
    out_dir.mkdir(exist_ok=True)
    create_icon(256, out_dir / "icon-256.png")
    create_icon(64, out_dir / "icon-64.png")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())