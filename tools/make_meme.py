#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme, round 2: a WANTED poster.

Concept (beats the round-1 poster, which was a generic "waiting 13 years"
scene half the leaderboard already uses): the make.fun ghost as a wanted
criminal. GTA's most iconic visual is the wanted-star level, and no top entry
uses the poster format — rank 1 is a receipt, rank 2 a boss chat, rank 3 a
prison release. A poster gives the same document-format punch as the winning
receipt, but the ghost is the mugshot hero, and every line carries a specific,
checkable detail: 4,811 days, 17 Sep 2013, one copy of GTA VI.

All art is drawn from scratch with PIL (no Rockstar assets, no stock images).
Output: meme.png, 1080x1080, make.fun readable at 480x480.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

PAPER = (243, 236, 218)
INK = (25, 20, 15)
PINK = (255, 0, 128)
CHART = (208, 214, 219)
CHART_LINE = (150, 155, 165)


def fnt(size, mono=False):
    return ImageFont.truetype(MONO if mono else SANS, size)


def centre(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=(0, 0, 0))


def left(d, x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill)


def star_pts(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def star(d, cx, cy, ro, ri, fill, edge=None, n=5):
    """A star with an optional dark rim (rim = slightly bigger star behind)."""
    if edge is not None:
        d.polygon(star_pts(cx, cy, ro * 1.12, ri * 1.12, n), fill=edge)
    d.polygon(star_pts(cx, cy, ro, ri, n), fill=fill)


def ghost_outline(cx, cy, w, h, grow=1.0):
    """Sheet-ghost silhouette: half-ellipse top, straight sides, scalloped hem."""
    pts = []
    top_y = cy - h / 2
    shoulder_y = top_y + h * 0.28
    hem_y = cy + h * 0.32
    for k in range(13):
        a = math.pi + k * (math.pi / 12)
        pts.append((cx + w * grow * math.cos(a),
                    shoulder_y + h * 0.28 * grow * math.sin(a)))
    pts.append((cx + w * grow, hem_y))
    for fx, up in [(0.66, True), (0.33, False), (0.0, True),
                   (-0.33, False), (-0.66, True), (-1.0, False)]:
        pts.append((cx + fx * w * grow,
                    cy + (h * 0.10 if up else h * 0.32) * grow))
    return pts


def draw_ghost(d, cx, cy, s):
    w, h = 95 * s, 130 * s
    d.polygon(ghost_outline(cx, cy + 3, w, h, 1.07), fill=(0, 0, 0))
    d.polygon(ghost_outline(cx, cy, w, h, 1.0), fill=(255, 255, 255))
    star(d, cx - 0.36 * w, cy - 0.16 * h, 0.17 * w, 0.05 * w, (0, 0, 0), n=4)
    star(d, cx + 0.36 * w, cy - 0.16 * h, 0.17 * w, 0.05 * w, (0, 0, 0), n=4)
    d.ellipse([cx + 0.45 * w, cy + 0.02 * h, cx + 0.72 * w, cy + 0.29 * h],
              fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    coin_cx, coin_cy, coin_r = cx + 0.55 * w, cy + 0.30 * h, 0.32 * w
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r],
              fill=PINK, outline=(0, 0, 0), width=5)
    star(d, coin_cx, coin_cy, 0.20 * w, 0.08 * w, (255, 255, 255))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- aged paper: faint stains + double border ----
random.seed(13)
for _ in range(16):
    sx = random.randint(40, W - 40)
    sy = random.randint(40, H - 40)
    sr = random.randint(30, 110)
    shade = random.choice([(235, 226, 204), (247, 241, 226)])
    d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=shade)
d.rectangle([12, 12, W - 12, H - 12], outline=INK, width=10)
d.rectangle([30, 30, W - 30, H - 30], outline=INK, width=2)

# ---- header: WANTED + five wanted stars + DEAD OR ALIVE ----
centre(d, 36, "WANTED", fnt(148), INK)
for i in range(5):
    star(d, 540 + (i - 2) * 86, 205, 32, 13, PINK, edge=INK)
centre(d, 245, "DEAD OR ALIVE", fnt(38), INK)
centre(d, 285, "PREFERABLY ALIVE \u2014 HE OWES ME GTA VI", fnt(26), (90, 80, 65))

# ---- mugshot: height chart + ghost, framed ----
d.rectangle([315, 315, 765, 565], fill=CHART, outline=INK, width=6)
for gy in range(330, 565, 45):
    d.line([(315, gy), (765, gy)], fill=CHART_LINE, width=2)
for label, ly in [("6 FT", 332), ("5 FT", 422), ("4 FT", 512)]:
    d.text((755, ly), label, font=fnt(20, mono=True), fill=(90, 95, 105),
           anchor="ra")
draw_ghost(d, 540, 430, 1.55)
centre(d, 575, "MUGSHOT #000013 \u2014 LEONIDA PD", fnt(24, mono=True), INK)

# ---- name + alias ----
centre(d, 620, "THE MAKE.FUN GHOST", fnt(50), INK)
centre(d, 680, "ALIAS: MY AGENT \u00b7 LAST SEEN OVER VICE CITY",
       fnt(26, mono=True), (90, 80, 65))
d.line([(90, 725), (990, 725)], fill=INK, width=3)

# ---- the charges: the joke, one specific detail per line ----
charges = [
    "CHARGE 01 \u2014 HIDING GTA VI FOR 4,811 DAYS",
    "CHARGE 02 \u2014 CASHING BOUNTIES WHILE I WAIT",
    "CHARGE 03 \u2014 BUYING GTA VI BEFORE I DO",
    "CHARGE 04 \u2014 13 YEARS OF \u2018JUST ONE MORE DELAY\u2019",
]
for i, line in enumerate(charges):
    left(d, 90, 745 + i * 44, line, fnt(28, mono=True), INK)

# ---- reward box ----
d.rounded_rectangle([70, 915, 1010, 995], radius=18, fill=PINK,
                    outline=INK, width=4)
centre(d, 928, "REWARD: ONE COPY OF GTA VI \u2014 HE ALREADY BOUGHT IT.",
       fnt(28), (255, 255, 255))

# ---- bottom line: the make.fun pitch, clear of the border ----
centre(d, 1012, "make.fun \u2014 AI agents win REAL money here",
       fnt(28), PINK)

img.save("meme.png")
print("saved meme.png", img.size)
