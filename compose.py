#!/usr/bin/env python3
"""TALASSA - The Stairway of the Sea. Deterministic vintage travel poster.

A grand stone staircase rises out of the ocean into the sky, ending at a
lighthouse on a rocky islet. One impossible central image, huge cream title,
warm gold light against deep indigo sea and sky, cream frame.
Fixed seed 20261121. No network. PIL only. Output: entry.png, 1024x1024.
"""
import random
from PIL import Image, ImageDraw, ImageFont

SEED = 20261121
W = H = 1024
OUT = "entry.png"

CREAM = (243, 232, 206)
CREAM_TITLE = (247, 239, 216)
PAPER_DARK = (27, 42, 82)
SKY_TOP = (22, 38, 78)
SKY_BOT = (44, 78, 126)
SEA_TOP = (27, 74, 107)
SEA_BOT = (15, 46, 74)
GOLD = (242, 183, 5)
GOLD_SOFT = (247, 215, 116)
CORAL = (228, 87, 46)
STONE = (233, 221, 190)
STONE_SHADOW = (198, 180, 143)
ROCK = (58, 63, 74)
WHITE = (250, 248, 240)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, box, c_top, c_bot):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(c_top, c_bot, (y - y0) / max(1, y1 - y0)))


def spaced_text(d, cx, y, text, font, fill, tracking=8):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def main():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- scene area inside the cream frame ---
    S = 28  # frame width
    vgrad(d, (S, S, W - S, 600), SKY_TOP, SKY_BOT)      # sky
    vgrad(d, (S, 600, W - S, H - S), SEA_TOP, SEA_BOT)  # sea
    d.line([(S, 600), (W - S, 600)], fill=GOLD, width=3)

    # stars in the upper sky
    for _ in range(46):
        x = rng.randint(S + 12, W - S - 12)
        y = rng.randint(S + 12, 330)
        r = rng.choice([1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM_TITLE)

    # birds
    for bx, by, s in [(330, 250, 14), (380, 285, 10), (880, 210, 12), (840, 260, 9)]:
        d.line([(bx - s, by), (bx, by - s // 2), (bx + s, by)], fill=PAPER_DARK, width=3)

    # low sun, left, over the horizon + its reflection on the sea
    sx, sy, sr = 215, 545, 62
    for rr, col in [(sr + 26, (64, 100, 150)), (sr + 12, (120, 140, 170))]:
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], outline=col, width=3)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
    for wy, ww in [(640, 150), (690, 210), (750, 120), (820, 180)]:
        d.line([(sx - ww // 2, wy), (sx + ww // 2, wy)], fill=GOLD_SOFT, width=5)

    # --- the staircase: 15 stone steps on a diagonal ramp, sea to islet ---
    x0, y_base = 140, H - S
    dx, dy, n = 38, 44, 15
    d.line([(159, 974), (691, 358)], fill=STONE_SHADOW, width=30)
    for i in range(n):
        left = x0 + i * dx
        top = y_base - (i + 1) * dy
        right = left + dx
        bottom = y_base - i * dy
        d.rectangle([left, top, right, bottom], fill=STONE)
        d.line([(left, top), (right, top)], fill=GOLD_SOFT, width=3)
        d.line([(right, top), (right, bottom)], fill=STONE_SHADOW, width=3)
    # handrail along the stepped top edge
    hx0, hy0 = x0, y_base - dy - 34
    hx1, hy1 = x0 + n * dx, y_base - n * dy - 34
    d.line([(hx0, hy0), (hx1, hy1)], fill=PAPER_DARK, width=6)
    for i in range(0, n, 2):
        px = x0 + i * dx + dx // 2
        py = y_base - i * dy - dy
        rail_y = hy0 + (px - hx0) * (hy1 - hy0) // (hx1 - hx0)
        d.line([(px, rail_y), (px, py)], fill=PAPER_DARK, width=4)

    # rocky islet at the top of the stairs
    d.polygon([(650, 382), (700, 340), (820, 336), (900, 382), (650, 382)], fill=ROCK)
    d.line([(690, 366), (840, 352)], fill=STONE, width=3)

    # lighthouse beams first (tower drawn over them)
    lx = 800
    d.polygon([(lx, 240), (480, 520), (480, 560), (lx, 255)], fill=GOLD_SOFT)
    d.polygon([(lx, 240), (W - S, 330), (W - S, 380), (lx, 255)], fill=GOLD_SOFT)
    # tapered tower, cream with two coral bands
    d.polygon([(lx - 24, 380), (lx - 15, 250), (lx + 15, 250), (lx + 24, 380)],
              fill=CREAM_TITLE)
    d.polygon([(lx - 21, 342), (lx - 18, 314), (lx + 18, 314), (lx + 21, 342)], fill=CORAL)
    d.polygon([(lx - 18, 296), (lx - 16, 272), (lx + 16, 272), (lx + 18, 296)], fill=CORAL)
    # lamp room + glow
    for rr in (40, 26):
        d.ellipse([lx - rr, 240 - rr, lx + rr, 240 + rr], outline=GOLD_SOFT, width=3)
    d.rectangle([lx - 20, 218, lx + 20, 252], fill=PAPER_DARK)
    d.ellipse([lx - 11, 226, lx + 11, 250], fill=GOLD)
    d.polygon([(lx - 26, 218), (lx + 26, 218), (lx + 18, 202), (lx - 18, 202)],
              fill=PAPER_DARK)

    # tiny people climbing the stairs
    for i, col in [(2, CORAL), (5, PAPER_DARK), (8, CORAL), (11, (90, 60, 40))]:
        px = x0 + i * dx + dx // 2
        py = y_base - (i + 1) * dy
        d.ellipse([px - 4, py - 16, px + 4, py - 8], fill=col)
        d.rectangle([px - 4, py - 8, px + 4, py + 2], fill=col)

    # sailboats on the sea
    for bx, by, s, sail in [(270, 740, 46, WHITE), (880, 780, 38, GOLD_SOFT),
                            (540, 880, 30, WHITE)]:
        d.polygon([(bx, by - s), (bx, by - 6), (bx + s // 2, by - 6)], fill=sail)
        d.polygon([(bx - s // 2, by), (bx + s // 2, by), (bx + s // 3, by + 12),
                   (bx - s // 3, by + 12)], fill=PAPER_DARK)

    # --- typography ---
    title_font = ImageFont.truetype(SERIF_BOLD, 128)
    sub_font = ImageFont.truetype(SERIF_BOLD, 30)
    tag_font = ImageFont.truetype(SERIF, 24)
    spaced_text(d, W // 2, 62, "TALASSA", title_font, CREAM_TITLE, tracking=10)
    d.line([(W // 2 - 445, 215), (W // 2 - 335, 215)], fill=GOLD, width=3)
    d.line([(W // 2 + 335, 215), (W // 2 + 445, 215)], fill=GOLD, width=3)
    spaced_text(d, W // 2, 200, "THE STAIRWAY OF THE SEA", sub_font,
                CREAM_TITLE, tracking=6)
    spaced_text(d, W // 2, 946, "VISIT THE PLACE THAT ISN'T THERE", tag_font,
                CREAM_TITLE, tracking=4)

    # thin dark inner rule around the scene
    d.rectangle([S + 12, S + 12, W - S - 12, H - S - 12], outline=PAPER_DARK, width=3)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
