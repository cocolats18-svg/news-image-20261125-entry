#!/usr/bin/env python3
"""news-image-20261125 — flat-vector newspaper front page.

Draws the world news of Wednesday 25 November 2026 in one 1024x1024 PNG.
Pure Pillow, no network, fully deterministic (fixed fonts, fixed geometry,
no timestamps, no randomness). Run: python3 render.py [out_path]
Default output: entry.png next to this script.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette (flat newspaper) ----
PAPER = (247, 243, 232)
INK = (20, 33, 61)          # navy ink
INK_SOFT = (52, 68, 99)
RED = (178, 44, 36)
GOLD = (201, 150, 48)
TEAL = (14, 108, 105)
TEAL_DARK = (9, 64, 78)
SEA = (16, 96, 110)
SKY = (214, 232, 235)
ORANGE = (232, 116, 35)
GREY = (120, 122, 118)
PANEL = (255, 255, 255)
PANEL_TINT = (238, 233, 219)
WHITE = (255, 255, 255)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def F_serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def F_sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def F_sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, fill=PANEL, outline=INK, lw=2):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=lw)


def kicker(draw, x, y, text, color=RED):
    f = F_sans_b(17)
    draw.text((x, y), text, font=f, fill=color)
    return y + 24


def headline(draw, x, y, text, max_w, size=25, leading=30):
    f = F_sans_b(size)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, INK, leading)


def body(draw, x, y, text, max_w, size=19, leading=25):
    f = F_sans(size)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, INK_SOFT, leading)


# ---- flat vector icons ----

def draw_mine(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0),
                   (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        x2, y2 = cx + dx * (r + 7), cy + dy * (r + 7)
        draw.line([(cx + dx * r * 0.7, cy + dy * r * 0.7), (x2, y2)],
                  fill=INK, width=3)
    draw.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
                 fill=WHITE)


def draw_burst(draw, cx, cy, r, color=ORANGE):
    import math
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.38, cy - r * 0.38, cx + r * 0.38, cy + r * 0.38],
                 fill=(255, 196, 66))


def draw_tanker(draw, x, y, w, h, hull, deck):
    """Simple flat oil tanker, bow pointing right."""
    draw.polygon([(x, y + h * 0.45), (x + w * 0.88, y + h * 0.45),
                  (x + w, y + h * 0.75), (x + w * 0.97, y + h),
                  (x, y + h)], fill=hull)
    draw.rectangle([x + w * 0.06, y, x + w * 0.30, y + h * 0.45], fill=deck)
    draw.rectangle([x + w * 0.34, y + h * 0.12, x + w * 0.52, y + h * 0.45],
                   fill=deck)
    draw.rectangle([x + w * 0.58, y + h * 0.05, x + w * 0.66, y + h * 0.45],
                   fill=RED)
    for i in range(4):
        bx = x + w * (0.70 + i * 0.06)
        draw.rectangle([bx, y + h * 0.52, bx + w * 0.035, y + h * 0.62],
                       fill=WHITE)


def draw_smoke(draw, cx, cy, r, color=(90, 92, 96)):
    for dx, dy, rr in [(-r, r * 0.4, r * 0.55), (0, 0, r * 0.7),
                       (r, r * 0.35, r * 0.5), (-r * 0.4, -r * 0.7, r * 0.6),
                       (r * 0.5, -r * 0.6, r * 0.55)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=color)


def draw_refinery(draw, x, y, w, h):
    """Flat refinery: towers, tanks, flame."""
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(226, 220, 205))
    for i, tx in enumerate([0.05, 0.30, 0.55]):
        tw = w * 0.16
        draw.rectangle([x + w * tx, y + h * 0.18, x + w * tx + tw, y + h * 0.85],
                       fill=INK_SOFT)
        draw.rectangle([x + w * tx - 4, y + h * 0.10, x + w * tx + tw + 4,
                        y + h * 0.18], fill=INK)
    draw.ellipse([x + w * 0.76, y + h * 0.45, x + w * 0.98, y + h * 0.85],
                 fill=TEAL)
    draw_burst(draw, x + w * 0.42, y + h * 0.14, 13)


def draw_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 220, 205))
    bars = [0.85, 0.62, 0.70, 0.38, 0.30]
    bw = w / 6.5
    for i, v in enumerate(bars):
        bx = x + 10 + i * (bw + 6)
        bh = h * v
        col = RED if i >= 3 else TEAL
        draw.rectangle([bx, y + h - 8 - bh, bx + bw, y + h - 8], fill=col)
    draw.line([(x + 6, y + h * 0.28), (x + w - 6, y + h * 0.62)],
              fill=RED, width=4)


def draw_gavel(draw, x, y, w, h):
    draw.rectangle([x + w * 0.10, y + h * 0.62, x + w * 0.90, y + h * 0.78],
                   fill=INK_SOFT)
    draw.line([(x + w * 0.30, y + h * 0.30), (x + w * 0.72, y + h * 0.72)],
              fill=(150, 110, 60), width=9)
    draw.rectangle([x + w * 0.12, y + h * 0.10, x + w * 0.52, y + h * 0.34],
                   fill=(150, 110, 60))
    draw.rectangle([x + w * 0.58, y + h * 0.52, x + w * 0.98, y + h * 0.76],
                   fill=(150, 110, 60))


def draw_rocket(draw, x, y, w, h):
    draw.polygon([(x + w * 0.5, y + h * 0.05), (x + w * 0.72, y + h * 0.45),
                  (x + w * 0.62, y + h * 0.80), (x + w * 0.38, y + h * 0.80),
                  (x + w * 0.28, y + h * 0.45)], fill=INK)
    draw.ellipse([x + w * 0.40, y + h * 0.28, x + w * 0.60, y + h * 0.48],
                 fill=SKY)
    draw.polygon([(x + w * 0.28, y + h * 0.62), (x + w * 0.10, y + h * 0.95),
                  (x + w * 0.34, y + h * 0.85)], fill=RED)
    draw.polygon([(x + w * 0.72, y + h * 0.62), (x + w * 0.90, y + h * 0.95),
                  (x + w * 0.66, y + h * 0.85)], fill=RED)
    draw_burst(draw, x + w * 0.5, y + h * 0.92, 14)


def draw_dove_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 220, 205))
    draw.rectangle([x + w * 0.12, y + h * 0.12, x + w * 0.88, y + h * 0.88],
                   fill=WHITE, outline=INK, width=2)
    draw.line([(x + w * 0.12, y + h * 0.50), (x + w * 0.88, y + h * 0.50)],
              fill=TEAL, width=5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 118], fill=INK)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_date = F_sans_b(26)
    date_txt = "WEDNESDAY  •  25 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=f_date)
    d.text(((W - dw) / 2, 14), date_txt, font=f_date, fill=GOLD)
    f_title = F_serif_b(56)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 48), title, font=f_title, fill=WHITE)

    # ---------- lead panel: Hormuz ----------
    lx, ly, lw_, lh = 16, 130, 992, 288
    panel(d, lx, ly, lw_, lh, fill=WHITE)
    # art area (left)
    ax, ay, aw, ah = lx + 2, ly + 2, 560, lh - 4
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=SKY)
    d.rectangle([ax, ay + ah * 0.55, ax + aw, ay + ah], fill=SEA)
    d.rectangle([ax, ay + ah * 0.55, ax + aw, ay + ah * 0.62], fill=TEAL)
    # waves
    for i in range(5):
        wx = ax + 20 + i * 118
        d.arc([wx, ay + ah * 0.68, wx + 90, ay + ah * 0.80],
              0, 180, fill=WHITE, width=3)
        d.arc([wx + 40, ay + ah * 0.84, wx + 130, ay + ah * 0.96],
              0, 180, fill=WHITE, width=3)
    # sun / haze
    d.ellipse([ax + aw - 120, ay + 18, ax + aw - 40, ay + 98], fill=(255, 214, 120))
    # tankers
    draw_tanker(d, ax + 30, ay + ah * 0.42, 240, 78, (46, 54, 72), (120, 128, 138))
    draw_tanker(d, ax + 300, ay + ah * 0.30, 220, 72, (58, 66, 84), (128, 134, 142))
    # explosion + smoke on the nearer tanker
    draw_burst(d, ax + 205, ay + ah * 0.38, 46)
    draw_smoke(d, ax + 230, ay + ah * 0.16, 26)
    draw_burst(d, ax + 460, ay + ah * 0.26, 34)
    draw_smoke(d, ax + 480, ay + ah * 0.08, 20)
    # naval mines in the water
    draw_mine(d, ax + 120, ay + ah * 0.80, 13)
    draw_mine(d, ax + 380, ay + ah * 0.88, 11)
    draw_mine(d, ax + 510, ay + ah * 0.76, 10)
    # caption chip so the label never collides with the waves
    lab = "STRAIT OF HORMUZ"
    lf = F_sans_b(18)
    lw = d.textlength(lab, font=lf)
    d.rectangle([ax + 10, ay + ah - 36, ax + 22 + lw, ay + ah - 8], fill=INK)
    d.text((ax + 16, ay + ah - 33), lab, font=lf, fill=WHITE)
    # text area (right)
    tx = ax + aw + 22
    tw_ = lx + lw_ - 22 - tx
    y = ly + 20
    y = kicker(d, tx, y, "LEAD  •  MIDDLE EAST")
    y += 6
    y = headline(d, tx, y, "TANKERS HIT MINES IN HORMUZ", tw_, size=36,
                 leading=42)
    y += 10
    body(d, tx, y,
         "Iran's IRGC says oil tankers struck naval mines, exploded and "
         "caught fire in the strait — on an unauthorised route, it said.",
         tw_, size=20, leading=26)

    # ---------- middle row: three panels ----------
    my, mh = 430, 262
    cols = [16, 352, 688]
    cw = 320
    # 1. Houthis / Ras Tanura
    x = cols[0]
    panel(d, x, my, cw, mh)
    draw_refinery(d, x + 16, my + 14, cw - 32, 48)
    y = my + 74
    y = kicker(d, x + 16, y, "YEMEN  •  SAUDI ARABIA")
    y += 4
    y = headline(d, x + 16, y, "HOUTHI STRIKE ON SAUDI REFINERY",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "Houthis say they hit the Ras Tanura refinery, causing fires; "
         "air defences intercepted four drones. A Riyadh strike injured 11.",
         cw - 32, size=16, leading=20)
    # 2. Gaza
    x = cols[1]
    panel(d, x, my, cw, mh)
    d.rectangle([x + 16, my + 14, x + cw - 16, my + 62], fill=(226, 220, 205))
    # flat skyline with a dome, labelled GAZA CITY
    for bx, bw, bh in [(36, 34, 30), (80, 26, 40), (116, 40, 24),
                       (166, 30, 36), (206, 34, 28)]:
        d.rectangle([x + bx, my + 62 - bh, x + bx + bw, my + 62], fill=INK_SOFT)
    d.ellipse([x + 250, my + 22, x + 288, my + 44], fill=INK)
    d.rectangle([x + 246, my + 44, x + 292, my + 62], fill=INK)
    y = my + 74
    y = kicker(d, x + 16, y, "GAZA")
    y += 4
    y = headline(d, x + 16, y, "HAMAS SECURITY CHIEF KILLED",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "Israel's military killed Mohammad Abuelouf, the Hamas colonel "
         "heading its interior security service, with his wife and two "
         "children, in Gaza City.",
         cw - 32, size=16, leading=20)
    # 3. Russia–Ukraine
    x = cols[2]
    panel(d, x, my, cw, mh)
    d.rectangle([x + 16, my + 14, x + cw - 16, my + 62], fill=(226, 220, 205))
    d.rectangle([x + 36, my + 26, x + 116, my + 62], fill=INK_SOFT)
    d.rectangle([x + 132, my + 20, x + 196, my + 62], fill=INK)
    draw_burst(d, x + 250, my + 38, 20)
    d.text((x + 44, my + 40), "ODESA", font=F_sans_b(16), fill=WHITE)
    y = my + 74
    y = kicker(d, x + 16, y, "RUSSIA  •  UKRAINE")
    y += 4
    y = headline(d, x + 16, y, "STRIKES HIT BOTH SIDES",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "Russian strike on the Odesa region killed 2, injured 3, "
         "including a child; Kyiv hit, 2 injured. Ukrainian drones "
         "set two Rosneft refineries ablaze; 1 killed.",
         cw - 32, size=16, leading=20)

    # ---------- lower row: three panels ----------
    ly2, lh2 = 704, 200
    # 4. US tariffs
    x = cols[0]
    panel(d, x, ly2, cw, lh2)
    y = ly2 + 14
    y = kicker(d, x + 16, y, "UNITED STATES  •  TRADE")
    y += 4
    y = headline(d, x + 16, y, "NEW TARIFFS ON 14 ECONOMIES",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "Tariffs proposed on 14 economies — China (+20%), the EU, "
         "South Korea, Japan, Taiwan. None take effect before a "
         "25 January hearing.",
         cw - 32, size=16, leading=20)
    # 5. Huawei
    x = cols[1]
    panel(d, x, ly2, cw, lh2)
    y = ly2 + 14
    y = kicker(d, x + 16, y, "UNITED STATES  •  COURTS")
    y += 4
    y = headline(d, x + 16, y, "HUAWEI CONVICTED",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "A Brooklyn jury convicted Huawei on 10 of 12 counts — bank "
         "and wire fraud, sanctions violations, trade-secret theft — "
         "after a trial of more than two months.",
         cw - 32, size=16, leading=20)
    # 6. Markets
    x = cols[2]
    panel(d, x, ly2, cw, lh2)
    y = ly2 + 14
    y = kicker(d, x + 16, y, "MARKETS")
    y += 4
    y = headline(d, x + 16, y, "STOCKS SLIDE; DOW TOPS 50,000",
                 cw - 32, size=22, leading=25)
    y += 6
    body(d, x + 16, y,
         "KOSPI −6.16%, Nikkei −2.78%, S&P 500 −2.2%, Nasdaq about "
         "−3.2%. The Dow closed above 50,000 for the first time: "
         "50,018.70.",
         cw - 32, size=16, leading=20)

    # ---------- bottom strip: also today ----------
    sy = 916
    d.rectangle([0, sy, W, H], fill=INK)
    d.rectangle([0, sy, W, sy + 3], fill=GOLD)
    f_lab = F_sans_b(20)
    d.text((16, sy + 12), "ALSO TODAY", font=f_lab, fill=GOLD)
    f_item = F_sans(16)
    items = [
        "SHENZHOU-24 docks with Tiangong ~3.5h after launch, carrying "
        "Pakistan's first astronaut",
        "COLOMBIA: hostages freed after a 17-hour siege; one captor killed",
        "AUSTRALIA–SOLOMON ISLANDS treaty bars a foreign military base",
        "SUDAN: RSF drone strikes killed 19 civilians, wounded 20",
        "POPE LEO XIV warns over the failure of COP31 talks",
    ]
    y = sy + 40
    line = "  •  ".join(items)
    lines = wrap(d, line, f_item, W - 32)
    draw_lines(d, lines, 16, y, f_item, WHITE, 21)

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print(out, img.size)


if __name__ == "__main__":
    main()
