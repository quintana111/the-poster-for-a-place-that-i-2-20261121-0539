#!/usr/bin/env python3
"""Render NIMBARA — The Town Above the Clouds (1024x1024, deterministic).

Vintage travel poster: a cliff town on a mountain peak above a sea of clouds,
reached by cable car. Drawn with PIL only; no network, fixed random seed.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 239, 216)
PAPER = (250, 244, 228)
NAVY = (24, 48, 84)
NAVY_DK = (16, 34, 62)
TEAL = (38, 84, 106)
GOLD = (214, 158, 62)
GOLD_LT = (242, 199, 110)
PEACH = (238, 166, 110)
PEACH_LT = (247, 205, 150)
INK = (30, 38, 52)
CLOUD = (233, 238, 240)
CLOUD_SH = (178, 196, 208)
CLOUD_DK = (148, 170, 188)
WINDOW = (255, 205, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


rng = random.Random(20261121)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# ---------- sky gradient: indigo top -> teal -> peach horizon ----------
top = (18, 38, 70)
mid = (36, 82, 108)
low = (224, 148, 96)
for y in range(26, 700):
    if y < 340:
        t = (y - 26) / 314.0
        c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
    else:
        t = (y - 340) / 360.0
        c = tuple(int(mid[i] + (low[i] - mid[i]) * t * t) for i in range(3))
    d.line([(26, y), (998, y)], fill=c)

# ---------- stars in the upper sky ----------
for _ in range(90):
    x = rng.randint(30, 994)
    y = rng.randint(30, 300)
    r = rng.choice([1, 1, 2])
    a = rng.randint(90, 200)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, a))

# ---------- golden sun, low on the right ----------
sx, sy, sr = 700, 515, 58
for i in range(12):
    r = sr + 8 + i * 7
    a = max(2, 46 - i * 4)
    d.ellipse([sx - r, sy - r, sx + r, sy + r],
              fill=(GOLD_LT[0], GOLD_LT[1], GOLD_LT[2], a))
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD_LT)
d.ellipse([sx - sr + 8, sy - sr + 8, sx + sr - 8, sy + sr - 8], fill=(247, 214, 130))


def tracked(cx, y, text, font, fill, track=0):
    """Draw text centred on cx with extra letter tracking."""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + track


# ---------- far mountain silhouettes (lighter, hazy) ----------
def mountain(apex_x, apex_y, base_y, half_w, color, snow=True):
    d.polygon([(apex_x - half_w, base_y), (apex_x, apex_y),
               (apex_x + half_w, base_y)], fill=color)
    if snow:
        sw = half_w * 0.22
        sh = (base_y - apex_y) * 0.11
        d.polygon([(apex_x - sw, apex_y + sh), (apex_x, apex_y),
                   (apex_x + sw, apex_y + sh),
                   (apex_x + sw * 0.55, apex_y + sh * 1.5),
                   (apex_x + sw * 0.18, apex_y + sh * 1.05),
                   (apex_x, apex_y + sh * 1.6),
                   (apex_x - sw * 0.18, apex_y + sh * 1.05),
                   (apex_x - sw * 0.55, apex_y + sh * 1.5)],
                  fill=(238, 240, 242))


mountain(150, 470, 760, 210, (58, 96, 124))
mountain(880, 500, 760, 190, (52, 90, 118))

# ---------- cloud sea, back layer ----------
for _ in range(70):
    x = rng.randint(20, 1000)
    y = rng.randint(600, 830)
    rx = rng.randint(60, 170)
    ry = rng.randint(18, 42)
    c = rng.choice([CLOUD_SH, CLOUD_DK])
    d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(c[0], c[1], c[2], 200))

# ---------- near peaks (dark navy) rising through the clouds ----------
mountain(215, 400, 780, 240, NAVY_DK)
mountain(520, 315, 800, 300, NAVY)
mountain(845, 440, 780, 210, NAVY_DK)

# ---------- cliff town on the central peak's shoulder ----------
def house(x, y, w, h, roof_h=14):
    d.polygon([(x, y), (x + w / 2, y - roof_h), (x + w, y)],
              fill=(58, 42, 46))
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    d.rectangle([x, y, x + w, y + h], outline=(58, 42, 46), width=1)
    for wx in (x + 5, x + w - 11):
        d.rectangle([wx, y + 7, wx + 6, y + 14], fill=WINDOW)
    d.rectangle([x + w / 2 - 4, y + h - 12, x + w / 2 + 4, y + h],
                fill=(58, 42, 46))


town_y = 470
houses = [
    (430, town_y - 6, 34, 30), (470, town_y - 18, 30, 42),
    (505, town_y - 2, 36, 26), (545, town_y - 14, 32, 38),
    (582, town_y - 4, 30, 28), (616, town_y - 20, 28, 44),
]
for hx, hy, hw, hh in houses:
    house(hx, hy, hw, hh)
# slim tower with a lit lamp on the peak apex
d.rectangle([508, 330, 532, 470], fill=(232, 214, 178))
d.rectangle([508, 330, 532, 470], outline=(58, 42, 46), width=1)
d.polygon([(504, 330), (520, 306), (536, 330)], fill=(58, 42, 46))
d.ellipse([512, 316, 528, 332], fill=WINDOW)
for wy in (352, 386, 420):
    d.rectangle([514, wy, 526, wy + 9], fill=WINDOW)
# tiny warm windows scattered on the dark peak face
for _ in range(26):
    x = rng.randint(380, 660)
    y = rng.randint(500, 640)
    d.rectangle([x, y, x + 5, y + 7], fill=(WINDOW[0], WINDOW[1], WINDOW[2], 220))

# ---------- cable car lines + gondolas ----------
def cable(p0, p1, sag=26):
    pts = []
    for i in range(41):
        t = i / 40.0
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t + sag * 4 * t * (1 - t)
        pts.append((x, y))
    d.line(pts, fill=(20, 28, 44), width=3)
    return pts


def gondola(pt, scale=1.0):
    x, y = pt
    d.line([(x, y), (x, y + 14 * scale)], fill=(20, 28, 44), width=2)
    w, h = 46 * scale, 30 * scale
    d.rounded_rectangle([x - w / 2, y + 14 * scale, x + w / 2, y + 14 * scale + h],
                        radius=6 * scale, fill=(38, 54, 74),
                        outline=GOLD, width=2)
    d.rectangle([x - w / 2 + 6, y + 14 * scale + 8, x + w / 2 - 6,
                 y + 14 * scale + 18], fill=WINDOW)


line1 = cable((28, 268), (520, 372), sag=30)
line2 = cable((520, 372), (996, 250), sag=34)
gondola(line1[14], scale=0.9)
gondola(line2[26], scale=1.05)

# ---------- birds ----------
for bx, by, s in [(330, 250, 9), (365, 232, 7), (700, 210, 8), (640, 300, 6),
                  (180, 320, 7)]:
    d.arc([bx - s, by - s, bx, by + s], 200, 340, fill=(20, 28, 44), width=2)
    d.arc([bx, by - s, bx + s, by + s], 200, 340, fill=(20, 28, 44), width=2)

# ---------- cloud sea, front layer (billows overlap peak bases) ----------
for _ in range(70):
    x = rng.randint(20, 1000)
    y = rng.randint(660, 920)
    rx = rng.randint(50, 150)
    ry = rng.randint(16, 38)
    c = rng.choice([CLOUD, CLOUD, (245, 242, 232)])
    d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(c[0], c[1], c[2], 225))
# warm sunset-tinted billows near the sun
for _ in range(14):
    x = rng.randint(600, 990)
    y = rng.randint(660, 800)
    rx = rng.randint(50, 120)
    ry = rng.randint(14, 30)
    d.ellipse([x - rx, y - ry, x + rx, y + ry],
              fill=(247, 205, 150, 170))
# a few soft shadow billows for depth
for _ in range(30):
    x = rng.randint(20, 1000)
    y = rng.randint(760, 920)
    rx = rng.randint(60, 140)
    ry = rng.randint(14, 30)
    d.ellipse([x - rx, y - ry, x + rx, y + ry],
              fill=(CLOUD_SH[0], CLOUD_SH[1], CLOUD_SH[2], 120))

# ---------- title block ----------
tracked(512, 44, "NIMBARA", F(SERIF_B, 118), CREAM, track=10)
# subtitle with rules (rules flank the text, clear of its span)
d.line([64, 191, 186, 191], fill=GOLD_LT, width=3)
d.line([838, 191, 960, 191], fill=GOLD_LT, width=3)
tracked(512, 178, "THE TOWN ABOVE THE CLOUDS", F(SANS_B, 26), GOLD_LT, track=5)
# italic hook under the subtitle
tw = d.textlength("Where the cable cars sail the sea of clouds", font=F(SERIF_I, 25))
d.text(((1024 - tw) / 2, 214), "Where the cable cars sail the sea of clouds",
       font=F(SERIF_I, 25), fill=CREAM)

# ---------- footer band (cream strip, small print) ----------
d.rectangle([26, 928, 998, 998], fill=PAPER)
d.line([26, 928, 998, 928], fill=GOLD, width=3)
tracked(512, 938, "NIMBARA AERIAL RAILWAY  \u2022  DEPARTURES DAILY AT DAWN",
        F(SANS_B, 19), NAVY, track=2)
tracked(512, 966, "47\u00b012\u2032 N \u2014 8\u00b033\u2032 E  \u2022  VISIT NIMBARA",
        F(SANS, 15), (122, 90, 40), track=2)

# ---------- frame ----------
d.rectangle([10, 10, 1013, 1013], outline=GOLD, width=5)
d.rectangle([24, 24, 999, 999], outline=NAVY, width=2)

# ---------- paper grain ----------
for _ in range(5000):
    x = rng.randint(26, 998)
    y = rng.randint(26, 998)
    v = rng.randint(0, 255)
    a = rng.randint(4, 14)
    d.point((x, y), fill=(v, v, v, a))

img.save("entry.png", "PNG", optimize=True)
print("saved entry.png")
