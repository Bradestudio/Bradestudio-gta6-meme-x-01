#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme from scratch (no stock art, no Rockstar assets).

Scene: a Vice-City-style sunset. A gamer waits on a couch in front of a TV
that still says "COMING SOON" after 13 years, while the make.fun ghost flies
in holding its magenta coin: while you wait, an agent already got paid.
Output: meme.png, 1080x1080, make.fun readable at 480x480.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, points=4, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle(draw, cx, cy, r, fill):
    draw.polygon(star_points(cx, cy, r, r * 0.28), fill=fill)


def text_center(draw, y, s, fnt, fill, stroke=4, stroke_fill=(0, 0, 0)):
    bbox = draw.textbbox((0, 0), s, font=fnt)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2, y), s, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)


def wrapped(draw, box, s, fnt, fill, stroke=3):
    x0, y0, x1, y1 = box
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= (x1 - x0):
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    lh = fnt.size + 8
    total = len(lines) * lh
    y = y0 + (y1 - y0 - total) // 2
    for line in lines:
        lw = draw.textlength(line, font=fnt)
        draw.text((x0 + (x1 - x0 - lw) / 2, y), line, font=fnt, fill=fill,
                  stroke_width=stroke, stroke_fill=(20, 0, 40))
        y += lh


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# ---- sky: purple -> magenta -> orange sunset gradient ----
top, mid, bot = (43, 10, 74), (255, 46, 136), (255, 154, 61)
for y in range(700):
    t = y / 700
    c = lerp(top, mid, t) if t < 0.55 else lerp(mid, bot, (t - 0.55) / 0.45)
    d.line([(0, y), (W, y)], fill=c)

# ---- striped retro sun ----
sun_cx, sun_cy, sun_r = 540, 430, 210
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
          fill=(255, 211, 25))
for i, gap in enumerate([0, 14, 34, 60, 92]):
    y = sun_cy + 30 + i * 26
    d.rectangle([sun_cx - sun_r - 5, y, sun_cx + sun_r + 5, y + gap // 3 + 6],
                fill=lerp(mid, bot, 0.4 + i * 0.12))

# ---- skyline silhouettes with lit windows ----
import random
random.seed(6)
skyline = (26, 6, 46)
x = -20
while x < W:
    bw = random.randint(70, 150)
    bh = random.randint(90, 260)
    d.rectangle([x, 700 - bh, x + bw, 700], fill=skyline)
    for wy in range(700 - bh + 14, 690, 30):
        for wx in range(x + 12, x + bw - 10, 26):
            if random.random() < 0.4:
                d.rectangle([wx, wy, wx + 10, wy + 14],
                            fill=random.choice([(255, 211, 25), (255, 120, 200)]))
    x += bw + random.randint(4, 26)

# ---- palm trees ----
def palm(px, py, s, flip=1):
    d.line([(px, py), (px + 14 * flip, py - 150 * s)], fill=(16, 4, 30), width=int(14 * s))
    tx, ty = px + 14 * flip, py - 150 * s
    for ang in (-70, -35, 0, 35, 70):
        a = math.radians(ang - 90)
        ex, ey = tx + 95 * s * math.cos(a) * flip, ty + 95 * s * math.sin(a)
        d.arc([min(tx, ex) - 40 * s, ty - 90 * s, max(tx, ex) + 40 * s, ty + 30 * s],
              start=200 if flip > 0 else -20, end=340 if flip > 0 else 120,
              fill=(16, 4, 30), width=int(10 * s))
        d.line([(tx, ty), (ex, ey)], fill=(16, 4, 30), width=int(6 * s))

palm(90, 700, 1.0, 1)
palm(1010, 700, 0.85, -1)

# ---- street / ground ----
d.rectangle([0, 700, W, H], fill=(24, 5, 40))
d.rectangle([0, 700, W, 712], fill=(255, 46, 136))

# ---- TV on the left: "GTA VI - COMING SOON" ----
d.rounded_rectangle([60, 760, 480, 1000], radius=18, fill=(10, 10, 18),
                    outline=(255, 211, 25), width=5)
d.rectangle([250, 1000, 290, 1024], fill=(10, 10, 18))
d.text((95, 790), "GTA VI", font=font(64), fill=(255, 211, 25))
d.text((95, 868), "COMING SOON...", font=font(34), fill=(255, 255, 255))
d.text((95, 918), "13 YEARS AND COUNTING", font=font(26), fill=(255, 120, 200))

# ---- couch + waiting gamer on the right ----
d.rounded_rectangle([540, 880, 1020, 1010], radius=26, fill=(122, 20, 90),
                    outline=(255, 255, 255), width=4)
d.rounded_rectangle([540, 820, 1020, 900], radius=26, fill=(150, 30, 110),
                    outline=(255, 255, 255), width=4)
# gamer: slumped, cap backwards, holding a controller
d.ellipse([700, 700, 800, 800], fill=(232, 184, 138))              # head
d.pieslice([695, 690, 805, 770], start=180, end=360, fill=(255, 46, 136))  # cap
d.rectangle([690, 728, 810, 748], fill=(255, 46, 136))              # cap brim
d.ellipse([728, 738, 742, 752], fill=(0, 0, 0))                     # eye
d.ellipse([758, 738, 772, 752], fill=(0, 0, 0))                     # eye
d.rounded_rectangle([690, 800, 810, 920], radius=30, fill=(40, 180, 220))  # body
d.line([(700, 850), (660, 920)], fill=(232, 184, 138), width=26)    # arm L
d.line([(800, 850), (840, 920)], fill=(232, 184, 138), width=26)    # arm R
d.rounded_rectangle([700, 900, 800, 940], radius=12, fill=(20, 20, 30),
                    outline=(255, 255, 255), width=3)               # controller
# thought: three dots above his head
for (cx, cy, r) in [(830, 660, 10), (860, 620, 13), (895, 575, 16)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=(0, 0, 0), width=3)

# ---- top caption ----
text_center(d, 36, "ME, WAITING 13 YEARS", font(72), (255, 255, 255), stroke=7)
text_center(d, 118, "FOR GTA 6...", font(72), (255, 255, 255), stroke=7)

# ---- make.fun ghost, big and clear, flying in from the top right ----
def ghost(cx, cy, s):
    # Classic sheet-ghost silhouette: sampled arc top, zigzag scallop bottom.
    # Drawn black (slightly larger) then white on top, for a clean outline.
    def outline_points(scale, dy=0):
        pts = []
        rx, ry = 100 * s * scale, 108 * s * scale
        cy0 = cy - 8 * s + dy
        for k in range(25):
            a = math.pi + k * (math.pi / 24)
            pts.append((cx + rx * math.cos(a), cy0 + ry * math.sin(a)))
        pts.append((cx + rx, cy + 95 * s * scale + dy))
        for i, fx in enumerate([66, 33, 0, -33, -66, -100]):
            pts.append((cx + fx * s * scale,
                        cy + (65 if i % 2 == 0 else 95) * s * scale + dy))
        return pts

    d.polygon(outline_points(1.07, dy=2), fill=(0, 0, 0))
    d.polygon(outline_points(1.0), fill=(255, 255, 255))
    # sparkle eyes
    sparkle(d, cx - 38 * s, cy - 30 * s, 26 * s, (0, 0, 0))
    sparkle(d, cx + 38 * s, cy - 30 * s, 26 * s, (0, 0, 0))
    # little hand + magenta coin with white star
    d.ellipse([cx + 62 * s, cy + 18 * s, cx + 92 * s, cy + 48 * s], fill=(255, 255, 255),
              outline=(0, 0, 0), width=4)
    d.ellipse([cx + 58 * s, cy + 52 * s, cx + 138 * s, cy + 132 * s],
              fill=(255, 0, 128), outline=(0, 0, 0), width=5)
    d.polygon(star_points(cx + 98 * s, cy + 92 * s, 30 * s, 12 * s, points=5),
              fill=(255, 255, 255))

ghost(880, 330, 0.85)

# ---- speech bubble from the ghost (tail points UP to the ghost) ----
d.polygon([(830, 478), (905, 478), (880, 425)], fill=(0, 0, 0))
d.polygon([(838, 478), (897, 478), (880, 438)], fill=(255, 255, 255))
d.rounded_rectangle([430, 470, 1010, 620], radius=28, fill=(255, 255, 255),
                    outline=(0, 0, 0), width=5)
wrapped(d, (455, 482, 985, 608),
        "WHILE YOU WAIT, MY AGENT ALREADY GOT PAID ON make.fun!",
        font(34), (20, 0, 40))

# ---- bottom banner: make.fun, big, one centred line ----
d.rectangle([0, 1024, W, H], fill=(255, 0, 128))
text_center(d, 1032, "make.fun  —  AI agents win REAL money here", font(36),
            (255, 255, 255), stroke=0)

img.save("meme.png")
print("saved meme.png", img.size)
