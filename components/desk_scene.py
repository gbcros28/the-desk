"""
Pixel desk scene — character + cosmetics rendered as styled HTML.
Updates live when you equip/buy items.
"""
import streamlit as st
import gamification


# Per-theme color palettes for the desk scene
SCENE_PALETTES = {
    "default":         {"bg": "#0d1117", "surface": "#1a2233", "border": "#4a90d9",   "shadow": "#1a3060",  "text": "#7ab8f5",  "screen_bg": "#050a14", "screen_fg": "#4a90d9"},
    "bloomberg_theme": {"bg": "#000",    "surface": "#0a0500", "border": "#ff6600",   "shadow": "#802000",  "text": "#ff9900",  "screen_bg": "#000",    "screen_fg": "#ff6600"},
    "stardew_theme":   {"bg": "#2d4a1e", "surface": "#1e3010", "border": "#8b6914",   "shadow": "#0d1406",  "text": "#ffe87a",  "screen_bg": "#141e0a", "screen_fg": "#ffe099"},
    "cherry_theme":    {"bg": "#1a0a14", "surface": "#1f0c18", "border": "#ff8fab",   "shadow": "#7a0030",  "text": "#ffb3c6",  "screen_bg": "#120810", "screen_fg": "#ff8fab"},
    "midnight_theme":  {"bg": "#080010", "surface": "#0d0018", "border": "#00ffff",   "shadow": "#004444",  "text": "#cc88ff",  "screen_bg": "#050008", "screen_fg": "#00ffff"},
    "gold_theme":      {"bg": "#080600", "surface": "#0f0c00", "border": "#ffd700",   "shadow": "#3a2a00",  "text": "#ffe566",  "screen_bg": "#080600", "screen_fg": "#ffd700"},
}

SCREEN_LABELS = {
    "default":         "📈",
    "bloomberg_theme": "BBRG",
    "stardew_theme":   "📊",
    "cherry_theme":    "✿",
    "midnight_theme":  "◈",
    "gold_theme":      "◎",
}


def render_desk_scene(user: dict):
    equipped   = gamification.get_equipped(user)
    owned      = gamification.get_owned_cosmetics(user)
    theme      = equipped.get("theme", "default")
    pal        = SCENE_PALETTES.get(theme, SCENE_PALETTES["default"])
    level      = user.get("level", 1)
    title      = user.get("title", "Intern")
    streak     = user.get("streak", 0)
    screen_txt = SCREEN_LABELS.get(theme, "📈")

    # ── Character sprite ─────────────────────────────────────────────────
    if "vest" in owned and equipped.get("cosmetic") == "vest":
        char = "🧑‍💼"
    elif level >= 8:
        char = "👔"
    elif level >= 5:
        char = "🧑‍💻"
    else:
        char = "🧒"

    # ── Monitor(s) ────────────────────────────────────────────────────────
    def monitor_html(label, width=72):
        return f"""
        <div style="display:inline-flex;flex-direction:column;align-items:center;margin:0 5px">
          <div style="width:{width}px;height:48px;background:{pal['screen_bg']};
               border:3px solid {pal['border']};
               box-shadow:3px 3px 0 {pal['shadow']};
               display:flex;align-items:center;justify-content:center;
               font-family:'Press Start 2P',monospace;font-size:8px;
               color:{pal['screen_fg']};letter-spacing:1px;
               image-rendering:pixelated;">
            {label}
          </div>
          <div style="width:16px;height:5px;background:{pal['border']};opacity:0.6"></div>
          <div style="width:36px;height:3px;background:{pal['shadow']};border-radius:0"></div>
        </div>"""

    monitors = monitor_html(screen_txt)
    if "extra_monitor" in owned:
        monitors = monitor_html(screen_txt) + monitor_html(screen_txt, 56)

    # ── Desk surface items ────────────────────────────────────────────────
    items = []
    items.append(f'<span title="Keyboard" style="font-size:16px">⌨️</span>')
    if "coffee_cup"   in owned: items.append('<span title="Coffee"     style="font-size:18px">☕</span>')
    if "desk_plant"   in owned: items.append('<span title="Plant"      style="font-size:18px">🪴</span>')
    if "rubber_duck"  in owned: items.append('<span title="Debug duck" style="font-size:16px">🦆</span>')
    if "stress_ball"  in owned: items.append('<span title="Stress ball"style="font-size:16px">🔴</span>')
    if "framed_cert"  in owned: items.append('<span title="CFA cert"   style="font-size:16px">📜</span>')
    if streak >= 3:              items.append(f'<span title="{streak}-day streak" style="font-size:14px">🔥</span>')
    items_row = "".join(f'<span style="margin:0 3px">{i}</span>' for i in items)

    # ── Pixel border helper ───────────────────────────────────────────────
    outer_shadow = f"4px 4px 0 {pal['shadow']}"

    html = f"""
    <div style="
        background:{pal['bg']};
        border:3px solid {pal['border']};
        box-shadow:{outer_shadow};
        padding:16px 20px 12px;
        margin:8px 0 16px;
        max-width:360px;
        text-align:center;
        image-rendering:pixelated;
        font-family:'Press Start 2P',monospace;
    ">
      <!-- name plate -->
      <div style="font-size:6px;color:{pal['text']};letter-spacing:1px;margin-bottom:8px;
                  border-bottom:2px solid {pal['border']};padding-bottom:6px;">
        {user['name'].upper()} · {title.upper()}
      </div>

      <!-- character -->
      <div style="font-size:44px;line-height:1;margin-bottom:8px">{char}</div>

      <!-- monitors -->
      <div style="margin-bottom:10px;display:flex;justify-content:center;align-items:flex-end;">
        {monitors}
      </div>

      <!-- desk surface -->
      <div style="
          background:{pal['surface']};
          border-top:3px solid {pal['border']};
          border-left:2px solid {pal['shadow']};
          border-right:2px solid {pal['shadow']};
          padding:7px 10px 6px;
          display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:2px;
      ">
        {items_row}
      </div>

      <!-- level bar -->
      <div style="font-size:5px;color:{pal['text']};margin-top:8px;letter-spacing:1px;opacity:0.7">
        LVL {level} · {streak}d STREAK
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.caption("Buy items in the Shop to customize your desk →")
