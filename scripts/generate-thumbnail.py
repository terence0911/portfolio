#!/usr/bin/env python3
"""Generate professional OG thumbnail and favicons for the portfolio."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images"
OUT = ROOT / "assets"

CREAM = (248, 245, 239)
BROWN_DARK = (77, 71, 46)
BROWN = (145, 113, 60)
GOLD = (239, 205, 61)
MUTED = (108, 100, 78)

HEADLINE = "HKU Information Management | Multimedia Design • Data Analytics • Marketing"


def load_font(size: int, bold: bool = False, sans: bool = False):
    if sans:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    elif bold:
        paths = [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
        ]
    else:
        paths = ["/System/Library/Fonts/Supplemental/Georgia.ttf"]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def load_crop(path: Path, size: tuple[int, int]) -> Image.Image:
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def warm_grade(im: Image.Image, strength: float = 0.45) -> Image.Image:
    r, g, b = im.split()
    warm = Image.merge(
        "RGB",
        (
            r.point(lambda p: min(255, int(p * 1.04 + 10))),
            g.point(lambda p: min(255, int(p * 0.99 + 5))),
            b.point(lambda p: max(0, int(p * 0.9))),
        ),
    )
    return Image.blend(im, warm, strength)


def wrap_text(text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    if "|" in text:
        return [part.strip() for part in text.split("|")]

    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def build_og_thumbnail() -> None:
    w, h = 1200, 630
    canvas = Image.new("RGB", (w, h), CREAM)

    # Subtle texture — heavily blurred landscape, no identifiable subjects
    texture = warm_grade(load_crop(IMG_DIR / "travel-nature-2.jpg", (w, h)), 0.55)
    texture = texture.filter(ImageFilter.GaussianBlur(radius=28))
    texture = ImageEnhance.Brightness(texture).enhance(1.12)
    texture = ImageEnhance.Contrast(texture).enhance(0.75)
    canvas = Image.blend(canvas, texture, 0.35)

    # Left accent band
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 10, h), fill=GOLD)
    draw.rectangle((10, 0, 14, h), fill=BROWN_DARK)

    # Content block
    margin_x = 96
    name_font = load_font(92, bold=True)
    headline_font = load_font(28, sans=True)
    label_font = load_font(22, sans=True)

    draw.text((margin_x, 168), "Terence Liu", font=name_font, fill=BROWN_DARK)
    draw.line((margin_x, 278, margin_x + 220, 278), fill=GOLD, width=4)

    lines = wrap_text(HEADLINE, headline_font, w - margin_x * 2, draw)
    y = 310
    for line in lines:
        draw.text((margin_x, y), line, font=headline_font, fill=BROWN)
        y += 42

    draw.text((margin_x, h - 72), "Portfolio", font=label_font, fill=MUTED)

    # Bottom rule
    draw.rectangle((margin_x, h - 48, w - margin_x, h - 46), fill=GOLD)

    canvas.save(OUT / "og-thumbnail.jpg", "JPEG", quality=94)


def build_icons() -> None:
    size = 512
    canvas = Image.new("RGB", (size, size), CREAM)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, size, 12), fill=GOLD)
    draw.rectangle((0, 12, size, 16), fill=BROWN_DARK)

    mono_font = load_font(200, bold=True)
    text = "TL"
    bbox = draw.textbbox((0, 0), text, font=mono_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1] - 10), text, font=mono_font, fill=BROWN_DARK)

    draw.rectangle((48, size - 20, size - 48, size - 16), fill=GOLD)

    canvas.save(OUT / "icon-512.png", "PNG")
    for sz, name in [(180, "apple-touch-icon.png"), (32, "favicon-32.png"), (16, "favicon-16.png")]:
        canvas.resize((sz, sz), Image.Resampling.LANCZOS).save(OUT / name, "PNG")
    canvas.resize((32, 32), Image.Resampling.LANCZOS).save(
        OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)]
    )


def main() -> None:
    build_og_thumbnail()
    build_icons()
    print(f"Wrote thumbnail assets to {OUT}")


if __name__ == "__main__":
    main()
