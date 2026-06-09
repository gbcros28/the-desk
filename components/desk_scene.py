"""
Pixel art desk scene — SVG-based, scales to full container width.
All geometry drawn as SVG <rect> elements (true pixel art, no emoji).
"""
import streamlit as st
import gamification

# ── Theme palettes ─────────────────────────────────────────────────────────
PALETTES = {
    "default":         {"wall":  "#0d1420", "floor": "#171c27",
                        "desk":  "#1e2a3a", "desk_top": "#253346", "desk_edge": "#162030",
                        "screen": "#050e1a", "glow": "#4a8fe8",   "border": "#4a8fe8",
                        "win_sky": "#1a3a6e", "win_frame": "#253346",
                        "suit":  "#1e3a6e", "suit_hi": "#2a4e8a", "suit_sh": "#142a56",
                        "pants": "#152a50", "pants_sh": "#0e1e3a",
                        "shirt": "#e8eef8", "shirt_sh": "#c0cce0",
                        "tie":   "#c0392b", "tie_sh":   "#8a1a10",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#2d1b0e", "hair_hi":  "#4a2e1a",
                        "shoe":  "#141210", "belt": "#2a1a0a",
                        "shelf": "#1a2a3a", "book1": "#8a3020", "book2": "#20508a"},

    "bloomberg_theme": {"wall":  "#060400", "floor": "#120d00",
                        "desk":  "#1a1000", "desk_top": "#221500", "desk_edge": "#0e0900",
                        "screen": "#000000", "glow": "#e87d2a",   "border": "#e87d2a",
                        "win_sky": "#1a0e00", "win_frame": "#2a1800",
                        "suit":  "#1a0e00", "suit_hi": "#2a1800", "suit_sh": "#0e0800",
                        "pants": "#100a00", "pants_sh": "#080600",
                        "shirt": "#f0c080", "shirt_sh": "#c09040",
                        "tie":   "#e87d2a", "tie_sh":   "#a04010",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#2d1b0e", "hair_hi":  "#4a2e1a",
                        "shoe":  "#0a0800", "belt": "#180e00",
                        "shelf": "#1a1000", "book1": "#a04010", "book2": "#502000"},

    "stardew_theme":   {"wall":  "#141e0c", "floor": "#1e2e14",
                        "desk":  "#4a3520", "desk_top": "#5a4228", "desk_edge": "#362818",
                        "screen": "#0a1406", "glow": "#8ab44a",   "border": "#8ab44a",
                        "win_sky": "#2a5020", "win_frame": "#5a4228",
                        "suit":  "#2a4a20", "suit_hi": "#3a6a30", "suit_sh": "#1a3418",
                        "pants": "#1e3818", "pants_sh": "#142810",
                        "shirt": "#e8f0d0", "shirt_sh": "#b0c890",
                        "tie":   "#c8a428", "tie_sh":   "#907818",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#5a3010", "hair_hi":  "#7a4820",
                        "shoe":  "#1a1008", "belt": "#3a2010",
                        "shelf": "#4a3520", "book1": "#6a4a20", "book2": "#3a7a30"},

    "cherry_theme":    {"wall":  "#0e0610", "floor": "#1a0c18",
                        "desk":  "#2a1020", "desk_top": "#341428", "desk_edge": "#1c0a18",
                        "screen": "#0a0510", "glow": "#d4608a",   "border": "#d4608a",
                        "win_sky": "#2a0838", "win_frame": "#3a1040",
                        "suit":  "#2a1040", "suit_hi": "#3a1860", "suit_sh": "#1a0828",
                        "pants": "#1e0c30", "pants_sh": "#120820",
                        "shirt": "#f8e0ec", "shirt_sh": "#d0a8c0",
                        "tie":   "#d4608a", "tie_sh":   "#903050",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#2d1b0e", "hair_hi":  "#4a2e1a",
                        "shoe":  "#100810", "belt": "#200818",
                        "shelf": "#2a1020", "book1": "#883060", "book2": "#601888"},

    "midnight_theme":  {"wall":  "#06000e", "floor": "#100018",
                        "desk":  "#180828", "desk_top": "#200a34", "desk_edge": "#100620",
                        "screen": "#040008", "glow": "#00e5ff",   "border": "#7c4dff",
                        "win_sky": "#0a0028", "win_frame": "#200840",
                        "suit":  "#1a0840", "suit_hi": "#280c60", "suit_sh": "#100428",
                        "pants": "#12063a", "pants_sh": "#0a0428",
                        "shirt": "#d0c8f8", "shirt_sh": "#9888d0",
                        "tie":   "#7c4dff", "tie_sh":   "#4820c0",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#2d1b0e", "hair_hi":  "#4a2e1a",
                        "shoe":  "#0a0818", "belt": "#180830",
                        "shelf": "#180828", "book1": "#4820c0", "book2": "#008888"},

    "gold_theme":      {"wall":  "#080600", "floor": "#141000",
                        "desk":  "#2a1e08", "desk_top": "#342610", "desk_edge": "#1c1404",
                        "screen": "#060400", "glow": "#c8a428",   "border": "#c8a428",
                        "win_sky": "#1a1000", "win_frame": "#342610",
                        "suit":  "#1a1400", "suit_hi": "#2a2000", "suit_sh": "#0e0c00",
                        "pants": "#120e00", "pants_sh": "#0a0800",
                        "shirt": "#f0e8c0", "shirt_sh": "#c0b080",
                        "tie":   "#c8a428", "tie_sh":   "#907418",
                        "skin":  "#f5c2a0", "skin_sh":  "#c49070",
                        "hair":  "#2d1b0e", "hair_hi":  "#4a2e1a",
                        "shoe":  "#0e0c00", "belt": "#1a1400",
                        "shelf": "#2a1e08", "book1": "#907418", "book2": "#c8a428"},
}

# ── Pixel art grids (1 char = 1 pixel, '.' = transparent) ─────────────────
#
# Color key for characters:
#   H=hair  h=hair-hi  S=skin  s=skin-shadow  E=eyebrow  e=eye-white
#   D=eye-pupil  n=nose-shadow  M=lip  N=suit  r=suit-hi  R=suit-sh
#   W=shirt  w=shirt-sh  T=tie  t=tie-sh  G=pants  g=pants-sh
#   K=shoe  B=belt  P=pocket-sq
#
# ALL rows MUST be exactly 16 chars.

CHAR_BODY = [
    # 16 wide × 30 tall — detailed finance character
    "....HHHHHHHH....",  # 0  hair top
    "...HHHhHHhHHH...",  # 1  hair with highlights
    "..HHHhHHHHhHHH..",  # 2  hair wide
    "..HHHSSSSSSSSHh.",  # 3  forehead
    "..HHHSSSSSSSSSh.",  # 4  forehead
    "..HHHEESSSSEEsh.",  # 5  eyebrows (E=dark brow)
    "..HHHSeESSDeSSh.",  # 6  eyes (e=white, D=iris/pupil)
    "..HHHSSSSSSSSsh.",  # 7  mid face
    "..HHHSSSnSSSSsh.",  # 8  nose shadow (n)
    "...HHSSSSSSSssh.",  # 9  lower face
    "...HHSSSmMSSSsh.",  # 10 mouth (m=gap, M=bottom lip)
    "....SSSSSSSSsss.",  # 11 chin
    "....SSSSSSSSSS..",  # 12 neck
    "....SSSSTtTSSS..",  # 13 neck + tie start
    "..WwNNNtTTtNNWw.",  # 14 shirt collar + lapels
    ".NNNNrWwTTwWrNN.",  # 15 upper chest
    "NNNNNrWwTTwWrNNN",  # 16 suit chest  (16) ✓
    "NNNNPrNRTTRNrNNN",  # 17 pocket sq (P), shadow (R)
    "NNNNNrNRTTRNrNNN",  # 18 suit body
    "NNNNNrNRtTRNrNNN",  # 19 tie narrows
    "NNNNNrNNtTNNrNNN",  # 20 tie narrower
    "NNNNNrNNNTNNrNNN",  # 21 tie very narrow
    "NNNRNNNNNNNNNRnn",  # 22 suit hem / lower
    ".NBBBBBBBBBBBBn.",  # 23 belt (B)
    ".GGGGGGGGGGGGGg.",  # 24 pants
    ".GGGGGGGGGGGGGg.",  # 25 pants
    ".GGGGGGGGGGGGGg.",  # 26 pants
    ".GGGGGg..GGGGg..",  # 27 legs split
    ".GGGGGg..GGGGg..",  # 28 legs
    ".KKKKKk..KKKKk..",  # 29 shoes
]

CHAR_VEST = [
    # Same shape but vest instead of open suit
    "....HHHHHHHH....",
    "...HHHhHHhHHH...",
    "..HHHhHHHHhHHH..",
    "..HHHSSSSSSSSHh.",
    "..HHHSSSSSSSSSh.",
    "..HHHEESSSSEEsh.",
    "..HHHSeESSDeSSh.",
    "..HHHSSSSSSSSsh.",
    "..HHHSSSnSSSSsh.",
    "...HHSSSSSSSssh.",
    "...HHSSSmMSSSsh.",
    "....SSSSSSSSsss.",
    "....SSSSSSSSSS..",
    "....SSSSTtTSSS..",
    "..VvNNNtTTtNNVv.",  # V=vest color
    ".NNNNvVvTTvVvNN.",
    "NNNNNvVvTTvVvNNN",
    "NNNNPvVRTTRVvNNN",
    "NNNNNvVRTTRVvNNN",
    "NNNNNvVRtTRVvNNN",
    "NNNNNvVNtTNVvNNN",
    "NNNNNvVNNTNVvNNN",
    "NNNVvVNNNNNNVVnn",
    ".NBBBBBBBBBBBBn.",
    ".GGGGGGGGGGGGGg.",
    ".GGGGGGGGGGGGGg.",
    ".GGGGGGGGGGGGGg.",
    ".GGGGGg..GGGGg..",
    ".GGGGGg..GGGGg..",
    ".KKKKKk..KKKKk..",
]

# ── Background props ────────────────────────────────────────────────────────

WINDOW_ART = [
    # 14 wide x 12 tall
    "FFFFFFFFFFFFFF",  # 0 frame top
    "FbbbbbbFbbbbFF",  # 1 window panes (b=sky, F=frame)
    "FbbbbbbFbbbbFF",  # 2
    "FbbbbbbFbbbbFF",  # 3
    "FbbbbbbFbbbbFF",  # 4
    "FbbbbbbFbbbbFF",  # 5
    "FFFFFFFFFFFFff",  # 6 middle bar
    "FbbbbbbFbbbbFF",  # 7
    "FbbbbbbFbbbbFF",  # 8
    "FbbbbbbFbbbbFF",  # 9
    "FbbbbbbFbbbbFF",  # 10
    "FFFFFFFFFFFFFF",  # 11 frame bottom
]

BOOKSHELF_ART = [
    # 10 wide x 9 tall
    "SSSSSSSSSS",  # shelf plank
    "SaaBbBcCSS",  # books (a,B,c = colors)
    "SaaBbBcCSS",
    "SaaBbBcCSS",
    "SaaBbBcCSS",
    "SSSSSSSSSS",  # shelf plank
    "SddEEfFfSS",  # more books
    "SddEEfFfSS",
    "SSSSSSSSSS",  # shelf plank
]

# Main monitor: 12 wide x 9 tall
MONITOR_ART = [
    "MMMMMMMMMMMM",  # 0 frame top
    "MSSSSSSSSSSm",  # 1 screen (m=frame shadow)
    "MSSSSSSSSSSm",  # 2
    "MSSSSSSSSSSm",  # 3
    "MSSSSSSSSSSm",  # 4
    "MSSSSSSSSSSm",  # 5
    "MMMMMMMMMMmm",  # 6 frame bottom
    ".....MMM.....",  # 7 stand — wait 13... let me fix
]
MONITOR_ART = [
    "MMMMMMMMMMMM",  # 0 12 wide
    "MSSSSSSSSSSm",  # 1
    "MSSSSSSSSSSm",  # 2
    "MSSSSSSSSSSm",  # 3
    "MSSSSSSSSSSm",  # 4
    "MSSSSSSSSSSm",  # 5
    "MMMMMMMMMMmm",  # 6
    "....MMMM....",  # 7 stand  12 wide: 4+4+4=12 ✓
    "...MMMMMM...",  # 8 base   12: 3+6+3=12 ✓
]

MONITOR2_ART = [
    "MMMMMMMM",   # 0 8 wide
    "MSSSSSMm",   # 1
    "MSSSSSMm",   # 2
    "MSSSSSMm",   # 3
    "MSSSSSMm",   # 4
    "MMMMMmmm",   # 5
    "..MMMM..",   # 6 stand 8: 2+4+2=8 ✓
    "..MMMMM.",   # 7 base 8: 2+5+1=8 ✓
]

COFFEE_ART = [
    # 6 wide x 7 tall
    "..CCC.",   # steam  6: 2+3+1=6 ✓
    ".CcccC",   # mug top 6: 1+1+3+1=6 ✓
    ".CLLlC",   # liquid (L=coffee, l=highlight) 6 ✓
    ".CLLlC",
    ".CLLlC",
    ".CCCCn",   # mug bottom 6: 1+4+1=6 ✓
    ".HHHH.",   # handle curve 6 ✓
]

PLANT_ART = [
    # 7 wide x 8 tall
    "..GGG..",   # 0 leaf top 7 ✓
    ".GGGGGg",   # 1 leaves   7 ✓
    "GGGgGGg",   # 2          7 ✓
    ".GGgGGg",   # 3          7 ✓
    "..GGG..",   # 4          7 ✓
    "...S...",   # 5 stem     7 ✓
    "...S...",   # 6          7 ✓
    "..PPP..",   # 7 pot      7 ✓
]

DUCK_ART = [
    # 5 wide x 5 tall
    ".YYY.",   # 5 ✓
    "YYYYo",   # beak (o=orange)  5 ✓
    "YeYYY",   # eye (e=dark)     5 ✓
    ".YYY.",   # body             5 ✓
    "..Y..",   # feet             5 ✓
]


def _px(grid, colors, scale, ox=0, oy=0):
    """Render a pixel-art grid as SVG <rect> strings."""
    out = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "." or ch not in colors:
                continue
            out.append(
                f'<rect x="{(ox+x)*scale}" y="{(oy+y)*scale}"'
                f' width="{scale}" height="{scale}" fill="{colors[ch]}"/>'
            )
    return "".join(out)


def render_desk_scene(user: dict):
    equipped = gamification.get_equipped(user)
    owned    = gamification.get_owned_cosmetics(user)
    theme    = equipped.get("theme", "default")
    p        = PALETTES.get(theme, PALETTES["default"])
    level    = user.get("level", 1)
    title    = user.get("title", "Intern")
    streak   = user.get("streak", 0)
    is_vest  = "vest" in owned and equipped.get("cosmetic") == "vest"

    # ── Scene constants ─────────────────────────────────────────────────────
    # Virtual pixel grid: 128 wide × 72 tall, scale=5 → 640×360 SVG
    VW, VH, S = 128, 72, 5

    FLOOR_Y   = 52   # top of desk surface (virtual px)
    DESK_H    = 12
    CHAR_X    = 2    # character left in virtual px
    CHAR_Y    = 16   # character top
    MON_X     = 38   # main monitor left
    MON_Y     = 32   # main monitor top
    MON2_X    = 62   # second monitor
    WIN_X     = 4    # wall window left
    WIN_Y     = 4    # wall window top
    SHELF_X   = 100  # bookshelf left
    SHELF_Y   = 8    # bookshelf top

    # ── Background ───────────────────────────────────────────────────────────
    bg = (
        # Wall
        f'<rect x="0" y="0" width="{VW*S}" height="{FLOOR_Y*S}" fill="{p["wall"]}"/>'
        # Desk face (front edge visible)
        f'<rect x="0" y="{FLOOR_Y*S}" width="{VW*S}" height="{2*S}" fill="{p["desk_edge"]}"/>'
        # Desk surface
        f'<rect x="0" y="{(FLOOR_Y+2)*S}" width="{VW*S}" height="{(DESK_H-2)*S}" fill="{p["desk"]}"/>'
        # Desk top highlight stripe
        f'<rect x="0" y="{(FLOOR_Y+2)*S}" width="{VW*S}" height="{S}" fill="{p["desk_top"]}"/>'
        # Floor
        f'<rect x="0" y="{(FLOOR_Y+DESK_H)*S}" width="{VW*S}" height="{(VH-FLOOR_Y-DESK_H)*S}" fill="{p["floor"]}"/>'
        # Chair back (visible above desk, behind character)
        f'<rect x="{(CHAR_X+1)*S}" y="{(CHAR_Y-3)*S}" width="{14*S}" height="{4*S}" fill="{p["desk"]}"/>'
        f'<rect x="{(CHAR_X+1)*S}" y="{(CHAR_Y-3)*S}" width="{14*S}" height="{S}" fill="{p["desk_top"]}"/>'
    )

    # ── Wall window ─────────────────────────────────────────────────────────
    win_colors = {
        "F": p["win_frame"],
        "b": p["win_sky"],
        "f": p["desk_edge"],  # inner shadow
    }
    # Curtain hints (two small rects either side of window)
    curtain_c = p.get("book1", "#8a3020")
    curtain = (
        f'<rect x="{(WIN_X-2)*S}" y="{WIN_Y*S}" width="{2*S}" height="{12*S}" fill="{curtain_c}" opacity="0.7"/>'
        f'<rect x="{(WIN_X+14)*S}" y="{WIN_Y*S}" width="{2*S}" height="{12*S}" fill="{curtain_c}" opacity="0.7"/>'
    )
    window_svg = _px(WINDOW_ART, win_colors, S, WIN_X, WIN_Y)

    # ── Bookshelf ────────────────────────────────────────────────────────────
    shelf_colors = {
        "S": p["shelf"],
        "a": p["book1"],
        "B": p["book2"],
        "c": p["glow"],
        "C": p["border"],
        "d": p["tie"],
        "E": p["suit_hi"],
        "f": p["hair"],
        "F": p["skin_sh"],
    }
    shelf_svg = _px(BOOKSHELF_ART, shelf_colors, S, SHELF_X, SHELF_Y)

    # ── Character ─────────────────────────────────────────────────────────
    vest_hi = p.get("book2", "#2a1a30")   # vest highlight uses a contrasting hue
    vest_sh = p.get("desk_edge", "#1c0820")
    char_colors = {
        "H": p["hair"],    "h": p["hair_hi"],
        "S": p["skin"],    "s": p["skin_sh"],
        "E": p["hair"],    "e": "#e8e8e8",    "D": "#1a1a1a",
        "n": p["skin_sh"], "M": p["skin_sh"],
        "N": p["suit"],    "r": p["suit_hi"], "R": p["suit_sh"],
        "W": p["shirt"],   "w": p["shirt_sh"],
        "T": p["tie"],     "t": p["tie_sh"],
        "G": p["pants"],   "g": p["pants_sh"],
        "K": p["shoe"],    "B": p["belt"],     "P": p["shirt"],
        "V": vest_hi,      "v": vest_sh,
    }
    char_grid = CHAR_VEST if is_vest else CHAR_BODY
    char_svg  = _px(char_grid, char_colors, S, CHAR_X, CHAR_Y)

    # ── Monitor ───────────────────────────────────────────────────────────
    mon_colors = {"M": p["border"], "S": p["screen"], "m": p["desk_edge"]}

    def screen_lines(lx, ly, width, rows):
        """Glowing lines of 'code' on the screen."""
        lens   = [int(width*0.7), int(width*0.5), int(width*0.8),
                  int(width*0.4), int(width*0.65)]
        result = ""
        for i in range(rows):
            ww = lens[i % len(lens)] * S
            result += (
                f'<rect x="{(lx+1)*S}" y="{(ly+1+i)*S + S//3}" '
                f'width="{ww}" height="{max(2, S//3)}" '
                f'fill="{p["glow"]}" opacity="0.65"/>'
            )
        return result

    mon_svg = (
        _px(MONITOR_ART, mon_colors, S, MON_X, MON_Y)
        + screen_lines(MON_X, MON_Y, 10, 5)
    )

    mon2_svg = ""
    if "extra_monitor" in owned:
        mon2_svg = (
            _px(MONITOR2_ART, mon_colors, S, MON2_X, MON_Y + 2)
            + screen_lines(MON2_X, MON_Y + 2, 6, 4)
        )

    # ── Keyboard (always present) ────────────────────────────────────────
    kb_x, kb_y = MON_X - 2, FLOOR_Y + 4
    keyboard = (
        f'<rect x="{kb_x*S}" y="{kb_y*S}" width="{14*S}" height="{3*S}" fill="{p["desk_top"]}" rx="2"/>'
        # Key rows
        + "".join(
            f'<rect x="{(kb_x+1+kx)*S + 1}" y="{(kb_y+1+ky)*S + 1}" '
            f'width="{S-2}" height="{S-2}" fill="{p["border"]}" opacity="0.25"/>'
            for ky in range(2) for kx in range(12)
        )
    )

    # ── Desk items ────────────────────────────────────────────────────────
    items_svg = ""
    ix = 90   # right-side item column (virtual px)

    if "coffee_cup" in owned:
        cc = {
            "C": "#7a5030", "c": "#8a6040",
            "L": "#5a2808", "l": "#c8a060",
            "H": "#4a3020", "n": "#3a2010",
        }
        items_svg += _px(COFFEE_ART, cc, S, ix, FLOOR_Y + 2)
        ix += 8

    if "desk_plant" in owned:
        pc = {
            "G": "#3a8a2a", "g": "#247018",
            "S": "#6a4010", "P": "#7a5020",
        }
        items_svg += _px(PLANT_ART, pc, S, ix, FLOOR_Y - 3)
        ix += 9

    if "rubber_duck" in owned:
        dc = {"Y": "#f0c020", "o": "#e07810", "e": "#1a1a1a"}
        items_svg += _px(DUCK_ART, dc, S, ix, FLOOR_Y + 3)
        ix += 7

    if "framed_cert" in owned:
        fx, fy = 82, 12
        items_svg += (
            f'<rect x="{fx*S}" y="{fy*S}" width="{10*S}" height="{8*S}" fill="{p["shelf"]}"/>'
            f'<rect x="{fx*S}" y="{fy*S}" width="{10*S}" height="{8*S}"'
            f' fill="none" stroke="{p["border"]}" stroke-width="2"/>'
            f'<rect x="{(fx+1)*S}" y="{(fy+1)*S}" width="{8*S}" height="{S}"'
            f' fill="{p["glow"]}" opacity="0.4"/>'
            f'<rect x="{(fx+2)*S}" y="{(fy+3)*S}" width="{6*S}" height="{S//2}"'
            f' fill="{p["glow"]}" opacity="0.25"/>'
            f'<rect x="{(fx+1)*S}" y="{(fy+5)*S}" width="{5*S}" height="{S//2}"'
            f' fill="{p["glow"]}" opacity="0.2"/>'
        )

    if "stress_ball" in owned:
        bx, by = ix, FLOOR_Y + 3
        items_svg += (
            f'<rect x="{bx*S}" y="{by*S}" width="{4*S}" height="{4*S}"'
            f' fill="{p["tie"]}" rx="{2*S}"/>'
            f'<rect x="{(bx+1)*S}" y="{(by+1)*S}" width="{S}" height="{S}"'
            f' fill="{p["shirt"]}" opacity="0.4" rx="{S//2}"/>'
        )
        ix += 6

    # Streak flame (3+ day streak)
    if streak >= 3:
        fx2 = 120
        intensity = min(streak / 10, 1.0)
        items_svg += (
            # outer flame
            f'<rect x="{fx2*S}" y="{(FLOOR_Y+1)*S}" width="{2*S}" height="{4*S}" fill="#ff6600"/>'
            f'<rect x="{(fx2-1)*S}" y="{(FLOOR_Y+2)*S}" width="{4*S}" height="{3*S}" fill="#ff6600"/>'
            f'<rect x="{fx2*S}" y="{(FLOOR_Y+2)*S}" width="{2*S}" height="{3*S}" fill="#ffcc00"/>'
            f'<rect x="{(fx2+1)*S}" y="{(FLOOR_Y+3)*S}" width="{S}" height="{S}" fill="#ffffff" opacity="{intensity:.1f}"/>'
            # streak count
            f'<text x="{fx2*S + S}" y="{(FLOOR_Y+6)*S}"'
            f' font-family="Inter,sans-serif" font-size="{int(S*1.5)}"'
            f' fill="{p["glow"]}" text-anchor="middle">{streak}🔥</text>'
        )

    # ── Floor shadow under desk ───────────────────────────────────────────
    shadow = (
        f'<rect x="{S*4}" y="{(FLOOR_Y+DESK_H)*S}" width="{(VW-8)*S}" height="{S}"'
        f' fill="#000000" opacity="0.3"/>'
    )

    # ── Name plate / info bar ─────────────────────────────────────────────
    bar_y = (VH - 4) * S
    name_bar = (
        f'<rect x="0" y="{bar_y}" width="{VW*S}" height="{4*S}" fill="{p["wall"]}" opacity="0.85"/>'
        f'<rect x="0" y="{bar_y}" width="{VW*S}" height="{S//2}" fill="{p["border"]}" opacity="0.7"/>'
        f'<text x="{VW*S//2}" y="{bar_y + int(S*2.6)}"'
        f' font-family="Inter,sans-serif" font-size="{int(S*2)}"'
        f' fill="{p["glow"]}" text-anchor="middle" font-weight="700">'
        f'{user["name"]} · {title} · Lv {level} · {user.get("xp",0):,} XP'
        f'</text>'
    )

    # ── Assemble ─────────────────────────────────────────────────────────
    svg = (
        f'<svg viewBox="0 0 {VW*S} {VH*S}" width="100%" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="display:block;image-rendering:pixelated;border-radius:6px;'
        f'border:1px solid {p["border"]}33;max-height:380px">'
        + bg
        + curtain
        + window_svg
        + shelf_svg
        + char_svg
        + mon_svg
        + mon2_svg
        + keyboard
        + items_svg
        + shadow
        + name_bar
        + f'</svg>'
    )

    st.markdown(svg, unsafe_allow_html=True)
    st.caption("Equip cosmetics from the Shop to customize your desk scene.")
