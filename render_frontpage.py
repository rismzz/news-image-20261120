#!/usr/bin/env python3
"""Render the 20 November 2026 world-news broadsheet (1024x1024 PNG).

Dense front page: masthead with the giant date, a lead story, a
timeline strip of the day so far, six section grids of short
verified stories, a markets ticker and a visible DATE CHECK line.
Every story below was first reported on 20 November 2026 (any
time zone); nothing from 19 November is carried over as today's
news. Pure Pillow, no network, deterministic output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (246, 241, 231)
INK = (22, 35, 58)
RED = (180, 35, 24)
BLUE = (29, 78, 137)
GOLD = (138, 109, 27)
GREY = (90, 92, 96)
LIGHT = (255, 255, 255)
NAVY = (18, 32, 56)
RULE = (198, 190, 172)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF, 46)
F_DATE = font(SANS_B, 19)
F_KICK = font(SANS_B, 13)
F_LEAD = font(SERIF, 29)
F_SUM = font(SANS, 15)
F_MINI = font(SANS_B, 15)
F_MINI_TXT = font(SANS, 13)
F_TIME = font(SANS_B, 13)
F_TL = font(SANS, 12)
F_SEC = font(SANS_B, 15)
F_ITEM = font(SANS, 13)
F_ITEM_B = font(SANS_B, 13)
F_TICK = font(SANS_B, 12)
F_FOOT = font(SANS, 12)
F_FOOT_B = font(SANS_B, 12)

LEAD_HEAD = "TRUMP PUTS IRAN WAR DECISION OFF TO 2027"
LEAD_SUM = (
    "\u201cI\u2019ll see what happens after Jan 1,\u201d the US president says \u2014 "
    "no rush on a decision as Gulf tensions simmer and the region waits."
)

MINIS = [
    ("VOYAGER 1, ONE LIGHT-DAY OUT",
     "NASA confirms the probe is now a full light-day from Earth \u2014 and \u201cnot done yet\u201d."),
    ("CYCLONE AKVAN BEARS DOWN",
     "300,000 evacuated in Odisha; 423 rescue teams out as the storm nears landfall."),
]

# (time IST, text) — every item first reported 20 Nov 2026.
TIMELINE = [
    ("01:23", "GTA VI sales pass The Odyssey\u2019s $1.8bn global run"),
    ("01:30", "Hayabusa2 engine trouble ends asteroid landing plan"),
    ("01:34", "NASA confirms Voyager 1\u2019s light-day milestone"),
    ("01:43", "Akvan: 300,000 evacuated, schools shut in Odisha"),
    ("03:06", "Trump: no rush on Iran decision, looks to 2027"),
    ("04:49", "Justice Varma: resignation \u2018not admission of guilt\u2019"),
]

# (section, [(bold lead, rest), ...]) — 5 stories per section.
SECTIONS = [
    ("WORLD", [
        ("ICJ: Myanmar committed genocide", "against the Rohingya, UN court rules"),
        ("Europe ready for Russia talks", "on ending the war in Ukraine, leaders say"),
        ("Houthis hit Riyadh tower", "Saudi wealth-fund tower damaged in attack"),
        ("US\u2013Venezuela restore ties", "deal to resume military cooperation signed"),
        ("N. Korea expands Yongbyon", "uranium enrichment grows, watchdog says"),
    ]),
    ("ASIA & INDIA", [
        ("Akvan nears landfall", "Odisha braces; 80,000 moved in Andhra too"),
        ("Modi meets William & Kate", "in Delhi; India\u2013UK ties on the agenda"),
        ("Justice Varma writes to Lok Sabha", "\u2018resignation not admission of guilt\u2019"),
        ("Railways cancel 10 trains", "23 more diverted as Akvan approaches"),
        ("NEET leak: charges vs 14", "Delhi court frames charges; trial 25 Nov"),
    ]),
    ("SCIENCE & SPACE", [
        ("Voyager 1, a light-day out", "24 hours for a signal to reach the probe"),
        ("Hayabusa2 changes course", "engine fault rules out asteroid landing"),
        ("Star seen swallowing companion", "astronomers witness engulfment first-hand"),
        ("Pew: faiths to swap places", "Islam set to pass Christianity as largest"),
        ("Economist\u2019 World Ahead 2027", "cover drops: \u2018Not going quietly\u2019"),
    ]),
    ("MARKETS", [
        ("Dow \u22122.19% to 49,097", "S&P \u22122.02%, Nasdaq \u22122.25%"),
        ("10-year yield tops 5%", "dollar near 19-month high at 103.9"),
        ("Gold $3,726, down 3.6%", "lowest since September 2025"),
        ("Bitcoin $62,362, down 3.0%", "crypto slide deepens; Ether $1,806"),
        ("Sensex +1.21%, Nifty +1.14%", "Indian stocks rally against the grain"),
    ]),
    ("SPORT", [
        ("Nicholls 113* rescues NZ", "New Zealand 243/5, Day 1 vs India"),
        ("Bavuma ruled out", "South Africa lose captain for decider"),
        ("Carlsen shock forfeit", "chess world fuming over \u2018favouritism\u2019"),
        ("India 2\u20131 Pakistan", "10th SAFF Championship title sealed"),
        ("India beat Malaysia", "Hong Kong Open badminton win"),
    ]),
    ("CULTURE & TECH", [
        ("GTA VI tops $1.8bn run", "sales pass The Odyssey\u2019s global total"),
        ("GTA VI\u2019s NPCs build its world", "NPR on the crowds of Leonida"),
        ("Anthropic valued at $1.5tn", "AI boom reprices the field again"),
        ("Musk: \u2018I\u2019m not MAGA\u2019", "regrets $500m spent on midterms"),
        ("Grindr\u2019s $120-a-month AI", "tier reads private chats, critics wary"),
    ]),
]

TICKER = (
    "MARKETS \u2014 SENSEX +1.21%  \u2022  NIFTY +1.14%  \u2022  DOW \u22122.19%  \u2022  "
    "GOLD $3,726  \u2022  BTC $62,362  \u2022  BRENT $93.14  \u2022  "
    "10-YR 5%+  \u2022  DXY 103.9"
)

FOOT = (
    "DATE CHECK \u2014 Every story on this page happened or was first reported on "
    "20 November 2026 (any time zone). Sources: Reuters \u2022 BBC \u2022 NYT \u2022 "
    "NDTV \u2022 Times of India \u2022 The Hindu \u2022 NPR \u2022 Al Jazeera \u2022 "
    "Space \u2022 Marketscreener."
)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt, leading):
    return len(lines) * leading


def draw_masthead(d):
    d.rectangle([0, 0, W, 8], fill=RED)
    d.text((16, 20), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    right = "31 STORIES \u2022 UTC TIMELINE \u2022 DATE CHECK"
    d.text((W - 16 - d.textlength(right, font=F_KICK), 32), right,
           font=F_KICK, fill=GREY)
    d.text((16, 76), "FRIDAY, 20 NOVEMBER 2026  \u2014  WORLD CHILDREN\u2019S DAY",
           font=F_DATE, fill=RED)
    d.line([16, 108, W - 16, 108], fill=INK, width=3)
    d.line([16, 112, W - 16, 112], fill=RULE, width=1)


def draw_lead(d):
    y = 120
    d.text((16, y), "LEAD", font=F_KICK, fill=RED)
    head = wrap(d, LEAD_HEAD, F_LEAD, 620)
    assert len(head) <= 2, f"lead headline wraps to {len(head)} lines"
    yy = y + 20
    for line in head:
        d.text((16, yy), line, font=F_LEAD, fill=INK)
        yy += 34
    summ = wrap(d, LEAD_SUM, F_SUM, 620)
    assert len(summ) <= 2, f"lead summary wraps to {len(summ)} lines"
    for line in summ:
        d.text((16, yy + 2), line, font=F_SUM, fill=INK)
        yy += 19
    # Right column: two mini stories with a red rule.
    x = 668
    d.line([x - 14, y + 4, x - 14, y + 118], fill=RED, width=3)
    my = y
    for title, txt in MINIS:
        t = wrap(d, title, F_MINI, 330)
        assert len(t) <= 2, f"mini title wraps to {len(t)} lines"
        for line in t:
            d.text((x, my), line, font=F_MINI, fill=INK)
            my += 18
        for line in wrap(d, txt, F_MINI_TXT, 330):
            d.text((x, my), line, font=F_MINI_TXT, fill=GREY)
            my += 16
        my += 10
    d.line([16, 248, W - 16, 248], fill=RULE, width=1)


def draw_timeline(d):
    y = 256
    d.text((16, y), "THE DAY SO FAR \u2014 TIMES IST (UTC+5:30)",
           font=F_KICK, fill=BLUE)
    d.line([16, y + 20, W - 16, y + 20], fill=BLUE, width=2)
    col_w = 160
    for i, (t, txt) in enumerate(TIMELINE):
        x = 16 + i * col_w
        if i:
            d.line([x - 8, y + 26, x - 8, y + 78], fill=RULE, width=1)
        d.text((x, y + 26), t, font=F_TIME, fill=RED)
        lines = wrap(d, txt, F_TL, col_w - 12)
        assert len(lines) <= 3, f"timeline item {i} wraps to {len(lines)} lines"
        ly = y + 44
        for line in lines:
            d.text((x, ly), line, font=F_TL, fill=INK)
            ly += 14
    d.line([16, 344, W - 16, 344], fill=RULE, width=1)


def draw_grid(d):
    cell_w, cell_h, gap = 496, 196, 8
    for idx, (name, items) in enumerate(SECTIONS):
        col, row = idx % 2, idx // 2
        x = 16 + col * (cell_w + gap)
        y = 352 + row * (cell_h + gap)
        d.rectangle([x, y, x + cell_w, y + cell_h], outline=RULE, width=1)
        d.rectangle([x, y, x + cell_w, y + 26], fill=NAVY)
        d.text((x + 10, y + 5), name, font=F_SEC, fill=LIGHT)
        d.text((x + cell_w - 10 - d.textlength(f"{len(items)} STORIES", font=F_KICK),
                y + 7), f"{len(items)} STORIES", font=F_KICK, fill=(200, 205, 215))
        iy = y + 36
        for lead, rest in items:
            lead_lines = wrap(d, lead, F_ITEM_B, cell_w - 20)
            rest_lines = wrap(d, rest, F_ITEM, cell_w - 20)
            assert len(lead_lines) == 1, f"item lead wraps: {lead!r}"
            assert len(rest_lines) == 1, f"item rest wraps: {rest!r}"
            d.text((x + 10, iy), "\u2022 " + lead, font=F_ITEM_B, fill=INK)
            d.text((x + 24, iy + 15), rest, font=F_ITEM, fill=GREY)
            iy += 31
        assert iy <= y + cell_h, f"section {name} overflows its cell"


def draw_footer(d):
    d.rectangle([0, 962, W, 992], fill=NAVY)
    tick = TICKER
    assert d.textlength(tick, font=F_TICK) <= W - 32, "ticker too wide"
    d.text((16, 970), tick, font=F_TICK, fill=LIGHT)
    lines = wrap(d, FOOT, F_FOOT, W - 32)
    assert len(lines) <= 2, f"footer wraps to {len(lines)} lines"
    fy = 994
    for line in lines:
        d.text((16, fy), line, font=F_FOOT, fill=INK)
        fy += 13


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_timeline(d)
    draw_grid(d)
    draw_footer(d)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
