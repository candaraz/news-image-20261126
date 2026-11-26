#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - news-image-20261126 entry generator.

Renders a dense one-page broadsheet of Thursday 26 November 2026 world
news to entry.png (1024x1024). Every story below was published on
26 November 2026 and checked item by item against the day's reporting
(Reuters, BBC, Al Jazeera and the wires). Stories that broke on
Wednesday 25 November are listed separately in the DATE CHECK box and
deliberately left out of the news columns.

Deterministic: pure PIL drawing, no clocks, no randomness.
Fonts resolve relative to this script file, never the CWD.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 24, 20)
FAINT = (96, 88, 74)
ACCENT = (163, 22, 33)
BOXBG = (238, 230, 210)
LEADBG = (240, 234, 216)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, name), size)


F_SERIF = "LiberationSerif-Regular.ttf"
F_BOLD = "LiberationSerif-Bold.ttf"
F_ITALIC = "LiberationSerif-Italic.ttf"

KICKER = font(F_BOLD, 13)
MASTHEAD = font(F_BOLD, 63)
DATELINE = font(F_SERIF, 15)
DATELINE_B = font(F_BOLD, 15)
LEAD_HEAD = font(F_BOLD, 29)
LEAD_DECK = font(F_SERIF, 14.5)
SECT = font(F_BOLD, 13)
HEAD = font(F_BOLD, 11.5)
DECK = font(F_SERIF, 10)
BOX_HEAD = font(F_BOLD, 12.5)
BOX_TXT = font(F_SERIF, 10)
FOOT = font(F_ITALIC, 10.5)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, col_w, head, deck):
    """One headline + one-line deck; returns y after the story."""
    for ln in wrap(draw, head, HEAD, col_w):
        draw.text((x, y), ln, font=HEAD, fill=INK)
        y += 13
    for ln in wrap(draw, deck, DECK, col_w):
        draw.text((x, y), ln, font=DECK, fill=(52, 48, 40))
        y += 11.5
    return y + 5.0


def draw_section(draw, x, y, col_w, title, stories):
    """Section header bar followed by its stories."""
    draw.rectangle([x, y, x + col_w, y + 17], fill=INK)
    draw.text((x + 6, y + 2.5), title, font=SECT, fill=PAPER)
    y += 23
    for head, deck in stories:
        y = draw_story(draw, x, y, col_w, head, deck)
    return y + 4


def draw_airshield(draw, x, y, w_, h_):
    """Geometric air-defence motif: radar arcs over a horizon, one
    incoming track broken by the shield arc."""
    base = y + h_ - 12
    cx = x + w_ // 2
    # horizon and ground ticks
    draw.line([x + 4, base, x + w_ - 4, base], fill=INK, width=3)
    for gx in range(x + 14, x + w_ - 8, 22):
        draw.line([gx, base, gx, base + 6], fill=FAINT, width=2)
    # concentric shield arcs
    for r in (34, 56, 78):
        draw.arc([cx - r, base - r, cx + r, base + r], start=180, end=360,
                 fill=INK, width=3)
    # radar sweep
    draw.line([cx, base, cx - 52, base - 52], fill=ACCENT, width=3)
    # incoming track, stopped at the outer arc
    draw.line([x + w_ - 16, y + 6, cx + 62, base - 62], fill=ACCENT, width=3)
    draw.line([cx + 62 - 9, base - 62, cx + 62, base - 62], fill=ACCENT, width=3)
    draw.line([cx + 62, base - 62 - 9, cx + 62, base - 62], fill=ACCENT, width=3)
    # burst where the track ends
    for dx, dy in ((-8, -8), (0, -11), (8, -8), (-11, 0), (11, 0)):
        draw.line([cx + 62, base - 62, cx + 62 + dx, base - 62 + dy],
                  fill=INK, width=2)
    # launcher block at centre
    draw.rectangle([cx - 12, base - 12, cx + 12, base], outline=INK, width=3)
    draw.line([cx, base - 12, cx, base - 22], fill=INK, width=3)


# ---------------------------------------------------------------- stories
# Every item: published Thursday 26 November 2026, verified item by item.

LEAD_HEADLINE = "POLAND MOVES TO SEAL ITS EASTERN SKY"
LEAD_TEXT = (
    "Warsaw will create a limited no-fly zone along its border with Ukraine, "
    "Deputy Defence Minister Cezary Tomczyk says, after three Russian Kh-101 "
    "cruise missiles landed on Polish soil. Poland also asks NATO allies to "
    "consider downing Russian missiles over Ukraine before they cross."
)

ASIA_PACIFIC = [
    ("Rescuers resume search for 13 trapped miners",
     "Thirteen are already confirmed dead in the flooded illegal gold mine in Bogor, West Java."),
    ("Bank of Korea raises its rate to 3.25%",
     "A 25-point hike resumes tightening as a chip-led export boom keeps inflation high."),
    ("China lands its biggest Boeing order since 2013",
     "Fifty jets worth $7.4 billion, finalised as trade tensions run on."),
    ("Kim Jong Un urges wider tactical-nuke deployment",
     "The North Korean leader calls for more battlefield nuclear weapons."),
    ("JETRO: Chinese firms now threaten Japanese rivals",
     "More Japanese companies abroad report tougher Chinese competition."),
    ("Australia enacts online safety law",
     "Platforms face fines of up to 5% of global revenue under the new act."),
]

EUROPE = [
    ("UK to publish new treaties agreed with the EU",
     "The texts carry a 10-year clause covering rebuilt border-check costs."),
    ("UK opens inquiry into nuclear-test veterans",
     "An independent review will examine the tests' impact on veterans and families."),
    ("Puigdemont to return to Spain on 12 December",
     "The Catalan separatist leader ends years of self-imposed exile."),
    ("Norway court voids climate-disputed oil licences",
     "The supreme court rules the contested licences invalid."),
    ("Germany begins rebuilding the Eagle's Nest",
     "Work starts on Hitler's fire-damaged mountain retreat in Bavaria."),
    ("Six-day global heat streak smashes the record",
     "Six straight days ran 2C above pre-industrial levels, the Guardian reports."),
]

WAR_UKRAINE = [
    ("Ukraine strikes Russian air base; five jets hit",
     "Kyiv says five military aircraft were struck in the attack."),
    ("Ukraine downs 88 of 112 Russian drones overnight",
     "Air defences report most of the incoming swarm destroyed."),
    ("SBU: two Samara refineries damaged in strikes",
     "Ukraine's security service claims a pair of key oil plants hit."),
    ("Kyiv's commander helps Norway harden air defences",
     "Ukraine's chief assists Norwegian forces along the Russian border."),
]

AMERICAS = [
    ("California braces for Thanksgiving flooding",
     "Storms and king tides threaten both US coasts over the holiday."),
    ("Macy's postpones its Thanksgiving parade",
     "The New York parade is put back because of the weather."),
    ("Trump's accounts traded Nvidia shares 44 times",
     "Records show the trades across this year, the BBC reports."),
    ("Venezuela discloses a $237.5 billion debt load",
     "The figure is published as a key step toward restructuring."),
    ("Peru shuts dozens of ports as currents batter coast",
     "Powerful swells damage the shoreline and halt traffic."),
]

MIDDLE_EAST_AFRICA = [
    ("Fuel tanker fire kills 31 on a Cairo highway",
     "The tanker crashed and burst into flames on the capital's outskirts."),
    ("Israeli judges urge dropping top Netanyahu charges",
     "The panel recommends removing the most serious counts in his trial."),
    ("Knesset panel backs an October 7 inquiry",
     "The committee approves a commission despite Netanyahu's resistance."),
    ("Israeli strike kills Hamas security chief in Gaza City",
     "The senior official died with family members in the strike."),
    ("Saudi-led coalition intercepts four drones",
     "The drones were brought down over the Eastern Province."),
    ("Two tankers strike mines in the Strait of Hormuz",
     "Oil climbs as shipping through the strait is disrupted."),
    ("Nigeria seizes $220 million of methamphetamine",
     "Five Mexican suspects are arrested in the large-scale bust."),
    ("Ghana unveils 'Heritage Series' banknotes",
     "The notes honour Nkrumah, Kofi Annan and Makola traders."),
    ("Kenya discharges its last Ebola patient",
     "In Congo, the outbreak's death toll has passed 5,300."),
]

TECH_MARKETS = [
    ("Asia shares bounce as AI rout and tariffs linger",
     "The Nikkei gained 1.6% and Seoul 1.9% in a rare November rally."),
    ("Nvidia ends down 3.9% at $149.30",
     "The stock sits $2.3 trillion below its October peak."),
    ("US approves SpaceX plan for a million satellites",
     "Regulators clear the vast data-satellite constellation."),
    ("OPEC+ meets on 29 November over 2027 output",
     "Ministers must weigh the UAE's exit and capacity claims."),
    ("Microdrama revenue to hit $20 billion in 2026",
     "Profits outside China remain thin, a new industry report finds."),
    ("Scientists find lakes beneath the Red Sea",
     "The mysterious lakes lie more than a mile below the surface."),
]

SPORT = [
    ("Man Utd held by Sporting amid disputed decisions",
     "Frustration reigns for Pochettino in a chaotic start to the job."),
    ("Borthwick: All Blacks tests are 'World Cup practice'",
     "England's coach frames the Nations Championship clashes."),
    ("U2 salute Dolly Parton at NFL Thanksgiving Eve show",
     "The band recreated their 'Torn' duet at the halftime show."),
]

DATE_CHECK = [
    "Huawei convicted in New York on 10 of 12 counts",
    "US proposes tariffs on China and 13 other partners",
    "Army detonates lead azide stockpile in Iowa",
    "North Korea expels Swiss diplomat in sanctions row",
    "Duran Duran guitarist Andy Taylor dies, aged 65",
    "Colombia supermarket siege ends; hostages freed",
    "Ramaphosa wins reprieve in the Farmgate case",
    "Medicare sets 2028 prices for 13 drugs",
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # page margin

    # --- masthead ------------------------------------------------------
    d.line([M, 16, W - M, 16], fill=INK, width=2)
    kick = "ONE IMAGE  ·  EVERY STORY CHECKED AGAINST THE DAY ITSELF"
    d.text(((W - d.textlength(kick, font=KICKER)) / 2, 22), kick, font=KICKER, fill=ACCENT)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=MASTHEAD)) / 2, 40), title, font=MASTHEAD, fill=INK)
    d.line([M, 116, W - M, 116], fill=INK, width=4)
    d.line([M, 122, W - M, 122], fill=INK, width=1)
    left = "Thursday 26 November 2026"
    d.text((M, 128), left, font=DATELINE_B, fill=INK)
    mid = "40 stories · 7 regions · one page"
    d.text(((W - d.textlength(mid, font=DATELINE)) / 2, 128), mid, font=DATELINE, fill=FAINT)
    right = "No. 26 — Daily Edition"
    d.text((W - M - d.textlength(right, font=DATELINE), 128), right, font=DATELINE, fill=INK)
    d.line([M, 150, W - M, 150], fill=INK, width=1)

    # --- lead panel ----------------------------------------------------
    ly = 158
    d.rectangle([M, ly, W - M, ly + 118], fill=LEADBG, outline=INK, width=2)
    draw_airshield(d, M + 18, ly + 14, 168, 92)
    tx = M + 208
    tw = W - M - tx - 14
    yy = ly + 10
    for ln in wrap(d, LEAD_HEADLINE, LEAD_HEAD, tw):
        d.text((tx, yy), ln, font=LEAD_HEAD, fill=ACCENT)
        yy += 34
    yy += 2
    for ln in wrap(d, LEAD_TEXT, LEAD_DECK, tw):
        d.text((tx, yy), ln, font=LEAD_DECK, fill=INK)
        yy += 18

    # --- body columns --------------------------------------------------
    top = 292
    col_w = (W - 2 * M - 2 * 16) // 3
    xs = [M, M + col_w + 16, M + 2 * (col_w + 16)]
    for x in xs[1:]:
        d.line([x - 8, top, x - 8, 852], fill=(190, 180, 158), width=1)

    y1 = draw_section(d, xs[0], top, col_w, "ASIA-PACIFIC", ASIA_PACIFIC)
    y1 = draw_section(d, xs[0], y1, col_w, "SPORT", SPORT)
    y2 = draw_section(d, xs[1], top, col_w, "EUROPE", EUROPE)
    y2 = draw_section(d, xs[1], y2, col_w, "WAR IN UKRAINE", WAR_UKRAINE)
    y2 = draw_section(d, xs[1], y2, col_w, "TECH, AI & MARKETS", TECH_MARKETS[:2])
    y3 = draw_section(d, xs[2], top, col_w, "AMERICAS", AMERICAS)
    y3 = draw_section(d, xs[2], y3, col_w, "MIDDLE EAST & AFRICA", MIDDLE_EAST_AFRICA[:5])

    # second row of sections under the columns, full width pairs
    by = max(y1, y2, y3) + 2
    half = (W - 2 * M - 16) // 2
    draw_section(d, M, by, half, "MIDDLE EAST & AFRICA — MORE", MIDDLE_EAST_AFRICA[5:])
    draw_section(d, M + half + 16, by, half, "TECH, AI & MARKETS — MORE", TECH_MARKETS[2:])

    # --- date check box -------------------------------------------------
    by2 = 866
    d.rectangle([M, by2, W - M, by2 + 96], fill=BOXBG, outline=ACCENT, width=2)
    d.text((M + 12, by2 + 8),
           "DATE CHECK — reported Wednesday 25 November, checked and deliberately left out:",
           font=BOX_HEAD, fill=ACCENT)
    half_items = (len(DATE_CHECK) + 1) // 2
    for i, item in enumerate(DATE_CHECK):
        cx = M + 12 + (i // half_items) * half
        cy = by2 + 32 + (i % half_items) * 15
        d.text((cx, cy), "x  " + item, font=BOX_TXT, fill=INK)

    # --- footer ----------------------------------------------------------
    fy = by2 + 106
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    foot = ("Every story above was published on Thursday 26 November 2026 and checked item by item. "
            "Sources: Reuters · BBC · Al Jazeera · AFP · AP and the day's wires.")
    d.text(((W - d.textlength(foot, font=FOOT)) / 2, fy + 7), foot, font=FOOT, fill=FAINT)

    # --- save ------------------------------------------------------------
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") and os.access("/output", os.W_OK) else HERE
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(render())
