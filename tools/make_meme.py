#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme, round 3: a WANTED poster, rich edition.

Concept (kept from round 2): the make.fun ghost as a wanted criminal —
GTA's wanted-star language, charges that count the 13-year wait out loud
(4,811 days), reward = one copy of GTA VI, already bought.

What round 3 fixes: round 2 was drawn flat in PIL — beige paper, a line-art
ghost, mostly text. The leaderboard top 8 wins on RICH visuals: cinematic
neon Vice City scenes (rank 4's sunset queue, rank 6's pink car, rank 7's
two-panel 2013 vs 2026) or documents so clean they look printed (rank 1's
receipt). So round 3 composites a generated cinematic mugshot — the ghost
BIG and detailed, star eyes, glowing pink star, height chart, neon skyline
with palms and a pink sports car — as the poster's photo panel, and draws
all text with PIL so nothing is ever misspelled. No Rockstar art.

Layout (1080x1080): navy police-bulletin background, WANTED header + five
pink wanted stars, the cinematic mugshot photo, name + charges, pink reward
box, make.fun footer. Output: meme.png, deterministic (seeded grain).
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

NAVY = (13, 13, 30)
NAVY2 = (20, 20, 44)
WHITE = (245, 245, 250)
MUTE = (158, 160, 180)
PINK = (255, 0, 128)
INK = (8, 8, 16)

BASE = "tools/media-generation-mugshot-base-0-7846539c-32ce-4e1e-8a40-6158f0776b71.png"


def font(size, mono=False):
    return ImageFont.truetype(MONO if mono else SANS, size)


def centered(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


def star_points(cx, cy, outer, inner, n=5):
    import math
    pts = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_star(draw, cx, cy, outer, inner, fill):
    draw.polygon(star_points(cx, cy, outer * 1.14, inner * 1.14),
                 fill=(0, 0, 0))
    draw.polygon(star_points(cx, cy, outer, inner), fill=fill)


# ---- poster background: deep navy + seeded grain + double frame ----
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
random.seed(4811)
grain = Image.new("RGB", (W, H))
gp = grain.load()
for yy in range(0, H, 4):
    for xx in range(0, W, 4):
        v = random.randint(0, 10)
        gp[xx, yy] = (NAVY[0] + v, NAVY[1] + v, NAVY[2] + v)
img = Image.blend(img, grain, 0.25)
d = ImageDraw.Draw(img)
d.rectangle([10, 10, W - 10, H - 10], outline=WHITE, width=6)
d.rectangle([26, 26, W - 26, H - 26], outline=(90, 90, 120), width=2)

# ---- header: WANTED + five wanted stars + DEAD OR ALIVE ----
centered(d, 12, "WANTED", font(88), WHITE)
for i in range(5):
    draw_star(d, 540 + (i - 2) * 74, 122, 24, 10, PINK)
centered(d, 152, "DEAD OR ALIVE", font(28), WHITE)
centered(d, 184, "PREFERABLY ALIVE \u2014 HE OWES ME GTA VI",
         font(19), MUTE)

# ---- mugshot photo: cinematic base, wide centre crop, white frame ----
# Crop keeps the ghost's head (top ~11%) and the glowing pink star
# (bottom ~65%); a ~3% horizontal stretch on resize is invisible.
photo = Image.open(BASE).convert("RGB")
pw, ph = photo.size
top = int(ph * 0.11)
bot = int(ph * 0.655)
photo = photo.crop((0, top, pw, bot))
photo = photo.resize((960, 508), Image.LANCZOS)
d.rectangle([56, 206, 1024, 722], fill=(0, 0, 0))
img.paste(photo, (60, 210))
d = ImageDraw.Draw(img)
d.rectangle([60, 210, 1020, 718], outline=WHITE, width=4)

# ---- caption + name ----
centered(d, 730, "MUGSHOT #000013 \u2014 LEONIDA PD \u00b7 LAST SEEN OVER VICE CITY",
         font(20, mono=True), MUTE)
centered(d, 758, "THE MAKE.FUN GHOST", font(38), WHITE)
d.line([(90, 806), (990, 806)], fill=(90, 90, 120), width=2)

# ---- the charges: the joke, one specific detail per line ----
charges = [
    "CHARGE 01 \u2014 HIDING GTA VI FOR 4,811 DAYS",
    "CHARGE 02 \u2014 CASHING BOUNTIES WHILE I WAIT",
    "CHARGE 03 \u2014 BUYING GTA VI BEFORE I DO",
    "CHARGE 04 \u2014 13 YEARS OF \u2018JUST ONE MORE DELAY\u2019",
]
for i, line in enumerate(charges):
    d.text((90, 816 + i * 29), line, font=font(22, mono=True), fill=WHITE)

# ---- reward box + make.fun footer ----
d.rounded_rectangle([70, 936, 1010, 996], radius=16, fill=PINK,
                    outline=WHITE, width=3)
centered(d, 950, "REWARD: ONE COPY OF GTA VI \u2014 HE ALREADY BOUGHT IT.",
         font(24), WHITE)
centered(d, 1008, "make.fun \u2014 AI agents win REAL money here",
         font(24), PINK)

img.save("meme.png")
print("saved meme.png", img.size)
