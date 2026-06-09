"""
Pixel art desk scene — SVG-based, scales to full container width.
Character, desk, monitor, and items all rendered as pixel art rectangles.
"""
import streamlit as st
import gamification

# ── Palette per theme ──────────────────────────────────────────────────────
PALETTES = {
    "default":         {"bg": "#0f1117", "floor": "#171c27", "desk": "#1e2a3a", "desk_top": "#253346",
                        "screen": "#050e1a", "screen_glow": "#4a8fe8", "border": "#4a8fe8",
                        "suit": "#1e3a6e", "pants": "#152a50", "shirt": "#e8eef8",
                        "tie": "#c0392b", "skin": "#f5c2a0", "hair": "#2d1b0e",
                        "shoe": "#141210", "wall": "#0d1420"},

    "bloomberg_theme": {"bg": "#0a0600", "floor": "#120d00", "desk": "#1a1000", "desk_top": "#221500",
                        "screen": "#000", "screen_glow": "#e87d2a", "border": "#e87d2a",
                        "suit": "#1a0e00", "pants": "#100a00", "shirt": "#f0c080",
                        "tie": "#e87d2a", "skin": "#f5c2a0", "hair": "#2d1b0e",
                        "shoe": "#0a0800", "wall": "#070400"},

    "stardew_theme":   {"bg": "#1a2812", "floor": "#223318", "desk": "#4a3520", "desk_top": "#5a4228",
                        "screen": "#0a1406", "screen_glow": "#8ab44a", "border": "#8ab44a",
                        "suit": "#2a4a20", "pants": "#1e3818", "shirt": "#e8f0d0",
                        "tie": "#c8a428", "skin": "#f5c2a0", "hair": "#5a3010",
                        "shoe": "#1a1008", "wall": "#141e0c"},

    "cherry_theme":    {"bg": "#120810", "floor": "#1c1018", "desk": "#2a1020", "desk_top": "#341428",
                        "screen": "#0a0510", "screen_glow": "#d4608a", "border": "#d4608a",
                        "suit": "#2a1040", "pants": "#1e0c30", "shirt": "#f8e0ec",
                        "tie": "#d4608a", "skin": "#f5c2a0", "hair": "#2d1b0e",
                        "shoe": "#100810", "wall": "#0e0610"},

    "midnight_theme":  {"bg": "#080012", "floor": "#10001e", "desk": "#180828", "desk_top": "#200a34",
                        "screen": "#04000a", "screen_glow": "#00e5ff", "border": "#7c4dff",
                        "suit": "#1a0840", "pants": "#12063a", "shirt": "#d0c8f8",
                        "tie": "#7c4dff", "skin": "#f5c2a0", "hair": "#2d1b0e",
                        "shoe": "#0a0818", "wall": "#060010"},

    "gold_theme":      {"bg": "#0a0800", "floor": "#141000", "desk": "#2a1e08", "desk_top": "#342610",
                        "screen": "#060400", "screen_glow": "#c8a428", "border": "#c8a428",
                        "suit": "#1a1400", "pants": "#120e00", "shirt": "#f0e8c0",
                        "tie": "#c8a428", "skin": "#f5c2a0", "hair": "#2d1b0e",
                        "shoe": "#0e0c00", "wall": "#080600"},
}

# ── Pixel art definitions (row strings, 1 char = 1 pixel) ─────────────────
# Key: . = transparent

CHAR_BODY = [
    # 12 wide x 22 tall — finance character
    "....HHHHHH..",  # 0  hair
    "...HHHHHHHH.",  # 1  hair
    "...HSSSSSSSH.",  # 2  forehead
    "...HSEESSEEH.",  # 3  eyes
    "...HSSSSSSSH.",  # 4  face
    "...HSSMMSSSH.",  # 5  mouth
    "....SSTTTSS..",  # 6  neck + tie
    "..WWNNTTNNNW.",  # 7  collar
    "..NNNNTTNNN..",  # 8  upper suit
    "..NNNNTTNNN..",  # 9  suit
    "..NNNNTTNNN..",  # 10 suit
    "..NNNNNNNN..",   # 11 suit lower (no tie)
    "..NNNNNNNN..",   # 12 suit hem
    "...GGGGGGG..",   # 13 pants
    "...GGGGGGG..",   # 14 pants
    "...GGG.GGG..",   # 15 legs split
    "...GGG.GGG..",   # 16 legs
    "...GGG.GGG..",   # 17 legs
    "...KKK.KKK..",   # 18 shoes
    "..KKKK.KKKK.",   # 19 shoes
]

CHAR_VEST = [
    # Same but with vest (darker suit, different collar)
    "....HHHHHH..",
    "...HHHHHHHH.",
    "...HSSSSSSSH.",
    "...HSEESSEEH.",
    "...HSSSSSSSH.",
    "...HSSMMSSSH.",
    "....SSTTTSS..",
    "..VVNNTTNNNV.",
    "..VVVVTTVVV..",
    "..VVVVTTVVV..",
    "..VVVVTTVVV..",
    "..VVVVVVVV..",
    "..VVVVVVVV..",
    "...GGGGGGG..",
    "...GGGGGGG..",
    "...GGG.GGG..",
    "...GGG.GGG..",
    "...GGG.GGG..",
    "...KKK.KKK..",
    "..KKKK.KKKK.",
]

MONITOR_ART = [
    # 10 wide x 7 tall
    "MMMMMMMMMM",
    "MSSSSSSSM.",
    "MSSSSSSSM.",
    "MSSSSSSSM.",
    "MMMMMMMMMM",
    "....MMM...",
    "...MMMMM..",
]

MONITOR2_ART = [
    "MMMMMMMM",
    "MSSSSSSM",
    "MSSSSSSM",
    "MSSSSSSM",
    "MMMMMMMM",
    "...MMM..",
    "..MMMMM.",
]

COFFEE_ART = [
    ".CCC.",
    "CLLC.",
    "CLLC.",
    ".CCC.",
    ".BBB.",
]

PLANT_ART = [
    # 5 wide x 6 tall
    ".GGG.",
    "GGGGG",
    ".GGG.",
    "..S..",
    "..S..",
    ".PPP.",
]

DUCK_ART = [
    ".YYY.",
    "YYYYO",
    ".YYY.",
    "..Y..",
]


def _px(grid, colors, scale, ox=0, oy=0):
    """Convert a pixel art grid to SVG rect strings."""
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "." or ch not in colors:
                continue
            rx = (ox + x) * scale
            ry = (oy + y) * scale
            rects.append(
                f'<rect x="{rx}" y="{ry}" width="{scale}" height="{scale}" fill="{colors[ch]}"/>'
            )
    return "".join(rects)


def render_desk_scene(user: dict):
    equipped = gamification.get_equipped(user)
    owned    = gamification.get_owned_cosmetics(user)
    theme    = equipped.get("theme", "default")
    p        = PALETTES.get(theme, PALETTES["default"])
    level    = user.get("level", 1)
    title    = user.get("title", "Intern")
    streak   = user.get("streak", 0)

    use_vest = "vest" in owned and equipped.get("cosmetic") == "vest"
    char_grid = CHAR_VEST if use_vest else CHAR_BODY

    # ── Scene dimensions (virtual pixels, scale applied later) ─────────────
    # viewBox units — scene is 96 wide x 60 tall virtual pixels
    VW, VH = 96, 62
    S = 6   # px per virtual pixel → SVG = 576 x 372

    # Layout positions (virtual px)
    FLOOR_Y   = 46   # desk surface top
    DESK_H    = 10
    CHAR_X    = 4    # character left edge
    CHAR_Y    = 20   # character top (sits behind desk)
    MON_X     = 30   # monitor left edge
    MON_Y     = 28   # monitor top (on desk)
    MON2_X    = 52
    ITEMS_Y   = FLOOR_Y + 1   # items on desk surface

    # ── Background ─────────────────────────────────────────────────────────
    bg_rects = (
        # wall
        f'<rect x="0" y="0" width="{VW*S}" height="{FLOOR_Y*S}" fill="{p["wall"]}"/>'
        # floor/desk surface
        f'<rect x="0" y="{FLOOR_Y*S}" width="{VW*S}" height="{DESK_H*S}" fill="{p["desk"]}"/>'
        # desk top highlight
        f'<rect x="0" y="{FLOOR_Y*S}" width="{VW*S}" height="{2*S}" fill="{p["desk_top"]}"/>'
        # floor below desk
        f'<rect x="0" y="{(FLOOR_Y+DESK_H)*S}" width="{VW*S}" height="{(VH-FLOOR_Y-DESK_H)*S}" fill="{p["floor"]}"/>'
    )

    # ── Character ──────────────────────────────────────────────────────────
    vest_color = "#3a2a0a" if theme == "gold_theme" else "#2a1a30"
    char_colors = {
        "H": p["hair"], "S": p["skin"], "E": "#1a1a1a", "M": "#8a4030",
        "N": p["suit"],  "W": p["shirt"], "T": p["tie"],
        "G": p["pants"], "K": p["shoe"],  "V": vest_color,
    }
    char_svg = _px(char_grid, char_colors, S, CHAR_X, CHAR_Y)

    # ── Monitor(s) ─────────────────────────────────────────────────────────
    mon_colors = {"M": p["border"], "S": p["screen"]}

    # Screen content — small glow lines
    scr_glow = (
        f'<rect x="{(MON_X+1)*S}" y="{(MON_Y+1)*S}" width="{6*S}" height="{S//2}" fill="{p["screen_glow"]}" opacity="0.7"/>'
        f'<rect x="{(MON_X+1)*S}" y="{(MON_Y+2)*S}" width="{4*S}" height="{S//2}" fill="{p["screen_glow"]}" opacity="0.4"/>'
        f'<rect x="{(MON_X+1)*S}" y="{(MON_Y+3)*S}" width="{5*S}" height="{S//2}" fill="{p["screen_glow"]}" opacity="0.5"/>'
    )
    mon_svg = _px(MONITOR_ART, mon_colors, S, MON_X, MON_Y) + scr_glow

    mon2_svg = ""
    if "extra_monitor" in owned:
        scr2_glow = (
            f'<rect x="{(MON2_X+1)*S}" y="{(MON_Y+1)*S}" width="{4*S}" height="{S//2}" fill="{p["screen_glow"]}" opacity="0.6"/>'
            f'<rect x="{(MON2_X+1)*S}" y="{(MON_Y+2)*S}" width="{3*S}" height="{S//2}" fill="{p["screen_glow"]}" opacity="0.35"/>'
        )
        mon2_svg = _px(MONITOR2_ART, mon_colors, S, MON2_X, MON_Y) + scr2_glow

    # ── Desk items ─────────────────────────────────────────────────────────
    items_svg = ""
    ix = 74  # starting x for items (right side of desk)

    # Keyboard (always present) — simple pixel block
    kb_color = p.get("desk_top", "#253346")
    hl_color = p.get("screen_glow", "#4a8fe8")
    items_svg += (
        f'<rect x="{(MON_X)*S}" y="{(FLOOR_Y+3)*S}" width="{8*S}" height="{2*S}" fill="{kb_color}"/>'
        f'<rect x="{(MON_X+1)*S}" y="{(FLOOR_Y+3)*S}" width="{S//2}" height="{S//2}" fill="{hl_color}" opacity="0.5"/>'
        f'<rect x="{(MON_X+2)*S}" y="{(FLOOR_Y+3)*S}" width="{S//2}" height="{S//2}" fill="{hl_color}" opacity="0.5"/>'
    )

    if "coffee_cup" in owned:
        cc = {"C": "#8a6040", "L": "#c8a060", "B": "#4a3020"}
        items_svg += _px(COFFEE_ART, cc, S, ix, ITEMS_Y + 1)
        ix += 6

    if "desk_plant" in owned:
        pc = {"G": "#3a8a2a", "S": "#5a3a10", "P": "#8a6040"}
        items_svg += _px(PLANT_ART, pc, S, ix, ITEMS_Y - 1)
        ix += 6

    if "rubber_duck" in owned:
        dc = {"Y": "#f0c020", "O": "#e08010"}
        items_svg += _px(DUCK_ART, dc, S, ix, ITEMS_Y + 2)
        ix += 5

    # Framed cert — small rectangle on wall
    if "framed_cert" in owned:
        cert_x, cert_y = 80, 10
        items_svg += (
            f'<rect x="{cert_x*S}" y="{cert_y*S}" width="{8*S}" height="{6*S}" fill="{p["desk"]}"/>'
            f'<rect x="{cert_x*S}" y="{cert_y*S}" width="{8*S}" height="{6*S}" fill="none" '
            f'stroke="{p["border"]}" stroke-width="1"/>'
            f'<rect x="{(cert_x+1)*S}" y="{(cert_y+1)*S}" width="{6*S}" height="{S}" fill="{p["screen_glow"]}" opacity="0.3"/>'
        )

    # Streak flame — pixel art
    if streak >= 3:
        flame_x = 88
        items_svg += (
            f'<rect x="{flame_x*S}" y="{(ITEMS_Y+1)*S}" width="{S}" height="{3*S}" fill="#ff6600"/>'
            f'<rect x="{(flame_x-1)*S}" y="{(ITEMS_Y+2)*S}" width="{3*S}" height="{2*S}" fill="#ff6600"/>'
            f'<rect x="{flame_x*S}" y="{(ITEMS_Y+2)*S}" width="{S}" height="{2*S}" fill="#ffcc00"/>'
        )

    # ── Name plate ─────────────────────────────────────────────────────────
    # Rendered as SVG text (readable, not pixel art)
    name_svg = (
        f'<text x="{VW*S//2}" y="{(VH-1)*S}" '
        f'font-family="Inter,sans-serif" font-size="{int(S*1.8)}" '
        f'fill="{p["border"]}" text-anchor="middle" font-weight="600">'
        f'{user["name"]} · {title} · Lv {level}'
        f'</text>'
    )

    # ── Assemble SVG ───────────────────────────────────────────────────────
    svg_w = VW * S
    svg_h = VH * S

    svg = (
        f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="display:block;image-rendering:pixelated;max-height:360px">'
        f'{bg_rects}'
        f'{char_svg}'
        f'{mon_svg}'
        f'{mon2_svg}'
        f'{items_svg}'
        f'{name_svg}'
        f'</svg>'
    )

    st.markdown(svg, unsafe_allow_html=True)
    st.caption("Buy items in the Shop to customize your desk")
