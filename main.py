#!/usr/bin/env python3
"""Render the "THE WORLD IN ONE DAY" front page for Thursday 26 November 2026.

A single-page newspaper made entirely of deterministic PIL drawing calls:
no clocks, no randomness, no network.  The page is laid out on a 1024x1024
canvas with three story columns, a lead story box with a small radar/sector
diagram, a date-check panel, and a footer crediting the day's wires.

The rendered PNG is written as ``entry.png`` into the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (created when missing); when the
variable is unset the file lands next to this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
PAPER = (247, 242, 231)     # page background
INK = (26, 24, 20)          # headlines, rules, section bars
LEADBG = (240, 234, 216)    # lead story box fill
DCBG = (238, 230, 210)      # date-check panel fill
RED = (163, 22, 33)         # accents: tagline, lead headline, panel frame
FAINT = (96, 88, 74)        # footer, dateline centre, diagram ticks
BODY = (52, 48, 40)         # story body copy

# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------
PAGE = 1024
EDGE = 28                   # left/right margin of the content span
SPAN = PAGE - EDGE          # 996, right edge of the content span
COLW = 312                  # story column width
COLX = (28, 356, 684)       # story column left edges
BARH = 18                   # section bar height

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def serif(weight, size):
    """Load one of the Liberation Serif faces bundled beside this script."""
    path = os.path.join(SCRIPT_DIR, "LiberationSerif-%s.ttf" % weight)
    return ImageFont.truetype(path, size)


# Type sizes (several are fractional on purpose: the page was designed with
# them, and FreeType honours fractional pixel sizes).
F_TAGLINE = serif("Bold", 13)
F_MASTHEAD = serif("Bold", 63)
F_DATELINE = serif("Bold", 15)
F_DATELINE_R = serif("Regular", 15)
F_LEAD_HEAD = serif("Bold", 29)
F_LEAD_BODY = serif("Regular", 14.5)
F_BAR = serif("Bold", 13)
F_HEADLINE = serif("Bold", 11.5)
F_BODY = serif("Regular", 10)
F_DC_TITLE = serif("Bold", 12.5)
F_DC_ITEM = serif("Regular", 10)
F_FOOTER = serif("Italic", 10.5)

MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def text_width(text, font):
    return MEASURE.textlength(text, font=font)


def wrap(text, font, width):
    """Greedy word wrap: pack whole words while the line fits ``width``."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if current and text_width(trial, font) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


# --------------------------------------------------------------------------
# Page furniture (fixed strings)
# --------------------------------------------------------------------------
TAGLINE = "ONE IMAGE  \u00b7  EVERY STORY CHECKED AGAINST THE DAY ITSELF"
MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE_LEFT = "Thursday 26 November 2026"
DATELINE_MID = "40 stories \u00b7 7 regions \u00b7 one page"
DATELINE_RIGHT = "No. 26 \u2014 Daily Edition"

LEAD_HEADLINE = "POLAND MOVES TO SEAL ITS EASTERN SKY"
LEAD_TEXT = (
    "Warsaw will create a limited no-fly zone along its border with Ukraine, "
    "Deputy Defence Minister Cezary Tomczyk says, after three Russian Kh-101 "
    "cruise missiles landed on Polish soil. Poland also asks NATO allies to "
    "consider downing Russian missiles over Ukraine before they cross."
)

DC_TITLE = ("DATE CHECK \u2014 reported Wednesday 25 November, checked and "
            "deliberately left out:")
DC_LEFT = [
    "Huawei convicted in New York on 10 of 12 counts",
    "US proposes tariffs on China and 13 other partners",
    "Army detonates lead azide stockpile in Iowa",
    "North Korea expels Swiss diplomat in sanctions row",
]
DC_RIGHT = [
    "Duran Duran guitarist Andy Taylor dies, aged 65",
    "Colombia supermarket siege ends; hostages freed",
    "Ramaphosa wins reprieve in the Farmgate case",
    "Medicare sets 2028 prices for 13 drugs",
]

FOOTER = ("Every story above was published on Thursday 26 November 2026 and "
          "checked item by item. Sources: Reuters \u00b7 BBC \u00b7 Al Jazeera "
          "\u00b7 AFP \u00b7 AP and the day's wires.")

# --------------------------------------------------------------------------
# Story data: (section label, [(headline, body-or-None), ...])
# --------------------------------------------------------------------------
ASIA = ("ASIA-PACIFIC", [
    ("Rescuers resume search for 13 trapped miners",
     "Thirteen are already confirmed dead in the flooded illegal gold mine "
     "in Bogor, West Java."),
    ("Bank of Korea raises its rate to 3.25%",
     "A 25-point hike resumes tightening as a chip-led export boom keeps "
     "inflation high."),
    ("China lands its biggest Boeing order since 2013",
     "Fifty jets worth $7.4 billion, finalised as trade tensions run on."),
    ("Kim Jong Un urges wider tactical-nuke deployment",
     "The North Korean leader calls for more battlefield nuclear weapons."),
    ("JETRO: Chinese firms now threaten Japanese rivals",
     "More Japanese companies abroad report tougher Chinese competition."),
    ("Australia enacts online safety law",
     "Platforms face fines of up to 5% of global revenue under the new act."),
])
SPORT = ("SPORT", [
    ("Man Utd held by Sporting amid disputed decisions",
     "Frustration reigns for Pochettino in a chaotic start to the job."),
    ("Borthwick: All Blacks tests are 'World Cup practice'",
     "England's coach frames the Nations Championship clashes."),
    ("U2 salute Dolly Parton at NFL Thanksgiving Eve show",
     "The band recreated their 'Tom' duet at the halftime show."),
])
EUROPE = ("EUROPE", [
    ("UK to publish new treaties agreed with the EU",
     "The texts carry a 10-year clause covering rebuilt border-check costs."),
    ("UK opens inquiry into nuclear-test veterans",
     "An independent review will examine the tests' impact on veterans and "
     "families."),
    ("Puigdemont to return to Spain on 12 December",
     "The Catalan separatist leader ends years of self-imposed exile."),
    ("Norway court voids climate-disputed oil licences",
     "The supreme court rules the contested licences invalid."),
    ("Germany begins rebuilding the Eagle's Nest",
     "Work starts on Hitler's fire-damaged mountain retreat in Bavaria."),
    ("Six-day global heat streak smashes the record",
     "Six straight days ran 2C above pre-industrial levels, the Guardian "
     "reports."),
])
WAR = ("WAR IN UKRAINE", [
    ("Ukraine strikes Russian air base; five jets hit",
     "Kyiv says five military aircraft were struck in the attack."),
    ("Ukraine downs 88 of 112 Russian drones overnight",
     "Air defences report most of the incoming swarm destroyed."),
    ("SBU: two Samara refineries damaged in strikes",
     "Ukraine's security service claims a pair of key oil plants hit."),
    ("Kyiv's commander helps Norway harden air defences",
     "Ukraine's chief assists Norwegian forces along the Russian border."),
])
TECH = ("TECH, AI & MARKETS", [
    ("Asia shares bounce as AI rout and tariffs linger",
     "The Nikkei gained 1.6% and Seoul 1.9% in a rare November rally."),
    ("Nvidia ends down 3.9% at $149.30",
     "The stock sits $2.3 trillion below its October peak."),
])
AMERICAS = ("AMERICAS", [
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
])
MEAST = ("MIDDLE EAST & AFRICA", [
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
])
MEAST_MORE = ("MIDDLE EAST & AFRICA \u2014 MORE", [
    ("Two tankers strike mines in the Strait of Hormuz",
     "Oil climbs as shipping through the strait is disrupted."),
    ("Nigeria seizes $220 million of methamphetamine",
     "Five Mexican suspects are arrested in the large-scale bust."),
    ("Ghana unveils 'Heritage Series' banknotes",
     "The notes honour Nkrumah, Kofi Annan and Makola traders."),
    ("Kenya discharges its last Ebola patient", None),
])
TECH_MORE = ("TECH, AI & MARKETS \u2014 MORE", [
    ("US approves SpaceX plan for a million satellites",
     "Regulators clear the vast data-satellite constellation."),
    ("OPEC+ meets on 29 November over 2027 output",
     "Ministers must weigh the UAE's exit and capacity claims."),
    ("Microdrama revenue to hit $20 billion in 2026",
     "Profits outside China remain thin, a new industry report finds."),
    ("Scientists find lakes beneath the Red Sea", None),
])


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------
def centred_x(text, font):
    """Float left edge that centres ``text`` on the page (subpixel-exact)."""
    return (PAGE - text_width(text, font)) / 2.0


def draw_header(d):
    d.rectangle([EDGE, 16, SPAN, 17], fill=INK)
    d.text((centred_x(TAGLINE, F_TAGLINE), 22), TAGLINE,
           font=F_TAGLINE, fill=RED)
    d.text((centred_x(MASTHEAD, F_MASTHEAD), 40), MASTHEAD,
           font=F_MASTHEAD, fill=INK)
    d.rectangle([EDGE, 115, SPAN, 118], fill=INK)
    d.rectangle([EDGE, 122, SPAN, 122], fill=INK)
    d.text((EDGE, 128), DATELINE_LEFT, font=F_DATELINE, fill=INK)
    d.text((centred_x(DATELINE_MID, F_DATELINE_R), 128), DATELINE_MID,
           font=F_DATELINE_R, fill=FAINT)
    d.text((SPAN - text_width(DATELINE_RIGHT, F_DATELINE_R), 128),
           DATELINE_RIGHT, font=F_DATELINE_R, fill=INK)
    d.rectangle([EDGE, 150, SPAN, 150], fill=INK)


def draw_diagram(d):
    """Radar/sector diagram inside the lead box: three range arcs over a
    baseline, a signal beam, a small tower, and a plane glyph."""
    cx, cy = 130, 252
    d.rectangle([50, 251, 210, 253], fill=INK)                    # baseline
    for radius in (78, 56, 34):                                   # range arcs
        d.arc([cx - radius, cy - radius, cx + radius, cy + radius],
              180, 360, fill=INK, width=3)
    d.line([(78, 200), (130, 252)], fill=RED, width=5)            # beam
    for tx in (60, 82, 104, 126, 148, 170, 192):                  # scale ticks
        d.rectangle([tx, 252, tx + 1, 258], fill=FAINT)
    d.rectangle([118, 240, 142, 252], outline=INK, width=3)       # tower block
    d.rectangle([129, 230, 131, 242], fill=INK)                   # antenna
    # plane glyph
    d.line([(198, 178), (193, 188)], fill=RED, width=3)
    d.line([(193, 181), (193, 187)], fill=RED, width=1)
    d.line([(183, 191), (191, 191)], fill=RED, width=1)
    d.rectangle([191, 179, 192, 188], fill=INK)
    d.line([(183, 181), (192, 190)], fill=INK, width=2)
    d.line([(199, 183), (192, 190)], fill=INK, width=2)
    d.polygon([(181, 189), (194, 189), (203, 190),
               (203, 191), (192, 191), (181, 190)], fill=INK)


def draw_lead(d):
    d.rectangle([30, 160, 994, 274], fill=LEADBG)
    d.rectangle([EDGE, 158, SPAN, 159], fill=INK)
    d.rectangle([EDGE, 275, SPAN, 276], fill=INK)
    d.rectangle([EDGE, 158, EDGE + 1, 276], fill=INK)
    d.rectangle([SPAN - 1, 158, SPAN, 276], fill=INK)
    draw_diagram(d)
    d.text((236, 168), LEAD_HEADLINE, font=F_LEAD_HEAD, fill=RED)
    y = 204
    for line in wrap(LEAD_TEXT, F_LEAD_BODY, 758):
        d.text((236, y), line, font=F_LEAD_BODY, fill=INK)
        y += 18


def draw_story(d, x, pen, headline, body, width):
    """Draw one story at the pen position; return the advanced pen."""
    d.text((x, pen), headline, font=F_HEADLINE, fill=INK)
    lines = wrap(body, F_BODY, width) if body else []
    for i, line in enumerate(lines):
        d.text((x, pen + 13 + i * 11.5), line, font=F_BODY, fill=BODY)
    return pen + 13 + max(0, len(lines) - 1) * 11.5 + 16.5


def draw_section(d, x, bar_y, pen, section, width):
    """Draw a section bar plus its stories; return (next bar y, next pen)."""
    label, stories = section
    d.rectangle([x, bar_y, x + width, bar_y + BARH - 1], fill=INK)
    d.text((x + 6, pen - 20.5), label, font=F_BAR, fill=PAPER)
    for headline, body in stories:
        pen = draw_story(d, x, pen, headline, body, width)
    import math
    return math.ceil(pen + 3.5), pen + 27.0


def draw_column(d, x, sections):
    bar_y, pen = 292, 315.0
    for section in sections:
        bar_y, pen = draw_section(d, x, bar_y, pen, section, COLW)
        # draw_section returns the following section's start pen as its
        # second value only when another section follows; recompute start:
        pen = pen  # start pen for the next section (bar_y already advanced)


HAIRLINE = (190, 180, 158)


def draw_hairlines(d):
    """Pale vertical rules in the two column gutters, behind the stories."""
    for gx in (348, 676):
        d.line([(gx, 292), (gx, 852)], fill=HAIRLINE)


def draw_bottom(d):
    for x, section in ((EDGE, MEAST_MORE), (520, TECH_MORE)):
        bar_y, pen = 740, 763.5
        label, stories = section
        d.rectangle([x, bar_y, x + 476, bar_y + BARH - 1], fill=INK)
        d.text((x + 6, pen - 20.5), label, font=F_BAR, fill=PAPER)
        for headline, body in stories:
            pen = draw_story(d, x, pen, headline, body, 476)


def draw_date_check(d):
    d.rectangle([30, 868, 994, 960], fill=DCBG)
    d.rectangle([EDGE, 866, SPAN, 962], outline=RED, width=2)
    d.text((40, 874), DC_TITLE, font=F_DC_TITLE, fill=RED)
    for i, item in enumerate(DC_LEFT):
        d.text((40, 898 + i * 15), "x  " + item, font=F_DC_ITEM, fill=INK)
    for i, item in enumerate(DC_RIGHT):
        d.text((516, 898 + i * 15), "x  " + item, font=F_DC_ITEM, fill=INK)


def draw_footer(d):
    d.rectangle([EDGE, 972, SPAN, 973], fill=INK)
    d.text((centred_x(FOOTER, F_FOOTER), 979), FOOTER,
           font=F_FOOTER, fill=FAINT)


def render():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(page)
    draw_header(d)
    draw_lead(d)
    draw_hairlines(d)
    draw_column(d, COLX[0], [ASIA, SPORT])
    draw_column(d, COLX[1], [EUROPE, WAR, TECH])
    draw_column(d, COLX[2], [AMERICAS, MEAST])
    draw_bottom(d)
    draw_date_check(d)
    draw_footer(d)
    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or SCRIPT_DIR
    os.makedirs(out_dir, exist_ok=True)
    render().save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
