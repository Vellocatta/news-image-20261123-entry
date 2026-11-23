#!/usr/bin/env python3
"""Draw the 23 November 2026 front page (1024x1024) from stories.py.

Written from scratch in this session. Layout: masthead, lead story with
drawn hero art, a row of three secondary stories, an 8-story featured
grid, and 38 one-line briefs in three columns. Every text block is
measured before it is drawn; a block that cannot fit its box raises
instead of clipping.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from stories import BRIEFS, FEATURED

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


PALETTES = {
    "navy": dict(paper="#f7f2e7", ink="#14181f", accent="#1e3a5f",
                 accent2="#b45309", muted="#5b6470", rule="#1e3a5f",
                 art_bg="#1e3a5f", art_fg="#f7f2e7", art_mid="#b45309"),
    "crimson": dict(paper="#f7f2e7", ink="#1c1a17", accent="#8b1a1a",
                    accent2="#1e3a5f", muted="#5b6470", rule="#8b1a1a",
                    art_bg="#8b1a1a", art_fg="#f7f2e7", art_mid="#e8b23a"),
    "teal": dict(paper="#f2f5f2", ink="#14201d", accent="#0f5f5c",
                accent2="#b45309", muted="#55645f", rule="#0f5f5c",
                art_bg="#0f5f5c", art_fg="#f2f5f2", art_mid="#e8b23a"),
    "cream": dict(paper="#fbf8f1", ink="#111111", accent="#111111",
                  accent2="#8b1a1a", muted="#555555", rule="#111111",
                  art_bg="#222222", art_fg="#fbf8f1", art_mid="#8b1a1a"),
    "black": dict(paper="#ffffff", ink="#000000", accent="#000000",
                 accent2="#c00000", muted="#444444", rule="#000000",
                 art_bg="#111111", art_fg="#ffffff", art_mid="#c00000"),
}


def wrap(text, fnt, width, draw):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, fnt, width, max_lines, draw):
    """Wrap text; raise if it needs more than max_lines."""
    lines = wrap(text, fnt, width, draw)
    if len(lines) > max_lines:
        raise ValueError(f"OVERFLOW ({len(lines)}>{max_lines}): {text!r}")
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(draw, x, y0, y1, fill, width=1):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---------------------------------------------------------------- art motifs
def art_sea(d, x0, y0, x1, y1, P):
    """Gulf at dusk: tanker and warship silhouettes, smoke, orange horizon."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    d.rectangle([x0, y0 + (y1 - y0) * 0.42, x1, y0 + (y1 - y0) * 0.55],
                fill=P["art_mid"])
    d.rectangle([x0, y0 + (y1 - y0) * 0.55, x1, y1], fill="#0e2438")
    w, h = x1 - x0, y1 - y0
    # tanker hull + bridge
    d.rectangle([x0 + w * 0.08, y0 + h * 0.62, x0 + w * 0.55, y0 + h * 0.74],
                fill="#0a0a0a")
    d.rectangle([x0 + w * 0.40, y0 + h * 0.50, x0 + w * 0.48, y0 + h * 0.62],
                fill="#0a0a0a")
    d.rectangle([x0 + w * 0.14, y0 + h * 0.58, x0 + w * 0.18, y0 + h * 0.62],
                fill="#0a0a0a")
    # warship silhouette
    d.polygon([(x0 + w * 0.62, y0 + h * 0.74), (x0 + w * 0.94, y0 + h * 0.74),
               (x0 + w * 0.90, y0 + h * 0.66), (x0 + w * 0.66, y0 + h * 0.66)],
              fill="#1a1a1a")
    d.rectangle([x0 + w * 0.72, y0 + h * 0.56, x0 + w * 0.76, y0 + h * 0.66],
                fill="#1a1a1a")
    # smoke plume
    for i, r in enumerate((26, 20, 14)):
        d.ellipse([x0 + w * 0.42 + i * 6, y0 + h * 0.30 - i * 8,
                   x0 + w * 0.42 + i * 6 + r, y0 + h * 0.30 - i * 8 + r],
                  fill="#d8d2c4")
    # waves
    for i in range(5):
        yy = y0 + h * (0.80 + i * 0.04)
        d.arc([x0 + 8, yy, x0 + w - 8, yy + 14], 0, 180, fill="#3a6a8a")


def art_globe(d, x0, y0, x1, y1, P):
    """Cracked globe for COP31."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#3f7a4e",
              outline=P["art_fg"], width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=P["art_fg"], width=2)
    d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 90, 270,
          fill=P["art_fg"], width=2)
    # crack
    d.line([(cx - 6, cy - r + 4), (cx + 4, cy - r // 3), (cx - 4, cy + r // 4),
            (cx + 6, cy + r - 6)], fill=P["art_mid"], width=3)


def art_chart(d, x0, y0, x1, y1, P):
    """Falling candlesticks, one green bounce."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    candles = [(0.06, 0.30, 0.55, 0.42, "#c0392b"), (0.22, 0.42, 0.68, 0.55, "#c0392b"),
               (0.38, 0.55, 0.80, 0.68, "#c0392b"), (0.54, 0.68, 0.86, 0.76, "#c0392b"),
               (0.70, 0.76, 0.60, 0.50, "#2e7d32"), (0.84, 0.50, 0.34, 0.28, "#2e7d32")]
    for fx, top, bot, _top2, col in candles:
        cx = x0 + w * fx
        d.line([(cx, y0 + h * top), (cx, y0 + h * bot)], fill=col, width=2)
        d.rectangle([cx - 5, y0 + h * min(top, bot) + 4, cx + 5,
                     y0 + h * max(top, bot) - 4], fill=col)


def art_ship(d, x0, y0, x1, y1, P):
    """Sinking frigate: tilted hull, smoke, waves."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    d.polygon([(x0 + w * 0.15, y0 + h * 0.72), (x0 + w * 0.80, y0 + h * 0.50),
               (x0 + w * 0.86, y0 + h * 0.58), (x0 + w * 0.22, y0 + h * 0.80)],
              fill="#0a0a0a")
    d.rectangle([x0 + w * 0.55, y0 + h * 0.36, x0 + w * 0.60, y0 + h * 0.52],
                fill="#0a0a0a")
    for i, r in enumerate((20, 15, 10)):
        d.ellipse([x0 + w * 0.55 + i * 5, y0 + h * 0.18 - i * 6,
                   x0 + w * 0.55 + i * 5 + r, y0 + h * 0.18 - i * 6 + r],
                  fill="#d8d2c4")
    for i in range(3):
        yy = y0 + h * (0.82 + i * 0.05)
        d.arc([x0 + 6, yy, x0 + w - 6, yy + 12], 0, 180, fill="#3a6a8a")


def art_dome(d, x0, y0, x1, y1, P):
    """Capitol dome silhouette on a blue wave."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    cx = x0 + w // 2
    d.rectangle([cx - 4, y0 + h * 0.18, cx + 4, y0 + h * 0.30], fill=P["art_fg"])
    d.pieslice([cx - w * 0.16, y0 + h * 0.22, cx + w * 0.16, y0 + h * 0.62],
               180, 360, fill=P["art_fg"])
    d.rectangle([x0 + w * 0.22, y0 + h * 0.60, x0 + w * 0.78, y0 + h * 0.68],
                fill=P["art_fg"])
    d.rectangle([x0 + w * 0.16, y0 + h * 0.68, x0 + w * 0.84, y0 + h * 0.76],
                fill=P["art_fg"])
    d.arc([x0 + 6, y0 + h * 0.82, x0 + w - 6, y0 + h * 0.96], 0, 180,
          fill=P["art_mid"], width=3)


def art_refinery(d, x0, y0, x1, y1, P):
    """Refinery towers and flame."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    for fx, fw, fh in ((0.12, 0.10, 0.55), (0.30, 0.08, 0.70), (0.48, 0.12, 0.45)):
        d.rectangle([x0 + w * fx, y0 + h * (1 - fh), x0 + w * (fx + fw), y0 + h * 0.92],
                    fill="#0a0a0a")
    d.polygon([(x0 + w * 0.66, y0 + h * 0.92), (x0 + w * 0.78, y0 + h * 0.92),
               (x0 + w * 0.72, y0 + h * 0.55)], fill="#0a0a0a")
    d.polygon([(x0 + w * 0.70, y0 + h * 0.50), (x0 + w * 0.78, y0 + h * 0.50),
               (x0 + w * 0.74, y0 + h * 0.30)], fill=P["art_mid"])
    d.ellipse([x0 + w * 0.70, y0 + h * 0.22, x0 + w * 0.78, y0 + h * 0.36],
              fill=P["art_mid"])


def art_rubble(d, x0, y0, x1, y1, P):
    """Collapsed building, rescue beam of light."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    d.polygon([(x0 + w * 0.10, y0 + h * 0.85), (x0 + w * 0.45, y0 + h * 0.45),
               (x0 + w * 0.80, y0 + h * 0.85)], fill="#0a0a0a")
    d.polygon([(x0 + w * 0.55, y0 + h * 0.85), (x0 + w * 0.75, y0 + h * 0.60),
               (x0 + w * 0.95, y0 + h * 0.85)], fill="#333333")
    d.polygon([(x0 + w * 0.30, y0 + h * 0.15), (x0 + w * 0.38, y0 + h * 0.15),
               (x0 + w * 0.62, y0 + h * 0.85), (x0 + w * 0.48, y0 + h * 0.85)],
              fill=P["art_mid"])


def art_quake(d, x0, y0, x1, y1, P):
    """Seismograph trace."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    mid = y0 + h // 2
    pts = []
    xs = [0.02, 0.10, 0.18, 0.26, 0.34, 0.42, 0.50, 0.58, 0.66, 0.74, 0.82, 0.90, 0.98]
    ys = [0.50, 0.50, 0.48, 0.52, 0.30, 0.72, 0.18, 0.85, 0.35, 0.60, 0.45, 0.52, 0.50]
    for fx, fy in zip(xs, ys):
        pts.append((x0 + w * fx, y0 + h * fy))
    d.line(pts, fill=P["art_mid"], width=3)
    d.line([(x0, mid), (x1, mid)], fill=P["art_fg"], width=1)


def art_ball(d, x0, y0, x1, y1, P):
    """Football on grass stripes."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    for i in range(4):
        d.rectangle([x0, y0 + h * (0.72 + i * 0.07), x1, y0 + h * (0.79 + i * 0.07)],
                    fill="#2e7d32" if i % 2 == 0 else "#256b29")
    cx, cy = (x0 + x1) // 2, y0 + h * 0.42
    r = min(w, h) // 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=P["art_fg"],
              outline="#111111", width=2)
    d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)],
              fill="#111111")


def art_circuit(d, x0, y0, x1, y1, P):
    """Circuit board traces and nodes."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    nodes = [(0.20, 0.30), (0.50, 0.20), (0.80, 0.35), (0.30, 0.65),
             (0.60, 0.70), (0.85, 0.75)]
    for i in range(len(nodes) - 1):
        x_a, y_a = nodes[i]
        x_b, y_b = nodes[i + 1]
        d.line([(x0 + w * x_a, y0 + h * y_a), (x0 + w * x_b, y0 + h * y_a),
                (x0 + w * x_b, y0 + h * y_b)], fill=P["art_mid"], width=2)
    for fx, fy in nodes:
        d.ellipse([x0 + w * fx - 5, y0 + h * fy - 5, x0 + w * fx + 5,
                   y0 + h * fy + 5], fill=P["art_fg"])


def art_tower(d, x0, y0, x1, y1, P):
    """Eiffel-style tower silhouette."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    cx = x0 + w // 2
    d.polygon([(cx - w * 0.28, y0 + h * 0.88), (cx - w * 0.05, y0 + h * 0.12),
               (cx + w * 0.05, y0 + h * 0.12), (cx + w * 0.28, y0 + h * 0.88)],
              fill="#0a0a0a")
    d.rectangle([x0 + w * 0.30, y0 + h * 0.60, x0 + w * 0.70, y0 + h * 0.66],
                fill=P["art_bg"])
    d.rectangle([cx - 3, y0 + h * 0.06, cx + 3, y0 + h * 0.14], fill="#0a0a0a")


def art_peaks(d, x0, y0, x1, y1, P):
    """Two mountain ranges meeting."""
    d.rectangle([x0, y0, x1, y1], fill=P["art_bg"])
    w, h = x1 - x0, y1 - y0
    d.polygon([(x0, y0 + h * 0.85), (x0 + w * 0.30, y0 + h * 0.30),
               (x0 + w * 0.60, y0 + h * 0.85)], fill="#3a5a7a")
    d.polygon([(x0 + w * 0.40, y0 + h * 0.85), (x0 + w * 0.70, y0 + h * 0.20),
               (x0 + w, y0 + h * 0.85)], fill=P["art_fg"])
    d.polygon([(x0 + w * 0.64, y0 + h * 0.32), (x0 + w * 0.70, y0 + h * 0.20),
               (x0 + w * 0.76, y0 + h * 0.32)], fill="#ffffff")


ART = {"sea": art_sea, "globe": art_globe, "chart": art_chart,
       "ship": art_ship, "dome": art_dome, "refinery": art_refinery,
       "rubble": art_rubble, "quake": art_quake, "ball": art_ball,
       "circuit": art_circuit, "tower": art_tower, "peaks": art_peaks}


# ------------------------------------------------------------------- layout
def draw_masthead(d, P, big=False):
    name = "THE WORLD TODAY"
    f_name = font(SERIF_B, 62 if big else 56)
    f_date = font(SANS_B, 17)
    f_tag = font(SANS, 13)
    wname = d.textlength(name, font=f_name)
    d.text(((W - wname) / 2, 6), name, font=f_name, fill=P["ink"])
    hline(d, 24, W - 24, 76, P["rule"], 3)
    date = "MONDAY, 23 NOVEMBER 2026"
    d.text((24, 82), date, font=f_date, fill=P["accent"])
    tag = "ONE DAY  •  ONE PAGE  •  THE WORLD"
    wt = d.textlength(tag, font=f_tag)
    d.text((W - 24 - wt, 84), tag, font=f_tag, fill=P["muted"])
    hline(d, 24, W - 24, 104, P["ink"], 1)


def draw_lead(d, P, story, big_art=False):
    x0, y0 = 24, 112
    if big_art:
        ax0, ay0, ax1, ay1 = 24, y0, 480, y0 + 208
        tx0 = 496
        tw = W - 24 - tx0
        max_head = 3
    else:
        ax0, ay0, ax1, ay1 = 672, y0, 1000, y0 + 196
        tx0 = x0
        tw = 656 - tx0
        max_head = 2
    ART[story["art"]](d, ax0, ay0, ax1, ay1, P)
    d.text((ax0, ay1 + 4), story["kicker"] + "  •  DRAWN FROM REPORTS",
           font=font(SANS, 11), fill=P["muted"])
    f_kick = font(SANS_B, 15)
    d.text((tx0, y0), story["kicker"], font=f_kick, fill=P["accent2"])
    f_head = font(SERIF_B, 38)
    lines = fit(story["headline"], f_head, tw, max_head, d)
    y = draw_lines(d, lines, tx0, y0 + 22, f_head, P["ink"], 46)
    f_deck = font(SANS, 17)
    dlines = fit(story["deck"], f_deck, tw, 2, d)
    y = draw_lines(d, dlines, tx0, y + 8, f_deck, P["ink"], 22)
    if y > 320:
        raise ValueError(f"LEAD OVERFLOW ends {y}: {story['headline']!r}")
    hline(d, 24, W - 24, 326, P["ink"], 2)


def draw_secondary(d, P, stories):
    cols = [(24, 330), (356, 330), (688, 330)]
    cw = 312
    for (x0, y0), s in zip(cols, stories):
        ART[s["art"]](d, x0, y0, x0 + cw, y0 + 52, P)
        f_kick = font(SANS_B, 12)
        d.text((x0, y0 + 56), s["kicker"], font=f_kick, fill=P["accent2"])
        f_head = font(SERIF_B, 20)
        lines = fit(s["headline"], f_head, cw, 2, d)
        y = draw_lines(d, lines, x0, y0 + 74, f_head, P["ink"], 23)
        f_deck = font(SANS, 13)
        dlines = fit(s["deck"], f_deck, cw, 3, d)
        y = draw_lines(d, dlines, x0, y + 2, f_deck, P["ink"], 15)
        if y > 498:
            raise ValueError(f"SECONDARY OVERFLOW ends {y}: {s['headline']!r}")
    hline(d, 24, W - 24, 502, P["ink"], 1)


def draw_featured(d, P, stories):
    # 4 columns x 2 rows, cells 242 wide, 132 tall
    for i, s in enumerate(stories):
        col, row = i % 4, i // 4
        x0 = 24 + col * 248
        y0 = 510 + row * 132
        cw = 242
        f_kick = font(SANS_B, 11)
        d.text((x0, y0), s["kicker"], font=f_kick, fill=P["accent2"])
        f_head = font(SERIF_B, 16)
        lines = fit(s["headline"], f_head, cw, 2, d)
        y = draw_lines(d, lines, x0, y0 + 18, f_head, P["ink"], 20)
        f_deck = font(SANS, 12)
        dlines = fit(s["deck"], f_deck, cw, 3, d)
        y = draw_lines(d, dlines, x0, y + 3, f_deck, P["ink"], 15)
        if y > y0 + 128:
            raise ValueError(f"FEATURED OVERFLOW ends {y}: {s['headline']!r}")
        if col < 3:
            vline(d, x0 + cw + 3, y0 + 2, y0 + 122, "#c9c2b2")
    hline(d, 24, W - 24, 778, P["ink"], 2)


def draw_briefs(d, P):
    y0 = 786
    f_head = font(SANS_B, 16)
    d.text((24, y0), "IN BRIEF", font=f_head, fill=P["accent"])
    hline(d, 24, W - 24, y0 + 22, P["rule"], 1)
    # 3 columns: 13 / 13 / 12 briefs, one line each, 13 px leading
    f_b = font(SANS, 12)
    cols = [BRIEFS[0:13], BRIEFS[13:26], BRIEFS[26:38]]
    for ci, group in enumerate(cols):
        x0 = 24 + ci * 330
        y = y0 + 30
        for b in group:
            lines = fit("•  " + b, f_b, 318, 1, d)
            draw_lines(d, lines, x0, y, f_b, P["ink"], 13)
            y += 13
        if y > 990:
            raise ValueError(f"BRIEFS OVERFLOW ends {y}")
        if ci < 2:
            vline(d, x0 + 322, y0 + 28, y0 + 28 + 13 * 13, "#c9c2b2")
    hline(d, 24, W - 24, 990, P["ink"], 2)
    f_foot = font(SANS, 11)
    d.text((24, 998), "THE WORLD TODAY  •  MONDAY 23 NOVEMBER 2026  •  ALL TIMES UTC",
           font=f_foot, fill=P["muted"])
    d.text((W - 24 - d.textlength("PAGE ONE", font=f_foot), 998), "PAGE ONE",
           font=f_foot, fill=P["muted"])


def render(variant):
    lead_idx = variant["lead"]
    palette = PALETTES[variant["palette"]]
    order = [FEATURED[lead_idx]] + [s for i, s in enumerate(FEATURED)
                                     if i != lead_idx]
    img = Image.new("RGB", (W, H), palette["paper"])
    d = ImageDraw.Draw(img)
    draw_masthead(d, palette, big=variant.get("big_masthead", False))
    draw_lead(d, palette, order[0], big_art=variant.get("big_art", False))
    draw_secondary(d, palette, order[1:4])
    draw_featured(d, palette, order[4:12])
    draw_briefs(d, palette)
    return img


VARIANTS = {
    "v1-navy-iran": dict(lead=0, palette="navy"),
    "v2-crimson-cop": dict(lead=1, palette="crimson"),
    "v3-teal-markets": dict(lead=2, palette="teal"),
    "v4-cream-iran": dict(lead=0, palette="cream"),
    "v5-navy-merkury": dict(lead=3, palette="navy"),
    "v6-black-iran": dict(lead=0, palette="black"),
    "v7-navy-democrats": dict(lead=4, palette="navy"),
    "v8-crimson-iran": dict(lead=0, palette="crimson"),
    "v9-navy-iran-bigart": dict(lead=0, palette="navy", big_art=True),
    "v10-teal-cop": dict(lead=1, palette="teal"),
}


def main():
    name = sys.argv[1]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(f"candidates/{name}.png")
    variant = VARIANTS[name]
    img = render(variant)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"{name}: {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
