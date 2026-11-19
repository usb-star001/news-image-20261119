#!/usr/bin/env python3
"""Render the front page for news-image-20261119.

Draws a one-page newspaper front page for Thursday 19 November 2026 with
Pillow (installed locally). All art is drawn with PIL primitives; no images
are downloaded. Output: entry.png, 1024x1024, under 1 MiB.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)      # warm newsprint
INK = (17, 17, 17)           # near-black
SOFT_INK = (60, 60, 60)
RED = (178, 34, 34)          # classic newspaper red accent
RULE = (17, 17, 17)
LIGHT_RULE = (150, 140, 120)
CAPTION = (90, 85, 70)

LIB = "/usr/share/fonts/truetype/liberation"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = f"{LIB}/LiberationSerif-Bold.ttf"
SERIF = f"{LIB}/LiberationSerif-Regular.ttf"
SERIF_I = f"{LIB}/LiberationSerif-Italic.ttf"
SANS_B = f"{LIB}/LiberationSans-Bold.ttf"
SANS = f"{LIB}/LiberationSans-Regular.ttf"
SANS_BD = f"{DEJAVU}/DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines of text; returns y just below the block."""
    if leading is None:
        leading = int(fnt.size * 1.12)
    for line in lines:
        if align == "center" and width is not None:
            lx = x + (width - draw.textlength(line, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x, y, w, weight=2, fill=RULE):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)
    return y + weight


def kicker(draw, x, y, label, size=20):
    f = font(SANS_B, size)
    draw.text((x, y), label, font=f, fill=RED)
    return y + size + 6


def headline(draw, x, y, text, size, max_w, leading=None):
    f = font(SERIF_B, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, x, y, lines, f, leading=leading or int(size * 1.04)), lines


def deck(draw, x, y, text, size, max_w, leading=None):
    f = font(SERIF, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, x, y, lines, f, fill=SOFT_INK,
                      leading=leading or int(size * 1.25)), lines


# ---------------------------------------------------------------- illustrations

def _sky_color(t):
    """Vice City sunset gradient: indigo -> magenta -> orange."""
    top = (38, 28, 84)
    mid = (168, 52, 130)
    bot = (249, 115, 22)
    if t < 0.55:
        u = t / 0.55
        return tuple(int(top[c] + (mid[c] - top[c]) * u) for c in range(3))
    u = (t - 0.55) / 0.45
    return tuple(int(mid[c] + (bot[c] - mid[c]) * u) for c in range(3))


def _palm(draw, px, base_y, s):
    """A palm silhouette: curved trunk, fronds arcing out and drooping."""
    top_x = px + int(12 * s)
    top_y = base_y - int(58 * s)
    # trunk as 3 segments curving right
    pts = [(px, base_y), (px + int(4 * s), base_y - int(22 * s)),
           (px + int(8 * s), base_y - int(40 * s)), (top_x, top_y)]
    draw.line(pts, fill=(16, 12, 32), width=5, joint="curve")
    # fronds: each a curve that rises slightly then droops down
    for dx, dy_end in [(-52, 26), (-40, 14), (-24, 4),
                       (24, 4), (40, 14), (52, 26)]:
        seg = []
        for k in range(9):
            t = k / 8
            fx = top_x + int(dx * s * t)
            fy = top_y + int((-8 * t + (dy_end + 8) * t * t) * s)
            seg.append((fx, fy))
        draw.line(seg, fill=(16, 12, 32), width=4, joint="curve")


def vice_city(draw, x, y, w, h):
    """Sunset over Vice City: gradient sky, slatted sun, skyline, palms."""
    for i in range(h):
        draw.line([(x, y + i), (x + w, y + i)], fill=_sky_color(i / max(1, h)))
    # slatted sun, left of centre so it clears the neon sign
    cx, cy, r = x + int(w * 0.18), y + int(h * 0.46), int(h * 0.26)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 230, 138))
    for k in range(4):
        gy = cy + int(r * (0.10 + 0.22 * k))
        gh = max(2, int(2 + k * 1.5))
        if gy + gh > y + h:
            break
        draw.rectangle([cx - r, gy, cx + r, gy + gh],
                       fill=_sky_color((gy - y) / max(1, h)))
    # skyline silhouettes
    horizon = y + int(h * 0.78)
    buildings = [
        (0.00, 0.30, 0.10), (0.10, 0.44, 0.07), (0.17, 0.26, 0.09),
        (0.26, 0.52, 0.08), (0.34, 0.34, 0.10), (0.44, 0.58, 0.07),
        (0.51, 0.30, 0.11), (0.62, 0.46, 0.08), (0.70, 0.28, 0.09),
        (0.79, 0.50, 0.07), (0.86, 0.32, 0.08), (0.94, 0.42, 0.06),
    ]
    for fx, fh, fw in buildings:
        bx = x + int(w * fx)
        bw = int(w * fw)
        bh = int(h * fh)
        draw.rectangle([bx, horizon - bh, bx + bw, horizon], fill=(24, 18, 48))
        for wy in range(horizon - bh + 8, horizon - 6, 14):
            for wx in range(bx + 5, bx + bw - 4, 11):
                if (wx * 7 + wy * 13) % 5 < 2:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(253, 224, 71))
    # water strip with reflections, clipped to the box
    draw.rectangle([x, horizon, x + w, y + h], fill=(30, 20, 60))
    for i in range(6):
        ry = horizon + 5 + i * 6
        if ry > y + h - 3:
            break
        rw = int(w * (0.20 + 0.10 * ((i * 37) % 5)))
        rx = x + int(w * (0.06 + 0.11 * ((i * 23) % 7)))
        rx2 = min(rx + rw, x + w - 4)
        draw.line([(rx, ry), (rx2, ry)], fill=(244, 114, 182), width=2)
    # palms inside the edges so their fronds stay in frame
    _palm(draw, x + int(w * 0.09), y + h, 1.15)
    _palm(draw, x + int(w * 0.89), y + h, 0.95)
    # neon sign
    neon = font(SANS_BD, 40)
    label = "VICE CITY"
    tw = draw.textlength(label, font=neon)
    lx = x + (w - tw) // 2
    ly = y + int(h * 0.08)
    for dx, dy, col in [(-2, -2, (168, 85, 247)), (2, 2, (236, 72, 153))]:
        draw.text((lx + dx, ly + dy), label, font=neon, fill=col)
    draw.text((lx, ly), label, font=neon, fill=(255, 255, 255))


def voyager_band(draw, x, y, w, h):
    """Starfield strip with a small probe and dashed path."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 12, 40))
    rnd = random.Random(19112026)
    for _ in range(60):
        sx = x + rnd.randint(2, w - 2)
        sy = y + rnd.randint(2, h - 2)
        r = rnd.choice([1, 1, 2])
        draw.ellipse([sx, sy, sx + r, sy + r], fill=(255, 255, 255))
    for i in range(0, w - 130, 16):
        draw.line([(x + 8 + i, y + h // 2), (x + 8 + i + 8, y + h // 2)],
                  fill=(147, 197, 253), width=2)
    px, py = x + w - 92, y + h // 2
    draw.ellipse([px - 15, py - 15, px + 15, py + 15], fill=(212, 175, 55))
    draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(245, 158, 11))
    draw.rectangle([px + 12, py - 5, px + 32, py + 5], fill=(226, 232, 240))
    draw.line([(px + 32, py), (px + 50, py - 11)], fill=(226, 232, 240), width=3)
    # label plate so the headline never collides with dashes or stars
    return px - 58


# ---------------------------------------------------------------- page assembly

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # side margin
    CW = W - 2 * M              # content width
    y = 24

    # ---- masthead
    mast = font(SERIF_B, 70)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, y), title, font=mast, fill=INK)
    y += 84
    y = hrule(d, M, y, CW, 5)
    y += 5
    dl = font(SANS_B, 24)
    d.text((M, y), "THURSDAY, 19 NOVEMBER 2026", font=dl, fill=INK)
    right = "GLOBAL EDITION"
    rw = d.textlength(right, font=dl)
    d.text((W - M - rw, y), right, font=dl, fill=RED)
    y += 32
    y = hrule(d, M, y, CW, 2)
    y += 8

    # ---- lead story: GTA VI
    y = kicker(d, M, y, "GAMING  •  LEAD STORY", 20)
    y, _ = headline(d, M, y, "GRAND THEFT AUTO VI LAUNCHES WORLDWIDE", 54, CW)
    y += 2
    y, _ = deck(d, M, y,
                "After a 13-year wait, Rockstar's return to Vice City arrives — "
                "and millions of players are already in.",
                22, CW)
    y += 6
    vice_city(d, M, y, CW, 108)
    y += 108 + 5
    cap = font(SERIF_I, 16)
    d.text((M, y), "Vice City at dusk. (Illustration)", font=cap, fill=CAPTION)
    y += 20
    y = hrule(d, M, y, CW, 2)
    y += 10

    # ---- two-column grid, two rows (text-led; the lead art carries the visuals)
    col_w = (CW - 24) // 2
    grid = [
        ("MIDDLE EAST",
         "IRAN HITS U.S. BASE IN KUWAIT AS GULF WAR WIDENS",
         "Drones target Ali Al Salem air base and sites in Bahrain after the "
         "U.S. strike on a missile site on Qeshm Island."),
        ("DIPLOMACY",
         "TRUMP, XI AND PUTIN SET FOR SHENZHEN TALKS",
         "The three leaders meet on the sidelines of the APEC summit."),
        ("BUSINESS",
         "ANTHROPIC'S $81.3BN IPO — THE BIGGEST EVER",
         "Shares priced at $83; trading begins today on Nasdaq under the "
         "ticker ANT."),
        ("TECHNOLOGY",
         "NVIDIA HALTS CHINA CHIP SHIPMENTS",
         "H-series sales to China end as acting chief Colette Kress takes "
         "over after Jensen Huang's exit."),
    ]
    for row in range(2):
        row_top = y
        row_bottom = row_top
        for col in range(2):
            kick, head, dk = grid[row * 2 + col]
            x = M + col * (col_w + 24)
            cy = row_top
            cy = kicker(d, x, cy, kick, 18)
            cy, _ = headline(d, x, cy, head, 30, col_w)
            cy += 2
            cy, _ = deck(d, x, cy, dk, 18, col_w)
            row_bottom = max(row_bottom, cy)
        y = row_bottom + 8
        y = hrule(d, M, y, CW, 1, fill=LIGHT_RULE)
        y += 6

    # ---- Voyager band
    y = kicker(d, M, y, "SCIENCE", 18)
    voyager_band(d, M, y, CW, 36)
    vtext = "VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH"
    vf = font(SANS_B, 19)
    vtw = d.textlength(vtext, font=vf)
    d.rectangle([M + 6, y + 3, M + 6 + vtw + 16, y + 33], fill=(10, 12, 40))
    d.text((M + 14, y + 9), vtext, font=vf, fill=(255, 255, 255))
    y += 36 + 4
    y, _ = deck(d, M, y,
                "NASA will confirm the milestone at a news conference today, "
                "nearly 50 years after launch.",
                18, CW)
    y += 6
    y = hrule(d, M, y, CW, 2)
    y += 8

    # ---- briefs strip
    briefs = [
        ("GAZA", "Israeli tanks push into central Gaza in the first major "
         "ground operation since the ceasefire."),
        ("EUROPE", "EU proposes a €45bn loan for Ukraine, to be repaid once "
         "Russia pays reparations."),
        ("WASHINGTON", "Democrats nominate Hakeem Jeffries for Speaker; he "
         "would be the first Black Speaker."),
        ("INDIA", "Cyclone Akvan nears India's east coast."),
    ]
    bw = (CW - 3 * 16) // 4
    top = y
    for i, (tag, txt) in enumerate(briefs):
        x = M + i * (bw + 16)
        bf = font(SANS_B, 16)
        d.text((x, top), tag, font=bf, fill=RED)
        tf = font(SERIF, 15)
        lines = wrap(d, txt, tf, bw)
        text_block(d, x, top + 20, lines, tf, fill=SOFT_INK, leading=19)
        if i < 3:
            d.line([(x + bw + 8, top), (x + bw + 8, top + 76)],
                   fill=LIGHT_RULE, width=1)
    y = top + 78

    # ---- footer
    fy = H - 28
    hrule(d, M, fy - 8, CW, 1, fill=LIGHT_RULE)
    ff = font(SANS, 14)
    foot = "Compiled from AP, Reuters, Bloomberg, The Hindu and NASA reporting."
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 2), foot, font=ff, fill=CAPTION)
    print("content bottom y =", y, "footer at", fy)

    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    import os
    print("saved entry.png", os.path.getsize("entry.png"), "bytes",
          page.size)
