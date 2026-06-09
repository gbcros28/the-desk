"""Pixel desk scene — renders via st.markdown with unsafe_allow_html."""
import streamlit as st
import gamification

SCENE_PALETTES = {
    "default":         {"bg": "#0f1117", "surface": "#171c27", "border": "#4a8fe8", "shadow": "#1a3060", "fg": "#7ab8f5", "screen_bg": "#050a14", "screen_fg": "#4a8fe8"},
    "bloomberg_theme": {"bg": "#0a0600", "surface": "#120d00", "border": "#e87d2a", "shadow": "#7a2000", "fg": "#f0c080", "screen_bg": "#050300", "screen_fg": "#e87d2a"},
    "stardew_theme":   {"bg": "#1a2812", "surface": "#223318", "border": "#8ab44a", "shadow": "#0d1406", "fg": "#e8f0d0", "screen_bg": "#141e0a", "screen_fg": "#8ab44a"},
    "cherry_theme":    {"bg": "#120810", "surface": "#1c1018", "border": "#d4608a", "shadow": "#7a0030", "fg": "#f0dce8", "screen_bg": "#0e0610", "screen_fg": "#d4608a"},
    "midnight_theme":  {"bg": "#080012", "surface": "#10001e", "border": "#7c4dff", "shadow": "#220044", "fg": "#e0d8f8", "screen_bg": "#060008", "screen_fg": "#00e5ff"},
    "gold_theme":      {"bg": "#0a0800", "surface": "#141000", "border": "#c8a428", "shadow": "#3a2800", "fg": "#f0e8c0", "screen_bg": "#080600", "screen_fg": "#c8a428"},
}

SCREEN_LABELS = {
    "default": "📈", "bloomberg_theme": "BBRG", "stardew_theme": "📊",
    "cherry_theme": "✿", "midnight_theme": "◈", "gold_theme": "◎",
}


def render_desk_scene(user: dict):
    equipped = gamification.get_equipped(user)
    owned    = gamification.get_owned_cosmetics(user)
    theme    = equipped.get("theme", "default")
    p        = SCENE_PALETTES.get(theme, SCENE_PALETTES["default"])
    level    = user.get("level", 1)
    title    = user.get("title", "Intern")
    streak   = user.get("streak", 0)
    scr      = SCREEN_LABELS.get(theme, "📈")

    # Character
    if "vest" in owned and equipped.get("cosmetic") == "vest":
        char = "🧑‍💼"
    elif level >= 8:
        char = "👔"
    elif level >= 5:
        char = "🧑‍💻"
    else:
        char = "🧒"

    # Monitor HTML
    def mon(w=72):
        return (
            f'<div style="display:inline-flex;flex-direction:column;align-items:center;margin:0 4px">'
            f'<div style="width:{w}px;height:46px;background:{p["screen_bg"]};'
            f'border:2px solid {p["border"]};'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:9px;color:{p["screen_fg"]}">{scr}</div>'
            f'<div style="width:14px;height:4px;background:{p["border"]};opacity:0.5"></div>'
            f'<div style="width:32px;height:3px;background:{p["shadow"]}"></div>'
            f'</div>'
        )

    monitors = mon()
    if "extra_monitor" in owned:
        monitors += mon(56)

    # Desk items
    items = ["⌨️"]
    if "coffee_cup"  in owned: items.append("☕")
    if "desk_plant"  in owned: items.append("🪴")
    if "rubber_duck" in owned: items.append("🦆")
    if "stress_ball" in owned: items.append("🔴")
    if "framed_cert" in owned: items.append("📜")
    if streak >= 3:             items.append("🔥")
    items_html = "".join(
        f'<span style="font-size:17px;margin:0 3px">{i}</span>' for i in items
    )

    html = (
        f'<div style="background:{p["bg"]};border:2px solid {p["border"]};'
        f'padding:14px 16px 10px;max-width:240px;text-align:center;'
        f'box-shadow:3px 3px 0 {p["shadow"]}">'

        f'<div style="font-size:11px;color:{p["fg"]};font-weight:600;'
        f'border-bottom:1px solid {p["border"]};padding-bottom:6px;margin-bottom:8px">'
        f'{user["name"]} · {title}</div>'

        f'<div style="font-size:42px;line-height:1;margin-bottom:8px">{char}</div>'

        f'<div style="display:flex;justify-content:center;align-items:flex-end;margin-bottom:8px">'
        f'{monitors}</div>'

        f'<div style="background:{p["surface"]};border-top:2px solid {p["border"]};'
        f'padding:6px 8px;display:flex;flex-wrap:wrap;justify-content:center">'
        f'{items_html}</div>'

        f'<div style="font-size:11px;color:{p["fg"]};opacity:0.6;margin-top:6px">'
        f'Lv {level} · {streak}d streak</div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)
    st.caption("Buy items in the Shop to customize your desk")
