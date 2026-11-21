#!/usr/bin/env python3
"""ANCHORA — The Lighthouse Anchor. Deterministic PIL travel poster, 1024x1024.
No network, fixed seed. Renders /output/entry.png (or argv[1])."""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

SEED = 20261121
W = H = 1024
FRAME = 14
CREAM = (244, 233, 205)
GOLD = (232, 178, 84)
GOLD_BRIGHT = (255, 214, 130)
BRONZE = (58, 44, 32)
BRONZE_LT = (96, 70, 46)
TEAL_DEEP = (16, 74, 88)
TEAL = (24, 106, 118)
INDIGO = (24, 30, 68)
PINK = (226, 122, 154)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def ribbon(dr, pts, width, fill):
    """Draw a thick curved band through pts as a filled polygon."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        x0, y0 = pts[max(0, i - 1)]
        x1, y1 = pts[min(n - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * width / 2, dx / L * width / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    dr.polygon(left + right[::-1], fill=fill)


def bezier(p0, p1, p2, steps=24):
    out = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        out.append((x, y))
    return out


def glow(dr, cx, cy, r, colour, steps=10):
    """Soft radial glow: concentric translucent circles on the overlay."""
    for i in range(steps, 0, -1):
        a = int(26 * (1 - i / steps) + 8)
        dr.ellipse([cx - r * i / steps, cy - r * i / steps,
                    cx + r * i / steps, cy + r * i / steps],
                   fill=colour + (a,))


def main(out_path):
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), CREAM)
    dr = ImageDraw.Draw(img)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)

    # --- sky gradient: indigo dusk -> teal horizon ---
    horizon = 660
    for y in range(FRAME, horizon):
        t = (y - FRAME) / (horizon - FRAME)
        c = lerp(INDIGO, (28, 96, 108), t)
        dr.line([(FRAME, y), (W - FRAME, y)], fill=c)
    # --- sea gradient ---
    for y in range(horizon, H - FRAME):
        t = (y - horizon) / (H - FRAME - horizon)
        c = lerp(TEAL, (10, 52, 66), t)
        dr.line([(FRAME, y), (W - FRAME, y)], fill=c)

    # --- stars ---
    for _ in range(70):
        x = rng.randint(FRAME + 8, W - FRAME - 8)
        y = rng.randint(FRAME + 8, 260)
        r = rng.choice([1, 1, 2])
        od.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 200, rng.randint(90, 200)))

    # --- distant headland + tiny town lights, left ---
    dr.polygon([(FRAME, 660), (FRAME, 600), (120, 585), (230, 620), (300, 660)],
               fill=(18, 42, 62))
    for i in range(9):
        x = 40 + i * 22 + rng.randint(-4, 4)
        y = 606 + rng.randint(-6, 10)
        od.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 200, 110, 220))

    # --- gold light path under the anchor ---
    for y in range(700, 985, 12):
        t = (y - 700) / 285
        half = 26 + t * 95
        a = int(110 * (1 - t) + 25)
        od.line([(512 - half, y), (512 + half, y)], fill=GOLD + (a,), width=5)

    # --- wave dashes ---
    for y in range(690, 990, 26):
        for _ in range(14):
            x = rng.randint(FRAME + 10, W - FRAME - 60)
            ln = rng.randint(18, 55)
            a = rng.randint(40, 110)
            od.line([(x, y), (x + ln, y)], fill=(140, 210, 210, a), width=3)

    cx = 512
    # --- chain from ring down-left to pier ---
    chain_pts = bezier((452, 330), (330, 520), (205, 845), steps=26)
    for i, (x, y) in enumerate(chain_pts):
        ang = math.degrees(math.atan2(8, -14)) + (i % 2) * 90
        r = 11
        od.ellipse([x - r, y - r * 0.62, x + r, y + r * 0.62],
                   outline=(210, 170, 100, 230), width=4)

    # --- ANCHOR ---
    # glow halo behind ring
    glow(od, cx, 300, 150, (255, 200, 100))
    # shaft
    dr.rectangle([cx - 20, 420, cx + 20, 700], fill=BRONZE)
    dr.line([(cx + 20, 420), (cx + 20, 700)], fill=GOLD, width=4)
    dr.line([(cx - 20, 420), (cx - 20, 700)], fill=(30, 22, 16), width=3)
    # ring (beacon): gold circle with bright core
    dr.ellipse([cx - 64, 236, cx + 64, 364], fill=GOLD)
    dr.ellipse([cx - 44, 256, cx + 44, 344], fill=(26, 34, 70))
    glow(od, cx, 300, 78, (255, 214, 130))
    dr.ellipse([cx - 30, 270, cx + 30, 330], fill=GOLD_BRIGHT)
    dr.ellipse([cx - 14, 286, cx + 14, 314], fill=(255, 240, 190))
    # crossbar: lantern gallery
    dr.rectangle([cx - 132, 392, cx + 132, 424], fill=BRONZE_LT)
    dr.rectangle([cx - 132, 392, cx + 132, 398], fill=GOLD)
    dr.rectangle([cx - 132, 418, cx + 132, 424], fill=GOLD)
    for wx in range(cx - 112, cx + 113, 28):
        dr.rectangle([wx, 402, wx + 14, 414], fill=GOLD_BRIGHT)
    # arms: curved ribbons from shaft base out and up, with flukes
    left_pts = bezier((cx - 14, 690), (cx - 120, 760), (cx - 205, 640), steps=20)
    right_pts = bezier((cx + 14, 690), (cx + 120, 760), (cx + 205, 640), steps=20)
    ribbon(dr, left_pts, 26, BRONZE)
    ribbon(dr, right_pts, 26, BRONZE)
    # gold rim-light on arm outer edges
    dr.line(left_pts, fill=GOLD, width=3)
    dr.line(right_pts, fill=GOLD, width=3)
    # fluke triangles (barbs) at arm tips, pointing out-up
    dr.polygon([(cx - 205, 640), (cx - 246, 596), (cx - 176, 606)], fill=BRONZE)
    dr.polygon([(cx - 205, 640), (cx - 246, 596), (cx - 176, 606)],
               outline=GOLD)
    dr.polygon([(cx + 205, 640), (cx + 246, 596), (cx + 176, 606)], fill=BRONZE)
    dr.polygon([(cx + 205, 640), (cx + 246, 596), (cx + 176, 606)],
               outline=GOLD)
    # anchor base knob
    dr.ellipse([cx - 26, 686, cx + 26, 724], fill=BRONZE_LT)
    dr.ellipse([cx - 26, 686, cx + 26, 724], outline=GOLD)

    # --- pier bottom-left with lanterns ---
    dr.rectangle([FRAME, 852, 330, 868], fill=(94, 64, 38))
    dr.rectangle([FRAME, 876, 300, 890], fill=(78, 52, 30))
    for px in (60, 140, 220, 290):
        dr.rectangle([px, 868, px + 10, 920], fill=(70, 46, 28))
    for lx in (52, 148, 232):
        dr.rectangle([lx, 824, lx + 6, 852], fill=(40, 28, 18))
        glow(od, lx + 3, 818, 22, (255, 190, 90))
        dr.ellipse([lx - 4, 810, lx + 10, 826], fill=GOLD_BRIGHT)

    # --- sailboats (right) ---
    def sailboat(bx, by, s, sail):
        dr.polygon([(bx - 34 * s, by), (bx + 34 * s, by),
                    (bx + 24 * s, by + 14 * s), (bx - 24 * s, by + 14 * s)],
                   fill=(52, 34, 22))
        dr.line([(bx, by), (bx, by - 52 * s)], fill=(40, 28, 18), width=3)
        dr.polygon([(bx + 3, by - 50 * s), (bx + 3, by - 6 * s),
                    (bx + 34 * s, by - 6 * s)], fill=sail)
        dr.polygon([(bx - 3, by - 44 * s), (bx - 3, by - 6 * s),
                    (bx - 26 * s, by - 6 * s)], fill=(240, 232, 210))

    sailboat(700, 800, 1.0, (244, 233, 205))
    sailboat(850, 850, 0.75, (232, 178, 84))
    sailboat(620, 880, 0.6, (240, 232, 210))

    # --- bougainvillea dot clusters: top-right + bottom-left edge ---
    for (bx, by) in [(930, 60), (950, 110), (905, 105), (60, 940), (95, 965)]:
        for _ in range(26):
            x = bx + rng.randint(-26, 26)
            y = by + rng.randint(-18, 18)
            r = rng.randint(2, 4)
            od.ellipse([x - r, y - r, x + r, y + r],
                       fill=(226, 122, 154, rng.randint(170, 235)))
        for _ in range(8):
            x = bx + rng.randint(-26, 26)
            y = by + rng.randint(-18, 18)
            od.ellipse([x - 3, y - 2, x + 3, y + 2], fill=(46, 110, 70, 200))

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    dr = ImageDraw.Draw(img)

    # --- title: huge cream serif, letterspaced ---
    title = "ANCHORA"
    tf = font(SERIF_B, 148)
    # measure with tracking
    tracking = 18
    widths = [dr.textlength(ch, font=tf) for ch in title]
    total = sum(widths) + tracking * (len(title) - 1)
    x = (W - total) / 2
    y_title = 30
    for ch, wch in zip(title, widths):
        dr.text((x, y_title), ch, font=tf, fill=CREAM)
        x += wch + tracking
    # subtitle with gold rules
    sf = font(SANS_B, 22)
    sub = "T H E   L I G H T H O U S E   A N C H O R"
    sw = dr.textlength(sub, font=sf)
    sx = (W - sw) / 2
    sy = 196
    dr.line([(sx - 150, sy + 16), (sx - 24, sy + 16)], fill=GOLD, width=3)
    dr.line([(sx + sw + 24, sy + 16), (sx + sw + 150, sy + 16)], fill=GOLD, width=3)
    dr.text((sx, sy), sub, font=sf, fill=GOLD_BRIGHT)

    # --- footer strip ---
    ff = font(SANS_B, 24)
    foot = "ANCHORA HARBOUR  •  LANTERNS LIT AT DUSK"
    fw = dr.textlength(foot, font=ff)
    dr.text(((W - fw) / 2, 968), foot, font=ff, fill=CREAM)

    # --- cream frame ---
    dr.rectangle([0, 0, W - 1, FRAME - 1], fill=CREAM)
    dr.rectangle([0, H - FRAME, W - 1, H - 1], fill=CREAM)
    dr.rectangle([0, 0, FRAME - 1, H - 1], fill=CREAM)
    dr.rectangle([W - FRAME, 0, W - 1, H - 1], fill=CREAM)
    dr.rectangle([FRAME - 1, FRAME - 1, W - FRAME, H - FRAME],
                 outline=(190, 160, 110), width=2)

    img.save(out_path, "PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png")
