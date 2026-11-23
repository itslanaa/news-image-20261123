#!/usr/bin/env python3
"""Draw the news-image-20261123 front page: 'Monday 23 November 2026'.

One 1024x1024 PNG, drawn entirely in code with PIL. No photos, no downloads,
no copied artwork. Every story was verified against live sources on 23 Nov 2026
(see the research notes in the repo README).

Structure (33 stories: 3 drawn leads + 10 drawn mid cards + 20 numbered briefs):
  regions EUROPE 14 / MIDDLE EAST 6 / AMERICAS 5 / ASIA 3 / GLOBAL 3 / AFRICA 2
  -- sums to exactly 33.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (178, 39, 30)
DARKRED = (140, 28, 22)
BLUE = (31, 78, 121)
GOLD = (176, 132, 30)
GREY = (92, 92, 88)
LIGHT = (186, 176, 154)
MAP_OCEAN = (213, 228, 236)
MAP_LAND = (233, 221, 193)
MAP_EDGE = (148, 133, 102)
CARD_BG = (252, 250, 244)

FDIR = "/usr/share/fonts/truetype/noto"
SERIF = os.path.join(FDIR, "NotoSerif-Regular.ttf")
SERIF_B = os.path.join(FDIR, "NotoSerif-Bold.ttf")
SERIF_I = os.path.join(FDIR, "NotoSerif-Italic.ttf")
SANS = os.path.join(FDIR, "NotoSans-Regular.ttf")
SANS_B = os.path.join(FDIR, "NotoSans-Bold.ttf")
SANS_I = os.path.join(FDIR, "NotoSans-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def para(draw, x, y, text, fnt, max_w, lh, fill=INK):
    """Draw a wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label, fill=RED):
    """Small [REPORTED]-style tag; returns the width it took."""
    f = font(SANS_B, 8)
    t = "[" + label + "]"
    w = draw.textlength(t, font=f)
    draw.text((x, y), t, font=f, fill=fill)
    return w


# ---------------------------------------------------------------- continents
# Stylised equirectangular polygons (lon, lat), drawn in code. Simplified
# shapes: the map only has to read as a world map with pins on it.
NORTH_AMERICA = [(-168, 66), (-140, 60), (-125, 49), (-120, 34), (-110, 24),
                 (-97, 16), (-83, 9), (-77, 8), (-83, 11), (-90, 21),
                 (-97, 26), (-89, 30), (-81, 26), (-76, 35), (-70, 42),
                 (-65, 44), (-55, 52), (-65, 60), (-85, 66), (-110, 68),
                 (-140, 70), (-168, 66)]
GREENLAND = [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70),
             (-25, 76), (-40, 76), (-55, 74), (-58, 70)]
SOUTH_AMERICA = [(-80, 9), (-70, 12), (-55, 6), (-50, 0), (-35, -8),
                 (-40, -22), (-55, -35), (-68, -52), (-73, -45), (-72, -25),
                 (-75, -15), (-80, -5), (-80, 9)]
EUROPE = [(-10, 36), (-9, 43), (-4, 48), (0, 51), (7, 54), (10, 59),
          (18, 56), (24, 58), (30, 62), (20, 70), (12, 66), (5, 58),
          (-4, 54), (-9, 43), (-10, 36)]
AFRICA = [(-6, 35), (10, 37), (30, 31), (35, 28), (43, 11), (51, 10),
          (42, 0), (39, -12), (33, -26), (20, -35), (12, -18), (9, 4),
          (-8, 4), (-17, 15), (-10, 30), (-6, 35)]
ASIA = [(28, 36), (30, 45), (40, 44), (48, 37), (58, 39), (68, 39),
        (76, 44), (85, 46), (95, 49), (105, 52), (120, 56), (135, 59),
        (145, 62), (158, 58), (162, 66), (152, 70), (136, 66), (124, 58),
        (112, 53), (100, 48), (88, 45), (76, 42), (64, 39), (52, 36),
        (40, 36), (28, 36)]
ASIA_S = [(35, 36), (39, 31), (47, 29), (57, 26), (66, 25), (72, 20),
          (77, 8), (82, 15), (88, 22), (93, 17), (98, 10), (103, 2),
          (108, 11), (111, 21), (118, 24), (121, 36), (127, 38), (133, 43),
          (140, 46), (141, 53), (137, 43), (130, 36), (124, 32), (118, 25),
          (109, 18), (103, 3), (97, 10), (91, 22), (85, 19), (80, 12),
          (74, 17), (67, 25), (57, 26), (49, 30), (41, 31), (35, 36)]
AUSTRALIA = [(113, -22), (115, -35), (124, -33), (132, -32), (140, -38),
             (150, -37), (153, -27), (146, -19), (142, -11), (135, -15),
             (126, -14), (118, -20), (113, -22)]
JAPAN = [(130, 31), (135, 34), (139, 37), (141, 42), (143, 44),
         (139, 42), (133, 35), (130, 33)]
INDONESIA = [(95, 5), (101, 0), (107, -6), (113, -7), (119, -8),
             (125, -9), (131, -3), (137, -2), (141, -5), (135, -8),
             (124, -9), (114, -8), (105, -5), (98, 2), (95, 5)]
NEW_ZEALAND = [(167, -45), (173, -41), (175, -38), (178, -37), (174, -41),
               (169, -46), (167, -45)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53),
      (1, 51), (-3, 50), (-5, 50)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, AFRICA,
              ASIA, ASIA_S, AUSTRALIA, JAPAN, INDONESIA, NEW_ZEALAND, UK]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---------------------------------------------------------------- masthead
    f_kick = font(SANS_B, 12)
    center(d, W // 2, 14, "THE WORLD IN ONE DAY  ·  33 STORIES  ·  SIX REGIONS  ·  ALL FROM ONE DAY",
           f_kick, fill=GREY)
    f_mast = font(SERIF_B, 47)
    center(d, W // 2, 32, "Monday 23 November 2026", f_mast)
    f_stand = font(SERIF_I, 15)
    center(d, W // 2, 88,
           "Iran hits US bases in Bahrain  ·  COP31 collapses with no deal  ·  Russia's 153-drone night over Ukraine",
           f_stand, fill=RED)
    d.line([(14, 110), (W - 14, 110)], fill=INK, width=2)

    # ------------------------------------------------------------ number strip
    nums = [
        ("153", "DRONES IN ONE NIGHT"),
        ("258", "HOUSE SEATS FOR THE DEMOCRATS"),
        ("25", "TANKERS ATTACKED IN A WEEK"),
        ("11", "KILLED IN DYMER, NEAR KYIV"),
        ("99%", "OF GAZA CONTAMINATED"),
        ("429", "FLIGHTS CANCELLED IN BELGIUM"),
    ]
    f_num = font(SERIF_B, 24)
    f_numlab = font(SANS_B, 8)
    bw, gap, y0 = 161, 6, 116
    for i, (n, lab) in enumerate(nums):
        x = 14 + i * (bw + gap)
        d.rectangle([x, y0, x + bw, y0 + 46], outline=LIGHT, width=1)
        center(d, x + bw // 2, y0 + 3, n, f_num)
        ly = y0 + 30
        for line in wrap(d, lab, f_numlab, bw - 10):
            center(d, x + bw // 2, ly, line, f_numlab, fill=GREY)
            ly += 9

    # ------------------------------------------------------------ region strip
    f_reg = font(SANS_B, 12)
    center(d, W // 2, 168,
           "EUROPE 14  ·  MIDDLE EAST 6  ·  AMERICAS 5  ·  ASIA 3  ·  GLOBAL 3  ·  AFRICA 2      —  33 STORIES IN ALL",
           f_reg)
    d.line([(14, 190), (W - 14, 190)], fill=INK, width=1)

    # ------------------------------------------------------------------- leads
    leads = [
        dict(kick="1 · BAHRAIN — WAR AT SEA",
             head="Iran hits US bases in Bahrain as tankers burn in Hormuz",
             deck="Tehran claims two Patriot radars hit at al-Riffa and Awali; Bahrain counts "
                  "two hurt at a torched industrial site; 25 tankers attacked in a week.",
             art="iran", tag="REPORTED"),
        dict(kick="2 · ANTALYA — COP31",
             head="COP31 collapses — no deal as the longest talks ever end",
             deck="Delegates reject the Antalya Pact on Sunday; fossil fuels stripped from "
                  "every draft; the first COP collapse since Copenhagen 2009.",
             art="cop", tag="CONFIRMED"),
        dict(kick="3 · UKRAINE — OVERNIGHT ASSAULT",
             head="Russia's 153-drone night kills 11 in Dymer",
             deck="A five-storey block collapses near Kyiv; 14 still missing as rescuers dig. "
                  "134 of 153 drones downed by 08:00; a kindergarten hit in Kharkiv.",
             art="ukraine", tag="REPORTED"),
    ]
    f_kick2 = font(SANS_B, 11)
    f_head = font(SERIF_B, 17)
    f_deck = font(SANS, 11)
    lw, lgap, ly0 = 324, 12, 198
    for i, L in enumerate(leads):
        x = 14 + i * (lw + lgap)
        d.rectangle([x, ly0, x + lw, ly0 + 15], fill=RED)
        d.text((x + 6, ly0 + 2), L["kick"], font=f_kick2, fill=(255, 255, 255))
        art_y = ly0 + 22
        if L["art"] == "iran":
            draw_iran(d, x, art_y, lw, 92)
        elif L["art"] == "cop":
            draw_cop(d, x, art_y, lw, 92)
        else:
            draw_ukraine(d, x, art_y, lw, 92)
        hy = art_y + 98
        hy = para(d, x + 2, hy, L["head"], f_head, lw - 4, 21)
        hy = para(d, x + 2, hy + 3, L["deck"], f_deck, lw - 4, 14, fill=(40, 40, 40))
        tag(d, x + 2, hy + 2, L["tag"])
        d.rectangle([x, ly0, x + lw, ly0 + 222], outline=LIGHT, width=1)

    # --------------------------------------------------------------- mid cards
    mids = [
        ("BENGHAZI · SEA DRONES", "Ukraine's sea drones sink a Russian warship off Libya",
         "Corvette Mercury sinks; a cargo ship is hit too. Zelenskyy confirms it.", "warship", "REPORTED"),
        ("WASHINGTON · VOTE", "Democrats take 258 House seats — biggest majority since 1992",
         "Hubbard beats Foxx by 330 votes; 44 seats gained; Senate 56–44.", "capitol", "CONFIRMED"),
        ("SEOUL · EXAM", "Korea's education minister quits over AI exam cheating",
         "Choi Kyo-jin resigns Sunday; 550,000 sat the exam; a top scorer used AI.", "exam", "CONFIRMED"),
        ("BRUSSELS · STRIKE", "Belgium stops: national strike grounds the country",
         "Airspace shut 07:00–21:00; 429 flights hit; unions fight €10bn cuts.", "plane", "CONFIRMED"),
        ("GAZA · WEST BANK", "Three killed in Gaza food-truck strike",
         "WCK: the truck was not ours. Eisenkot calls settler arson 'Jewish terrorism'.", "truck", "REPORTED"),
        ("DHAKA · RETURN", "Bangladesh: Hasina will be jailed if she returns",
         "Ex-PM faces a death sentence; her party is banned; blasts in 28 districts.", "jail", "CONFIRMED"),
        ("SINALOA · CAPTURE", "'Chapo Isidro' captured in Mexico",
         "FBI top-10 fugitive taken Friday night; four soldiers killed in the raid.", "cuffs", "CONFIRMED"),
        ("BELGRADE · FLOOD", "Belgrade floods after a month's rain in a day",
         "52 litres per square metre; streets under water, drivers pulled from cars.", "flood", "CONFIRMED"),
        ("COPENHAGEN · PLOT", "Denmark expels Russian attaché over rapper murder plot",
         "Rapper Kyivstoner targeted; two charged. Poland reveals an August attempt.", "mic", "REPORTED"),
        ("BARRANQUILLA · SPORT", "Paredes collapses live on TV after Boca's title",
         "Boca beat Atlético Mineiro 2–0; 32°C heat; 'just dizziness', he says.", "football", "CONFIRMED"),
    ]
    f_mkick = font(SANS_B, 9)
    f_mhead = font(SANS_B, 11)
    f_mdeck = font(SANS, 9)
    cw, cgap = 192, 9
    for r in range(2):
        for c in range(5):
            i = r * 5 + c
            kick, head, deck, art, tg = mids[i]
            x = 14 + c * (cw + cgap)
            y = 428 + r * 108
            d.rectangle([x, y, x + cw, y + 104], outline=LIGHT, width=1, fill=CARD_BG)
            draw_icon(d, art, x, y + 4, cw, 32)
            d.text((x + 6, y + 38), kick, font=f_mkick, fill=RED)
            tag(d, x + cw - 6 - text_w(d, "[" + tg + "]", font(SANS_B, 8)), y + 38, tg)
            hy = para(d, x + 6, y + 50, head, f_mhead, cw - 12, 13)
            para(d, x + 6, hy + 1, deck, f_mdeck, cw - 12, 11, fill=(55, 55, 55))

    # ------------------------------------------------------------ timeline strip
    f_tl = font(SANS, 10)
    f_tlb = font(SANS_B, 10)
    d.text((14, 648), "THE DAY IN UTC", font=f_tlb, fill=RED)
    tl = ("SUN 18:00 — 153 drones launched  ·  MON 07:00 — Belgian airspace shuts  ·  "
          "MON 08:00 — 134 of 153 downed  ·  MONDAY — NATO meets on Poland  ·  "
          "SUNDAY — COP31 pact rejected")
    d.text((128, 648), tl, font=f_tl, fill=INK)
    d.line([(14, 668), (W - 14, 668)], fill=LIGHT, width=1)

    # ------------------------------------------------------- map + also-on list
    f_sect = font(SANS_B, 12)
    d.text((16, 676), "WHERE IT HAPPENED", font=f_sect, fill=INK)
    d.text((16, 692), "Numbered pins: the 13 drawn stories  ·  dots: briefs 14–33",
           font=font(SANS_I, 9), fill=GREY)
    draw_map(d, 18, 708, 326, 196)

    briefs = [
        ("KRYVYI RIH", "A child and a young paramedic killed in a strike; 25 apartment blocks, a hospital and schools damaged."),
        ("BRUSSELS", "NATO meets in emergency session after three Russian missiles land in Poland; Rutte: 'every inch' defended."),
        ("ROSTOV", "Ukrainian drones hit oil sites in Rostov and Tatarstan, 1,500 km from the front."),
        ("GAZA", "Oxfam: the war left toxic contamination across 99% of Gaza."),
        ("INDONESIA", "Candy factory fire: 3 dead, 37 missing; DNA needed to name the victims."),
        ("RICHMOND", "Oregon and Virginia sue SpaceX over Grok's sexual deepfakes; 20,000+ images of children cited."),
        ("MENLO PARK", "Meta's AI chief: superintelligence is arriving — and control is at risk."),
        ("ODESA", "Odesa schools go remote for the week as strikes cut power, heat and water."),
        ("GAZA CITY", "Two more Palestinians killed in Gaza on Sunday; a drone strike near Deir al-Balah kills one."),
        ("MANAMA", "US official: no damage to US personnel or facilities in Bahrain."),
        ("ANTALYA", "COP31's one win: 90+ countries sign an electrification pledge."),
        ("HORMUZ", "Shipping through the strait falls 15% in a week; 37 tankers pass, down from 52."),
        ("RYLSK", "Ukraine hits Russia's Rubicon drone unit; an ammunition depot blows up."),
        ("BALTIC", "Russian cargo ship Sparta II burns in the Gulf of Finland after a drone strike."),
        ("WASHINGTON", "Putin 'privately agreed' to NATO-style guarantees for Ukraine, the Washington Post reports. [REPORTED]"),
        ("DAKAR", "CAS to rule Tuesday on Senegal's AFCON title appeal. [FORECAST]"),
        ("KYIV", "Drone debris falls on a warehouse and two school grounds; no casualties."),
        ("CHERKASY", "Nine Russian drones downed over Cherkasy; no injuries reported."),
        ("LYUBOTYN", "A Russian drone hits a railway station; train cars catch fire."),
        ("BELGRADE", "Serbia's weather chief arrested for alleged money-laundering as the floods hit."),
    ]
    f_also = font(SANS_B, 12)
    f_br = font(SANS, 9)
    f_brb = font(SANS_B, 9)
    d.text((360, 676), "ALSO ON MONDAY 23 NOVEMBER", font=f_also, fill=INK)
    col_x = [360, 688]
    col_w = 316
    for col in range(2):
        y = 696
        for j in range(10):
            i = col * 10 + j
            place, txt = briefs[i]
            num = str(14 + i) + ". "
            d.text((col_x[col], y), num, font=f_brb, fill=RED)
            nx = col_x[col] + text_w(d, num, f_brb)
            d.text((nx, y), place, font=f_brb, fill=INK)
            px = nx + text_w(d, place, f_brb)
            rest = " — " + txt
            lines = wrap(d, rest, f_br, col_w - (px - col_x[col]))
            d.text((px, y), lines[0].lstrip(), font=f_br, fill=INK)
            yy = y + 11
            for extra in lines[1:]:
                d.text((col_x[col], yy), extra, font=f_br, fill=INK)
                yy += 11
            y = yy + 1

    # ------------------------------------------------------------ date check
    d.rectangle([14, 912, W - 14, 968], outline=RED, width=1, fill=(250, 238, 235))
    f_dc = font(SANS_B, 10)
    f_dct = font(SANS, 10)
    d.text((22, 918), "DATE CHECK", font=f_dc, fill=RED)
    d.line([(100, 927), (104, 931), (112, 921)], fill=RED, width=2)
    d.text((118, 918), "Every story on this page happened, or was first reported, on Monday 23 November 2026.",
           font=f_dct, fill=INK)
    para(d, 22, 934,
         "Weekend events appear only where Monday moved them on: the Bahrain strikes (Sat), COP31's collapse (Sun), "
         "the Gaza truck (Sat), the 258th House seat (Sun), Korea's minister (Sun).",
         f_dct, W - 44, 13)
    d.text((22, 952), "LEFT OUT AS OTHER DAYS' NEWS — 19 NOV: the World Court's Myanmar ruling · 20 NOV: COP31's scheduled close.",
           font=f_dct, fill=INK)

    # ------------------------------------------------------------- source line
    f_src = font(SANS, 9)
    center(d, W // 2, 976,
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, Yonhap, ABS, ICJ.  Pictures and map: original, drawn in code.",
           f_src, fill=GREY)
    center(d, W // 2, 990,
           "Confidence: CONFIRMED = two or more outlets  ·  REPORTED = named sources, one side's claim where stated  ·  FORECAST = due date or draft.",
           f_src, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


# ------------------------------------------------------------------ lead art
def draw_iran(d, x, y, w, h):
    """War at sea: grey warship left, tanker burning right, waves below."""
    # sky drone
    dx, dy = x + w - 40, y + 6
    d.line([(dx - 12, dy), (dx + 12, dy)], fill=INK, width=2)
    d.line([(dx, dy - 3), (dx, dy + 3)], fill=INK, width=2)
    d.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=INK)
    # warship (left)
    sx, sy = x + 16, y + 44
    d.polygon([(sx, sy), (sx + 110, sy), (sx + 96, sy + 18), (sx + 8, sy + 18)],
              fill=(90, 100, 110), outline=INK)
    d.rectangle([sx + 30, sy - 16, sx + 66, sy], fill=(110, 120, 130), outline=INK)
    d.line([(sx + 48, sy - 16), (sx + 48, sy - 30)], fill=INK, width=2)
    d.rectangle([sx + 48, sy - 30, sx + 62, sy - 22], fill=RED)
    for wx in range(sx + 14, sx + 104, 14):
        d.rectangle([wx, sy + 4, wx + 6, sy + 9], fill=(220, 225, 230))
    # tanker (right) with fire
    tx, ty = x + w - 140, y + 52
    d.polygon([(tx, ty), (tx + 124, ty), (tx + 116, ty + 14), (tx + 8, ty + 14)],
              fill=(150, 60, 40), outline=INK)
    d.rectangle([tx + 88, ty - 12, tx + 112, ty], fill=(180, 80, 50), outline=INK)
    d.ellipse([tx + 22, ty - 26, tx + 46, ty - 2], fill=(255, 140, 0))
    d.ellipse([tx + 30, ty - 34, tx + 52, ty - 12], fill=(255, 200, 40))
    d.ellipse([tx + 40, ty - 20, tx + 58, ty - 4], fill=(255, 90, 0))
    for k, (ox, oy, r) in enumerate([(tx + 30, ty - 40, 7), (tx + 48, ty - 44, 9),
                                     (tx + 64, ty - 38, 6)]):
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(90, 90, 90))
    # waves
    for wy in (y + h - 18, y + h - 10):
        for wx in range(x + 8, x + w - 8, 24):
            d.arc([wx, wy - 4, wx + 22, wy + 6], 180, 360, fill=BLUE, width=2)


def draw_cop(d, x, y, w, h):
    """Globe + struck FOSSIL FUELS + red NO DEAL stamp + thermometer."""
    # globe
    gx, gy, gr = x + 34, y + 46, 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(90, 140, 190),
              outline=INK, width=2)
    d.ellipse([gx - 18, gy - 22, gx - 2, gy - 6], fill=(80, 160, 90))
    d.ellipse([gx - 6, gy + 4, gx + 16, gy + 22], fill=(80, 160, 90))
    d.ellipse([gx + 8, gy - 20, gx + 22, gy - 2], fill=(80, 160, 90))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 300, 60, fill=(255, 255, 255), width=2)
    # struck FOSSIL FUELS
    f_big = font(SANS_B, 17)
    t = "FOSSIL FUELS"
    tw = d.textlength(t, font=f_big)
    tx = x + w - tw - 14
    d.text((tx, y + 4), t, font=f_big, fill=INK)
    d.line([(tx - 4, y + 28), (tx + tw + 4, y + 6)], fill=RED, width=4)
    # NO DEAL stamp
    f_st = font(SANS_B, 19)
    st = "NO DEAL"
    sw = d.textlength(st, font=f_st)
    sx, sy = x + w // 2 - sw // 2 + 18, y + 38
    d.rectangle([sx, sy, sx + sw + 16, sy + 27], outline=RED, width=3)
    d.text((sx + 8, sy + 3), st, font=f_st, fill=RED)
    # thermometer
    tx2, ty2 = x + w - 30, y + 34
    d.rounded_rectangle([tx2, ty2, tx2 + 10, ty2 + 30], radius=5, outline=INK, width=2,
                        fill=(255, 255, 255))
    d.ellipse([tx2 - 4, ty2 + 26, tx2 + 14, ty2 + 42], outline=INK, width=2, fill=RED)
    d.rectangle([tx2 + 3, ty2 + 16, tx2 + 7, ty2 + 30], fill=RED)
    f_sm = font(SANS_B, 8)
    d.text((tx2 - 22, ty2 + 6), "1.5°C", font=f_sm, fill=RED)
    f_lab = font(SANS_B, 8)
    center(d, x + w // 2 + 20, y + 72, "ANTALYA PACT REJECTED", f_lab, fill=GREY)


def draw_ukraine(d, x, y, w, h):
    """Five-storey block, one corner collapsed, drones above, 11 KILLED badge."""
    # drones
    for dx, dy in [(x + 40, y + 8), (x + w - 60, y + 4), (x + w // 2 + 30, y + 14)]:
        d.line([(dx - 10, dy), (dx + 10, dy)], fill=INK, width=2)
        d.line([(dx, dy - 3), (dx, dy + 3)], fill=INK, width=2)
        d.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=INK)
    # block
    bx, by, bw, bh = x + 52, y + 26, 150, 56
    d.rectangle([bx, by, bx + bw, by + bh], fill=(200, 190, 170), outline=INK, width=2)
    for r in range(4):
        for c in range(6):
            wx, wy = bx + 8 + c * 24, by + 6 + r * 13
            d.rectangle([wx, wy, wx + 12, wy + 8], fill=(60, 70, 90))
    # collapsed corner (right side)
    d.polygon([(bx + bw, by), (bx + bw, by + bh), (bx + bw - 34, by + bh),
               (bx + bw - 18, by + 30), (bx + bw - 30, by + 12)],
              fill=(150, 140, 120), outline=INK)
    d.polygon([(bx + bw - 34, by + bh), (bx + bw, by + bh), (bx + bw + 18, by + bh + 8),
               (bx + bw - 20, by + bh + 8)], fill=(120, 110, 95), outline=INK)
    # smoke
    for ox, oy, r in [(bx + bw - 8, by - 6, 6), (bx + bw - 22, by - 12, 8),
                      (bx + bw - 2, by - 14, 5)]:
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(120, 120, 120))
    # 11 KILLED badge
    f_b = font(SANS_B, 12)
    t = "11 KILLED"
    tw = d.textlength(t, font=f_b)
    bx2, by2 = x + 14, y + h - 24
    d.rectangle([bx2, by2, bx2 + tw + 12, by2 + 18], fill=RED)
    d.text((bx2 + 6, by2 + 3), t, font=f_b, fill=(255, 255, 255))


# ------------------------------------------------------------------ mid icons
def draw_icon(d, kind, x, y, w, h):
    """Small flat pictogram for a mid card; box is (x, y, x+w, y+h)."""
    cx = x + w // 2
    cy = y + h // 2
    if kind == "warship":
        # sinking warship, tilted hull + smoke
        d.polygon([(x + 40, y + 18), (x + 150, y + 6), (x + 158, y + 16),
                   (x + 48, y + 26)], fill=(90, 100, 110), outline=INK)
        d.rectangle([x + 86, y + 2, x + 108, y + 10], fill=(110, 120, 130),
                    outline=INK)
        for ox, oy, r in [(x + 150, y + 2, 6), (x + 162, y + 6, 8)]:
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(90, 90, 90))
        for wy in (y + h - 8, y + h - 3):
            for wx in range(x + 20, x + w - 20, 22):
                d.arc([wx, wy - 3, wx + 20, wy + 5], 180, 360, fill=BLUE, width=2)
    elif kind == "capitol":
        # Capitol dome + 258 badge
        d.polygon([(cx - 26, y + 10), (cx + 26, y + 10), (cx, y - 2)],
                  fill=(210, 198, 168), outline=INK)
        d.rectangle([cx - 30, y + 10, cx + 30, y + 14], fill=(180, 168, 140),
                    outline=INK)
        for px in (cx - 24, cx - 8, cx + 8, cx + 20):
            d.rectangle([px, y + 14, px + 5, y + h - 2], fill=(240, 234, 220),
                        outline=INK)
        f = font(SANS_B, 12)
        t = "258"
        d.text((x + w - 44, y + 2), t, font=f, fill=RED)
    elif kind == "exam":
        # exam paper + pencil + AI stamp
        d.rectangle([cx - 22, y + 2, cx + 14, y + h - 2], fill=(255, 255, 255),
                    outline=INK)
        for ly in (y + 8, y + 14, y + 20):
            d.line([(cx - 18, ly), (cx + 10, ly)], fill=GREY, width=1)
        d.line([(cx + 22, y + 26), (cx + 34, y + 6)], fill=(230, 180, 40), width=4)
        d.polygon([(cx + 34, y + 6), (cx + 38, y + 12), (cx + 30, y + 12)], fill=INK)
        f = font(SANS_B, 11)
        d.text((x + w - 46, y + 14), "AI", font=f, fill=RED)
    elif kind == "plane":
        # grounded plane, nose down + picket sign
        d.polygon([(x + 30, y + 14), (x + 130, y + 6), (x + 150, y + 12),
                   (x + 130, y + 18), (x + 40, y + 24)], fill=(70, 90, 120))
        d.polygon([(x + 80, y + 6), (x + 96, y + 6), (x + 88, y + 16)], fill=(70, 90, 120))
        d.line([(x + 150, y + 12), (x + 168, y + 8)], fill=RED, width=3)
        d.rectangle([x + 8, y + 4, x + 26, y + 16], fill=RED)
        d.line([(x + 17, y + 16), (x + 17, y + h)], fill=INK, width=2)
    elif kind == "truck":
        # delivery truck + flame
        d.rectangle([x + 24, y + 10, x + 110, y + h - 8], fill=(200, 200, 190),
                    outline=INK)
        d.rectangle([x + 110, y + 16, x + 142, y + h - 8], fill=(150, 170, 200),
                    outline=INK)
        d.ellipse([x + 40, y + h - 10, x + 54, y + h + 4], fill=INK)
        d.ellipse([x + 118, y + h - 10, x + 132, y + h + 4], fill=INK)
        d.ellipse([x + 148, y + 2, x + 162, y + 16], fill=(255, 140, 0))
        d.ellipse([x + 153, y + 6, x + 167, y + 20], fill=(255, 200, 40))
    elif kind == "jail":
        # prison bars + gavel
        for bx in range(x + 30, x + 120, 16):
            d.line([(bx, y + 2), (bx, y + h - 2)], fill=INK, width=4)
        d.line([(x + 30, y + 2), (x + 116, y + 2)], fill=INK, width=3)
        d.line([(x + 30, y + h - 2), (x + 116, y + h - 2)], fill=INK, width=3)
        d.line([(x + 150, y + 22), (x + 172, y + 4)], fill=(90, 58, 28), width=5)
        d.rectangle([x + 142, y + 2, x + 154, y + 12], fill=(122, 82, 52))
    elif kind == "cuffs":
        # handcuffs
        d.ellipse([cx - 34, cy - 10, cx - 6, cy + 12], outline=INK, width=4)
        d.ellipse([cx + 6, cy - 10, cx + 34, cy + 12], outline=INK, width=4)
        d.line([(cx - 6, cy + 1), (cx + 6, cy + 1)], fill=INK, width=3)
        d.line([(cx - 20, cy - 10), (cx - 14, cy - 18)], fill=INK, width=2)
        d.line([(cx + 14, cy - 10), (cx + 20, cy - 18)], fill=INK, width=2)
        f = font(SANS_B, 9)
        d.text((x + 8, y + 2), "FBI TOP 10", font=f, fill=RED)
    elif kind == "flood":
        # flooded street: rain + water + car roof
        for rx in range(x + 10, x + w - 10, 18):
            d.line([(rx, y + 2), (rx - 4, y + 10)], fill=BLUE, width=2)
        d.rectangle([x + 40, y + 18, x + 150, y + h - 6], fill=(70, 110, 150))
        for wy in (y + 22, y + 27):
            for wx in range(x + 44, x + 146, 20):
                d.arc([wx, wy - 3, wx + 18, wy + 4], 180, 360, fill=(220, 235, 245),
                      width=2)
        d.polygon([(cx - 26, y + 12), (cx + 26, y + 12), (cx + 18, y + 18),
                   (cx - 18, y + 18)], fill=(180, 40, 30))
    elif kind == "mic":
        # microphone + shield
        d.ellipse([cx - 12, y + 2, cx + 12, y + 22], fill=(60, 60, 70),
                  outline=INK)
        for gy in (y + 8, y + 14):
            d.line([(cx - 12, gy), (cx + 12, gy)], fill=(200, 200, 200), width=1)
        d.line([(cx, y + 22), (cx, y + 30)], fill=INK, width=3)
        d.arc([cx - 10, y + 18, cx + 10, y + 32], 0, 180, fill=INK, width=2)
        sx = x + w - 34
        d.polygon([(sx, y + 12), (sx + 22, y + 12), (sx + 22, y + 22),
                   (sx + 11, y + 30), (sx, y + 22)], fill=BLUE, outline=INK)
        d.line([(sx + 5, y + 19), (sx + 10, y + 24), (sx + 18, y + 15)],
               fill=(255, 255, 255), width=2)
    elif kind == "football":
        # football + TV camera
        d.ellipse([cx - 34, cy - 12, cx - 2, cy + 14], fill=(255, 255, 255),
                  outline=INK, width=2)
        d.polygon([(cx - 22, cy - 4), (cx - 16, cy - 10), (cx - 10, cy - 4),
                   (cx - 13, cy + 4), (cx - 21, cy + 3)], fill=INK)
        d.rectangle([cx + 12, y + 8, cx + 44, y + 24], fill=(40, 40, 50))
        d.polygon([(cx + 44, y + 12), (cx + 56, y + 16), (cx + 44, y + 20)],
                  fill=(40, 40, 50))
        d.line([(cx + 28, y + 24), (cx + 28, y + 30)], fill=INK, width=2)
        f = font(SANS_B, 9)
        d.text((x + 8, y + 2), "2–0", font=f, fill=RED)


def draw_map(d, x0, y0, w, h):
    """Equirectangular world map with numbered pins 1-13 and dots 14-33."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_OCEAN, outline=INK, width=1)
    lon0, lon1 = -180.0, 180.0
    lat0, lat1 = 80.0, -60.0

    def proj(lon, lat):
        px = x0 + 8 + (lon - lon0) / (lon1 - lon0) * (w - 16)
        py = y0 + 8 + (lat0 - lat) / (lat0 - lat1) * (h - 16)
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_EDGE)
    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        d.line([(px, y0), (px, y0 + h)], fill=(190, 205, 215), width=1)
    for lat in (60, 30, 0, -30):
        _, py = proj(0, lat)
        d.line([(x0, py), (x0 + w, py)], fill=(190, 205, 215), width=1)

    pins = {  # number: (lon, lat)
        1: (50.6, 26.2), 2: (30.7, 36.9), 3: (30.3, 50.8), 4: (20.1, 32.1),
        5: (-77.0, 38.9), 6: (127.0, 37.5), 7: (4.4, 50.8), 8: (34.5, 31.5),
        9: (90.4, 23.8), 10: (-107.4, 24.8), 11: (20.5, 44.8),
        12: (12.6, 55.7), 13: (-74.8, 11.0),
    }
    dots = {  # number: (lon, lat, dx, dy)
        14: (33.4, 47.9, 0, 0), 15: (4.4, 50.8, 9, -7), 16: (39.7, 47.2, 0, 0),
        17: (34.5, 31.5, 8, 7), 18: (106.8, -6.2, 0, 0), 19: (-77.4, 37.5, -8, 6),
        20: (-122.2, 37.5, 0, 0), 21: (30.7, 46.5, 0, 0), 22: (34.5, 31.5, -8, -7),
        23: (50.6, 26.2, 8, 7), 24: (30.7, 36.9, 9, 6), 25: (56.5, 26.6, 0, 0),
        26: (34.7, 51.6, 0, 0), 27: (24.0, 59.5, 0, 0), 28: (-77.0, 38.9, 9, -6),
        29: (-17.4, 14.7, 0, 0), 30: (30.5, 50.4, 8, 6), 31: (32.1, 49.4, 0, 0),
        32: (35.9, 49.9, 0, 0), 33: (20.5, 44.8, 9, 6),
    }
    f_pin = font(SANS_B, 9)
    for n, (lon, lat) in pins.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255),
                  width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 6), t, font=f_pin,
               fill=(255, 255, 255))
    for n, (lon, lat, dx, dy) in dots.items():
        px, py = proj(lon, lat)
        d.ellipse([px + dx - 2, py + dy - 2, px + dx + 2, py + dy + 2], fill=INK)


if __name__ == "__main__":
    main()
