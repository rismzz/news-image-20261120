#!/usr/bin/env python3
"""Render the 20 November 2026 broadsheet: 'THE WORLD IN ONE DAY'.

Draws a dense 1024x1024 front page with Pillow (DejaVu fonts, no
network): giant dated masthead, lead story, two minis, a UTC timeline
strip, an 8-section grid of 40 stories (headline + one-line summary),
a markets ticker and a visible DATE CHECK line. Every story was first
reported on Friday 20 November 2026, in some time zone.

Deterministic: the same input always writes the same PNG bytes.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14

PAPER = (247, 242, 231)
INK = (17, 17, 17)
MUTED = (74, 74, 74)
RED = (163, 18, 18)
BLUE = (26, 58, 107)
RULE = (17, 17, 17)
LIGHT_RULE = (120, 110, 95)
BOX = (238, 231, 214)
TIMELINE_BG = (232, 226, 208)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

DATE_LINE = "FRIDAY, 20 NOVEMBER 2026"
MASTHEAD = "THE WORLD IN ONE DAY"
SUBLINE = "43 STORIES  ·  ONE DAY  ·  ALL FIRST REPORTED FRIDAY 20 NOVEMBER 2026"

LEAD_KICKER = "LEAD  ·  THE HAGUE — INTERNATIONAL COURT OF JUSTICE"
LEAD_HEAD = "MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES"
LEAD_SUM = ("The ICJ finds Myanmar responsible for genocide against the Rohingya — "
            "the first such ruling against a state. A landmark day for international justice.")

MINIS = [
    ("SHENZHEN",
     "Trump, Xi and Putin issue joint peace declaration",
     "First three-way summit ends with a four-point declaration."),
    ("WALL STREET",
     "Nasdaq −5.28% wipes out its 2026 gains",
     "AI rout drags the S&P 500 to a seventh straight loss; Dow −950."),
]

TIMELINE = [
    ("02:00 UTC", "Akvan makes landfall near Gopalpur, Odisha"),
    ("06:00 UTC", "Akvan weakens to a deep depression inland"),
    ("MORNING", "ICJ: Myanmar committed genocide"),
    ("MIDDAY", "UK and EU seal post-Brexit trade deal"),
    ("AFTERNOON", "COP31 draft drops fossil-fuel phase-out"),
    ("21:00 UTC", "Wall St closes: Nasdaq −5.28%"),
]

# 8 sections x 5 stories: (headline, one-line summary).
SECTIONS = [
    ("WORLD", [
        ("Kyiv bridges hit in overnight barrage",
         "Russia strikes three Kyiv bridges; nine killed, embassies damaged."),
        ("EU approves €1bn in arms aid for Kyiv",
         "Council backs joint weapons buying; delivery due by end-2027."),
        ("UK pledges 1,000+ drones for Ukraine",
         "£260m package of long-range drones and kit announced."),
        ("Kenya discharges its last Ebola patient",
         "42-day countdown to an Ebola-free declaration begins."),
        ("Dozens missing as migrant boat capsizes",
         "Boat goes down off Senegal; search under way at Yenne."),
    ]),
    ("EUROPE", [
        ("UK and EU seal post-Brexit trade deal",
         "Food trade, linked carbon markets and youth mobility agreed."),
        ("Merz rejects a new Yalta over Europe",
         "Germany: no great-power deal on Europe without Europeans."),
        ("Estonia to shut border with Russia",
         "Tallinn acts after a GRU-linked sabotage attack."),
        ("Denmark backs Greenland–US security pact",
         "Parliament approves trilateral security agreement."),
        ("Italy hit by nationwide strike",
         "Workers and students protest over the cost of living."),
    ]),
    ("AMERICAS", [
        ("Senate passes energy permitting bill",
         "Bipartisan overhaul clears 62–33; House action still needed."),
        ("White House fires national cyber director",
         "Sean Cairncross out after a week of tech outages."),
        ("Trump pardons Pete Rose posthumously",
         "Baseball's banned hits king pardoned by the president."),
        ("NYC to close Rikers Island jail by 2032",
         "Mayor unveils plan to shut the notorious jail complex."),
        ("Bukele registers for a third term",
         "El Salvador's president seeks re-election again."),
    ]),
    ("MIDDLE EAST", [
        ("Houthi missile hits Riyadh tower",
         "Blast damages the Saudi sovereign wealth fund's PIF tower."),
        ("Tanker on fire in the Strait of Hormuz",
         "Vessel hit a mine as Iran steps up tanker attacks."),
        ("Israeli troops cross Gaza ceasefire line",
         "First incursion past the Yellow Line since the truce."),
        ("Trump puts Iran war decision off to 2027",
         "'See what happens after Jan 1,' he says of a strike."),
        ("US and Venezuela sign military pact",
         "Cooperation deal signed in Caracas."),
    ]),
    ("ASIA & INDIA", [
        ("Cyclone Akvan makes landfall in Odisha",
         "Storm crosses near Gopalpur; winds 70–80 km/h, gusts to 90."),
        ("Akvan weakens to a deep depression",
         "IMD: system over south coastal Odisha by 11:30 IST."),
        ("Modi meets William and Kate",
         "The Prince and Princess of Wales meet India's PM."),
        ("Justice Varma: resignation 'not guilt'",
         "Judge says quitting is not an admission of guilt."),
        ("NEET leak: charges filed",
         "Charges filed over the medical exam paper leak."),
    ]),
    ("SCIENCE & SPACE", [
        ("Voyager 1 reaches one light-day out",
         "NASA probe is now a full light-day from Earth."),
        ("Hayabusa2 asteroid landing called off",
         "Engine trouble ends JAXA's asteroid touchdown plan."),
        ("Star caught swallowing its companion",
         "Astronomers watch a star engulf its binary partner."),
        ("'Supermountains' found under Antarctica",
         "Himalaya-sized ancient ranges mapped beneath the ice."),
        ("HMS Vengeance sets 217-day patrol record",
         "UK nuclear submarine's seven months under water."),
    ]),
    ("CULTURE & TECH", [
        ("GTA VI passes The Odyssey's $1.8bn run",
         "Rockstar's epic overtakes the film's box-office haul."),
        ("Anthropic slides on day two after IPO",
         "Shares fall after a record Nasdaq debut."),
        ("Protesters demand human control of AI",
         "Crowds rally after Anthropic's listing in the US."),
        ("US auctions first deep-sea mining leases",
         "Sale goes ahead despite a court ruling for wildlife."),
        ("Musk: 'I'm not MAGA'",
         "The billionaire distances himself from the movement."),
    ]),
    ("SPORT", [
        ("India bowl out New Zealand for 368",
         "Nicholls 175* and Phillips 118; Bumrah takes four."),
        ("India A thrash Nepal by 306 runs",
         "Tilak and Kushagra hit tons in Rising Stars opener."),
        ("Bengaluru FC go top with 2–0 win",
         "Martínez and Williams sink Mumbai City in the ISL."),
        ("Pochettino calls for 'love' at Man Utd",
         "New boss urges unity before his first match."),
        ("Bavuma ruled out of second Test",
         "South Africa captain misses Bangladesh clash in Centurion."),
    ]),
]

TICKER = ("DOW 48,147 −1.93% · S&P 500 6,910 −3.70% · NASDAQ 22,618 −5.28% · "
          "GOLD $3,527 −4.3% · BITCOIN $58,955 −4.8% · 10-YR 4.91% · "
          "WTI $84.10 +1.1% · VIX 39.5")

DATE_CHECK = ("DATE CHECK — Every story on this page was first reported on Friday 20 November 2026, "
              "in some time zone. No 19 November story is carried as today's news.")
SOURCES = "Sources: Reuters · BBC · NYT · AP · IMD · IANS · Investopedia · Euronews · One Turn"

WARNINGS = []


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt, max_w, label):
    """Truncate with an ellipsis if a single line cannot fit; warn."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_w(draw, text[:mid] + ell, fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    WARNINGS.append("%s truncated: %r" % (label, text))
    return text[:lo] + ell


def center(draw, y, text, fnt, fill=INK):
    draw.text(((W - text_w(draw, text, fnt)) / 2, y), text, font=fnt, fill=fill)


def hrule(draw, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

def draw_masthead(draw):
    y = 10
    center(draw, y, MASTHEAD, F_TITLE(40))
    y = 56
    center(draw, y, DATE_LINE, F_SANS_B(25))
    y = 88
    center(draw, y, SUBLINE, F_SANS_B(11), fill=MUTED)
    hrule(draw, 106, width=2)
    return 114


def draw_lead(draw, y):
    # Kicker + 2-line headline + 2-line summary, full width.
    draw.text((MARGIN, y), LEAD_KICKER, font=F_SANS_B(11), fill=RED)
    y += 16
    lines = wrap(draw, LEAD_HEAD, F_TITLE(27), W - 2 * MARGIN)
    assert len(lines) <= 2, "lead headline wraps to %d lines" % len(lines)
    for line in lines:
        draw.text((MARGIN, y), line, font=F_TITLE(27), fill=INK)
        y += 32
    for line in wrap(draw, LEAD_SUM, F_SANS(13), W - 2 * MARGIN):
        draw.text((MARGIN, y), line, font=F_SANS(13), fill=MUTED)
        y += 17
    hrule(draw, y + 4, width=1, fill=LIGHT_RULE)
    return y + 10


def draw_minis(draw, y):
    box_w = (W - 2 * MARGIN - 10) // 2
    box_h = 52
    for i, (kicker, head, summ) in enumerate(MINIS):
        x0 = MARGIN + i * (box_w + 10)
        draw.rectangle([x0, y, x0 + box_w, y + box_h], fill=BOX,
                       outline=RULE, width=1)
        tx = x0 + 8
        draw.text((tx, y + 5), kicker, font=F_SANS_B(10), fill=RED)
        head_fit = fit_one_line(draw, head, F_SANS_B(12), box_w - 16,
                                "mini headline %d" % i)
        draw.text((tx, y + 20), head_fit, font=F_SANS_B(12), fill=INK)
        summ_fit = fit_one_line(draw, summ, F_SANS(10), box_w - 16,
                                "mini summary %d" % i)
        draw.text((tx, y + 36), summ_fit, font=F_SANS(10), fill=MUTED)
    return y + box_h + 6


def draw_timeline(draw, y):
    h = 52
    draw.rectangle([MARGIN, y, W - MARGIN, y + h], fill=TIMELINE_BG,
                   outline=RULE, width=1)
    # Tab label overlapping the top border (costs no height).
    tab = "  THE DAY IN UTC  "
    tab_w = text_w(draw, tab, F_SANS_B(10))
    draw.rectangle([MARGIN + 8, y - 7, MARGIN + 8 + tab_w, y + 7],
                   fill=PAPER)
    draw.text((MARGIN + 8, y - 7), tab, font=F_SANS_B(10), fill=RED)
    col_w = (W - 2 * MARGIN) // len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        x0 = MARGIN + i * col_w + 8
        draw.text((x0, y + 8), when, font=F_SANS_B(10), fill=BLUE)
        lines = wrap(draw, what, F_SANS(9), col_w - 16)
        assert len(lines) <= 2, "timeline item %d wraps to %d lines" % (i, len(lines))
        ly = y + 21
        for line in lines:
            draw.text((x0, ly), line, font=F_SANS(9), fill=INK)
            ly += 11
        if i:
            draw.line([(MARGIN + i * col_w, y + 6),
                       (MARGIN + i * col_w, y + h - 6)],
                      fill=LIGHT_RULE, width=1)
    return y + h + 6


def draw_section(draw, x0, y, cell_w, cell_h, title, stories):
    draw.text((x0, y), title, font=F_SANS_B(13), fill=RED)
    draw.line([(x0, y + 17), (x0 + cell_w, y + 17)], fill=RULE, width=2)
    sy = y + 22
    for head, summ in stories:
        head_fit = fit_one_line(draw, head, F_SANS_B(11), cell_w - 4,
                                "headline %s" % head)
        draw.text((x0, sy), head_fit, font=F_SANS_B(11), fill=INK)
        summ_fit = fit_one_line(draw, summ, F_SANS(10), cell_w - 4,
                                "summary %s" % summ)
        draw.text((x0, sy + 12), summ_fit, font=F_SANS(10), fill=MUTED)
        sy += 25
    return sy


def draw_grid(draw, y):
    cols, rows = 2, 4
    gap = 10
    cell_w = (W - 2 * MARGIN - gap) // cols
    cell_h = 148
    for idx, (title, stories) in enumerate(SECTIONS):
        assert len(stories) == 5, "section %s has %d stories" % (title, len(stories))
        col, row = idx % cols, idx // cols
        x0 = MARGIN + col * (cell_w + gap)
        y0 = y + row * cell_h
        end = draw_section(draw, x0, y0, cell_w, cell_h, title, stories)
        assert end <= y0 + cell_h, "section %s overflows cell" % title
        if col == 0:
            draw.line([(x0 + cell_w + 5, y0 + 2),
                       (x0 + cell_w + 5, y0 + cell_h - 12)],
                      fill=LIGHT_RULE, width=1)
    return y + rows * cell_h

def draw_ticker(draw, y):
    hrule(draw, y, width=2)
    ticker = fit_one_line(draw, TICKER, F_SANS_B(10), W - 2 * MARGIN,
                          "ticker")
    center(draw, y + 7, ticker, F_SANS_B(10))
    hrule(draw, y + 24, width=2)
    return y + 30


def draw_datecheck(draw, y):
    lines = wrap(draw, DATE_CHECK, F_SANS_B(11), W - 2 * MARGIN)
    assert len(lines) <= 2, "date check wraps to %d lines" % len(lines)
    for line in lines:
        center(draw, y, line, F_SANS_B(11), fill=RED)
        y += 14
    center(draw, y + 2, SOURCES, F_SANS(9), fill=MUTED)
    return y + 15


def render(out_path):
    n_stories = sum(len(s) for _, s in SECTIONS)
    assert len(SECTIONS) == 8, "expected 8 sections"
    assert n_stories == 40, "expected 40 grid stories, got %d" % n_stories
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_minis(draw, y)
    y = draw_timeline(draw, y)
    y = draw_grid(draw, y)
    y = draw_ticker(draw, y + 4)
    y = draw_datecheck(draw, y + 2)
    assert y <= H - 4, "layout overflows: y=%d" % y
    img.save(out_path, format="PNG", optimize=True)
    data = open(out_path, "rb").read()
    print("wrote %s %dx%d %d bytes sha256=%s" % (
        out_path, W, H, len(data), hashlib.sha256(data).hexdigest()))
    print("stories: %d grid + lead + 2 minis = 43 headline items" % n_stories)
    if WARNINGS:
        print("WARNINGS (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  " + w)
    else:
        print("no truncation warnings")
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
