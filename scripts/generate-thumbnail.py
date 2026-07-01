#!/usr/bin/env python3
"""Generate professional OG thumbnail and favicons for the portfolio."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GREY = (130, 130, 130)
GREY_LIGHT = (170, 170, 170)

NAME = "Terence Liu"
ROLE = "Information Management · Student"
HEADLINE = (
    "HKU Information Management · Multimedia Design · "
    "Data Analytics · Marketing"
)
TOP_BAR = "Hong Kong  |  +852 6050 3732  |  lkwterence@gmail.com"
SECTION_LABEL = "INFORMATION MANAGEMENT"


def load_font(size: int, weight: str = "regular"):
    paths: list[str]
    if weight == "black":
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Black.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Black.ttf",
        ]
    elif weight == "bold":
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    elif weight == "light":
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/HelveticaNeueLight.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font) -> float:
    return draw.textlength(text, font=font)


def draw_right(
    draw: ImageDraw.ImageDraw,
    right_x: int,
    y: int,
    text: str,
    font,
    fill: tuple[int, int, int],
) -> None:
    width = text_width(draw, text, font)
    draw.text((right_x - width, y), text, font=font, fill=fill)


def wrap_text(
    text: str, font, max_width: int, draw: ImageDraw.ImageDraw
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if text_width(draw, trial, font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int,
    weight: str = "black",
) -> object:
    size = start_size
    while size > 40:
        font = load_font(size, weight)
        if text_width(draw, text, font) <= max_width:
            return font
        size -= 4
    return load_font(40, weight)


def build_og_thumbnail() -> None:
    w, h = 1200, 630
    canvas = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(canvas)

    margin_left = 72
    margin_right = 72
    content_right = w - margin_right

    top_font = load_font(20, "light")
    draw.text((margin_left, 44), TOP_BAR, font=top_font, fill=GREY_LIGHT)

    portfolio_font = fit_font_size(
        draw, "Portfolio", w - margin_left - margin_right, 196, "black"
    )
    portfolio_bbox = draw.textbbox((0, 0), "Portfolio", font=portfolio_font)
    portfolio_h = portfolio_bbox[3] - portfolio_bbox[1]
    draw.text((margin_left, 108), "Portfolio", font=portfolio_font, fill=BLACK)

    block_top = 108 + portfolio_h + 52
    block_width = 400
    block_left = content_right - block_width

    dash_y = block_top + 8
    draw.line((block_left, dash_y, block_left + 52, dash_y), fill=BLACK, width=3)

    name_font = load_font(38, "bold")
    draw.text((block_left, block_top + 28), NAME, font=name_font, fill=BLACK)

    role_font = load_font(22, "regular")
    draw.text((block_left, block_top + 78), ROLE, font=role_font, fill=GREY)

    section_top = block_top + 148
    label_font = load_font(18, "bold")
    draw.text((block_left, section_top), SECTION_LABEL, font=label_font, fill=BLACK)

    body_font = load_font(15, "light")
    body_lines = wrap_text(HEADLINE, body_font, block_width, draw)
    body_y = section_top + 34
    line_height = 22
    for line in body_lines:
        draw.text((block_left, body_y), line, font=body_font, fill=GREY)
        body_y += line_height

    canvas.save(OUT / "og-thumbnail.jpg", "JPEG", quality=94)


def build_icons() -> None:
    size = 512
    canvas = Image.new("RGB", (size, size), WHITE)
    draw = ImageDraw.Draw(canvas)

    mono_font = load_font(196, "black")
    text = "TL"
    bbox = draw.textbbox((0, 0), text, font=mono_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        text,
        font=mono_font,
        fill=BLACK,
    )

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
