#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (build-time only)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG, PANEL = "#0B1020", "#151C31"
INK, MUTED = "#F4F6FB", "#A7B7CF"
GOLD, RED, BLUE = "#F5B13B", "#EF5B4C", "#4FA9E8"
GREEN, PURPLE = "#4FC38D", "#B58AF0"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)


def center(d, box, text, f, fill):
    x0, y0, x1, y1 = box
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((x0 + x1 - (bb[2] - bb[0])) / 2,
            (y0 + y1 - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=fill)


def fit(text, box_w, sz):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    f = font(sz)
    while sz > 24 and probe.textbbox((0, 0), text, font=f)[2] > box_w:
        sz -= 2
        f = font(sz)
    return f


def card(d, x, y, w, h, accent, label, sub, icon):
    d.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=PANEL,
                        outline=accent, width=3)
    d.rounded_rectangle((x, y, x + 10, y + h), radius=5, fill=accent)
    center(d, (x + 10, y + 14, x + w, y + 92), label, font(42), INK)
    center(d, (x + 14, y + h - 76, x + w - 12, y + h - 22), sub, font(22), MUTED)
    icon(d, x + w / 2, y + h / 2 + 6, accent)


def leaders(d, cx, cy, c):
    d.rectangle((cx - 100, cy - 78, cx + 100, cy + 40), fill="#7E1B2B")
    for dx in (-44, 44):
        d.ellipse((cx + dx - 19, cy - 52, cx + dx + 19, cy - 14), fill=INK)
        d.rectangle((cx + dx - 22, cy + 4, cx + dx + 22, cy + 38), fill=c)
    d.line((cx - 24, cy + 14, cx + 24, cy + 14), fill=INK, width=10)
    d.line((cx - 100, cy + 50, cx + 100, cy + 50), fill=RED, width=9)


def missile(d, cx, cy, c):
    d.polygon([(cx - 30, cy - 78), (cx + 30, cy - 78),
               (cx + 18, cy + 20), (cx - 18, cy + 20)], fill=INK)
    d.polygon([(cx - 30, cy - 78), (cx, cy - 108),
               (cx + 30, cy - 78)], fill=c)
    d.rectangle((cx - 20, cy + 16, cx + 20, cy + 34), fill=RED)
    for dx, dy in ((-58, -54), (58, -54), (-52, 34), (52, 34)):
        d.line((cx + dx - 12, cy + dy, cx + dx + 12, cy + dy), fill=RED, width=6)
        d.line((cx + dx, cy + dy - 12, cx + dx, cy + dy + 12), fill=RED, width=6)


def bridge(d, cx, cy, c):
    d.rectangle((cx - 96, cy + 28, cx + 96, cy + 36), fill=BLUE)
    for dx in (-72, 72):
        d.polygon([(cx + dx - 9, cy + 30), (cx + dx - 5, cy - 42),
                   (cx + dx + 5, cy - 42), (cx + dx + 9, cy + 30)], fill=c)
    d.line((cx - 88, cy - 26, cx - 18, cy - 20), fill=INK, width=11)
    d.line((cx + 20, cy - 22, cx + 88, cy - 28), fill=INK, width=11)
    d.polygon([(cx - 4, cy - 8), (cx + 14, cy + 30), (cx + 2, cy + 28)], fill=RED)


def market(d, cx, cy, c):
    pts = [(cx - 96, cy + 52), (cx - 56, cy + 22), (cx - 20, cy + 34),
           (cx + 18, cy - 6), (cx + 54, cy - 22), (cx + 96, cy - 62)]
    d.line(pts, fill=c, width=13, joint="curve")
    for px, py in pts:
        d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=c)
    d.polygon([(cx + 96, cy - 82), (cx + 96, cy - 38),
               (cx + 60, cy - 50)], fill=c)


def maple(d, cx, cy, c):
    d.polygon([(cx, cy - 74), (cx + 16, cy - 36), (cx + 54, cy - 48),
               (cx + 42, cy - 8), (cx + 72, cy + 16), (cx + 26, cy + 24),
               (cx + 18, cy + 64), (cx, cy + 36), (cx - 18, cy + 64),
               (cx - 26, cy + 24), (cx - 72, cy + 16), (cx - 42, cy - 8),
               (cx - 54, cy - 48), (cx - 16, cy - 36)], fill=RED)
    d.line((cx - 92, cy + 72, cx + 92, cy + 72), fill=c, width=7)
    d.line((cx - 70, cy + 52, cx + 70, cy + 52), fill=c, width=5)


def outage(d, cx, cy, c):
    d.polygon([(cx - 96, cy - 6), (cx + 20, cy - 30),
               (cx + 88, cy - 24), (cx + 62, cy), (cx - 44, cy + 22)], fill=c)
    d.line((cx - 86, cy + 30, cx + 66, cy + 30), fill=RED, width=8)
    d.line((cx + 30, cy + 44, cx - 30, cy + 78), fill=RED, width=12)
    d.ellipse((cx - 60, cy - 66, cx + 32, cy - 34), outline=c, width=5)


def build(path):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for gy in range(0, H, 64):
        d.line((0, gy, W, gy), fill="#121A2E", width=1)
    d.rectangle((0, 0, W, 14), fill=GOLD)
    hero = "18 NOVEMBER 2026"
    center(d, (24, 40, W - 24, 194), hero, fit(hero, W - 80, 104), INK)
    center(d, (24, 196, W - 24, 248),
           "WEDNESDAY  -  THE WORLD IN ONE PICTURE", font(36), GOLD)
    d.line((56, 270, W - 56, 270), fill="#33415E", width=4)
    cw, ch, gx, gy, x0, y0 = 292, 316, 18, 20, 56, 300
    cards = [
        (RED, "CHINA", "Trump meets Xi at APEC", leaders),
        (RED, "IRAN", "US strikes missile sites", missile),
        (RED, "UKRAINE", "Odesa; Crimea bridge", bridge),
        (GREEN, "MARKETS", "Nvidia lifts tech shares", market),
        (GOLD, "CANADA", "Tariff thaw with China", maple),
        (PURPLE, "OUTAGES", "FAA ground stop", outage),
    ]
    for i, spec in enumerate(cards):
        card(d, x0 + (i % 3) * (cw + gx), y0 + (i // 3) * (ch + gy),
             cw, ch, *spec)
    d.line((56, 966, W - 56, 966), fill="#33415E", width=4)
    center(d, (24, 970, W - 24, 1014),
           "ONE DAY  -  SIX STORIES  -  18 NOV 2026", font(32), MUTED)
    im.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    build("/opt/data/makefun/repos/news-image-20261118/entry.png")
    print("wrote entry.png")
