#!/usr/bin/env python3
"""Build the entry image for the make.fun bounty
"Sum up 23 November's world news in one image" (news-image-20261123).

Draws a 1024x1024 newspaper-style summary of the real world news of
Monday 23 November 2026, as reported that day by Just Security (Early
Edition), Al Jazeera / Reuters via Algenom, Daily News Egypt, Off the Wire
and AP News. Six stories, one per region/field, each a short headline plus
one faithful one-line summary. Text is drawn with PIL (no AI text render)
so every label is exact and legible.

Output: assets/news-20261123.png (PNG, 1024x1024, under 1 MiB).
Run: python3 tools/build_image.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "news-20261123.png")

W, H = 1024, 1024

NAVY = (14, 42, 71)
GOLD = (232, 184, 75)
WHITE = (255, 255, 255)
INK = (17, 24, 33)
GREY = (70, 80, 92)
LIGHT_ROW = (241, 244, 248)
RULE = (214, 220, 228)
FOOT_GREY = (110, 120, 132)

# Six stories of 23 November 2026 (all reported that day).
STORIES = [
    ("CLIMATE", "COP31 ends with no deal",
     "UN climate talks in Turkey close late, no deal on fossil fuels or money.",
     (30, 122, 76)),
    ("MIDDLE EAST", "US sanctions hit Iran banks",
     "Treasury targets 20+ exchange houses; Tehran claims $290bn against the US.",
     (179, 64, 42)),
    ("EUROPE", "NATO sends AWACS to Poland",
     "Early-warning jet sent after Russian missiles came down in Poland.",
     (36, 86, 166)),
    ("UKRAINE WAR", "Ukraine hits Russian ships in Libya",
     "Zelenskyy: sea drones struck two Russian vessels at Benghazi port.",
     (106, 63, 160)),
    ("MARKETS", "Asian chip stocks slide",
     "Kospi drops 3.3% as a Wall Street rout spreads doubts over AI spending.",
     (194, 112, 14)),
    ("AMERICAS", "\u2018Chapo Isidro\u2019 captured",
     "Mexico arrests Sinaloa cartel leader, one of the FBI\u2019s 10 most wanted.",
     (14, 124, 123)),
]


def font(name, size):
    """Liberation Sans (Arial-metric) with DejaVu fallback."""
    candidates = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % name,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"
        % ("-Bold" if name == "Bold" else ""),
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    f_kicker = font("Bold", 24)
    f_date = font("Bold", 74)
    f_sub = font("Regular", 25)
    f_tag = font("Bold", 20)
    f_head = font("Bold", 30)
    f_sum = font("Regular", 22)
    f_num = font("Bold", 32)
    f_foot = font("Regular", 18)

    # ---- header band ----
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.text((36, 30), "THE WORLD IN ONE IMAGE", font=f_kicker, fill=GOLD)
    d.text((34, 62), "23 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((36, 152), "MONDAY  \u00b7  SIX STORIES FROM AROUND THE WORLD",
           font=f_sub, fill=(178, 196, 216))
    d.rectangle([0, 196, W, 200], fill=GOLD)

    # ---- story rows ----
    top = 200
    row_h = 127
    for i, (tag, head, summ, color) in enumerate(STORIES):
        y0 = top + i * row_h
        if i % 2 == 1:
            d.rectangle([0, y0, W, y0 + row_h], fill=LIGHT_ROW)
        # number badge
        d.rounded_rectangle([28, y0 + 31, 92, y0 + 95], radius=10, fill=color)
        num = str(i + 1)
        nb = d.textbbox((0, 0), num, font=f_num)
        d.text((60 - (nb[2] - nb[0]) / 2, y0 + 31 + (64 - (nb[3] - nb[1])) / 2 - 2),
               num, font=f_num, fill=WHITE)
        # category tag
        d.text((114, y0 + 20), tag, font=f_tag, fill=color)
        # headline
        d.text((112, y0 + 46), head, font=f_head, fill=INK)
        # one-line summary
        d.text((112, y0 + 88), summ, font=f_sum, fill=GREY)
        if i < len(STORIES) - 1:
            d.line([(28, y0 + row_h), (W - 28, y0 + row_h)], fill=RULE, width=1)

    # ---- footer ----
    foot = "Sources: Just Security \u00b7 Al Jazeera \u00b7 Reuters \u00b7 AP News  —  all events reported on 23 Nov 2026"
    fb = d.textbbox((0, 0), foot, font=f_foot)
    d.text(((W - (fb[2] - fb[0])) / 2, 200 + 6 * row_h + 14), foot,
           font=f_foot, fill=FOOT_GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote %s (%dx%d, %d bytes)" % (OUT, W, H, size))
    assert size <= 1024 * 1024, "image over 1 MiB!"


if __name__ == "__main__":
    main()
