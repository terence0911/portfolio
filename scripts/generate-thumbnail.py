#!/usr/bin/env python3
"""Generate artsy OG thumbnail and favicons from portfolio photos."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images"
OUT = ROOT / "assets"

CREAM = (248, 245, 239)
BROWN = (77, 71, 46)
GOLD = (239, 205, 61)
AMBER = (145, 113, 60)


def load_font(size: int, bold: bool = False):
    paths = (
        ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf", "/System/Library/Fonts/Supplemental/Georgia.ttf"]
        if bold
        else ["/System/Library/Fonts/Supplemental/Georgia.ttf"]
    )
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def load_crop(path: Path, size: tuple[int, int], focus: str = "center") -> Image.Image:
    im = Image.open(path).convert("RGB")
    cy = 0.32 if focus == "top" else 0.5
    return ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=(0.5, cy))


def warm_grade(im: Image.Image, strength: float = 0.55) -> Image.Image:
    r, g, b = im.split()
    warm = Image.merge(
        "RGB",
        (
            r.point(lambda p: min(255, int(p * 1.06 + 14))),
            g.point(lambda p: min(255, int(p * 0.98 + 8))),
            b.point(lambda p: max(0, int(p * 0.86))),
        ),
    )
    return Image.blend(im, warm, strength)


def vignette(im: Image.Image, strength: float = 0.4) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((-w * 0.2, -h * 0.15, w * 1.2, h * 1.15), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 5))
    dark = Image.new("RGB", (w, h), (36, 32, 22))
    return Image.composite(im, dark, mask.point(lambda p: int(255 - p * strength)))


def grain(im: Image.Image) -> Image.Image:
    noise = Image.effect_noise(im.size, 16).convert("RGB")
    return Image.blend(im, noise, 0.05)


def build_og_thumbnail() -> None:
    w, h = 1200, 630
    canvas = Image.new("RGB", (w, h), CREAM)

    bg = warm_grade(load_crop(IMG_DIR / "travel-nature-2.jpg", (w, h)), 0.7)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=6))
    bg = ImageEnhance.Brightness(bg).enhance(1.08)
    canvas = Image.blend(canvas, bg, 0.85)

    portrait = warm_grade(load_crop(IMG_DIR / "about-portrait.jpg", (480, h), "top"), 0.55)
    portrait = vignette(portrait, 0.28)
    canvas.paste(portrait, (0, 0))

    rule = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(rule).rectangle((468, 48, 476, h - 48), fill=(*GOLD, 255))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), rule).convert("RGB")

    inset = warm_grade(load_crop(IMG_DIR / "gallery-art-1.jpg", (280, 210)), 0.4)
    inset = ImageOps.expand(inset, border=10, fill=CREAM)
    inset = ImageOps.expand(inset, border=2, fill=BROWN)
    inset = inset.rotate(-4, expand=True, fillcolor=CREAM)
    canvas.paste(inset, (w - 340, h - 250))

    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle((510, 110, w - 70, 400), radius=18, fill=(*CREAM, 235))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), panel).convert("RGB")

    draw = ImageDraw.Draw(canvas)
    draw.text((560, 150), "Terence", font=load_font(86, bold=True), fill=BROWN)
    draw.text((560, 235), "Liu", font=load_font(86, bold=True), fill=BROWN)
    draw.line((560, 330, 760, 330), fill=GOLD, width=3)
    draw.text((560, 350), "Information Management", font=load_font(26), fill=AMBER)
    draw.text((560, 388), "HKU · Portfolio", font=load_font(20), fill=(100, 92, 62))

    canvas = grain(vignette(canvas, 0.18))
    canvas.save(OUT / "og-thumbnail.jpg", "JPEG", quality=93)


def build_icons() -> None:
    size = 512
    icon = warm_grade(load_crop(IMG_DIR / "about-portrait.jpg", (size, size), "top"), 0.62)
    icon = vignette(icon, 0.32)
    framed = ImageOps.expand(icon, border=14, fill=CREAM)
    framed = ImageOps.expand(framed, border=5, fill=GOLD)
    framed = framed.resize((size, size), Image.Resampling.LANCZOS)
    framed.save(OUT / "icon-512.png", "PNG")
    for sz, name in [(180, "apple-touch-icon.png"), (32, "favicon-32.png"), (16, "favicon-16.png")]:
        framed.resize((sz, sz), Image.Resampling.LANCZOS).save(OUT / name, "PNG")
    framed.resize((32, 32), Image.Resampling.LANCZOS).save(
        OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)]
    )


def main() -> None:
    build_og_thumbnail()
    build_icons()
    print(f"Wrote thumbnail assets to {OUT}")


if __name__ == "__main__":
    main()
