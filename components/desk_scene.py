"""Visual desk scene — character + cosmetics rendered as styled HTML."""
import streamlit as st
import gamification


def render_desk_scene(user: dict):
    equipped = gamification.get_equipped(user)
    owned = gamification.get_owned_cosmetics(user)
    theme = equipped.get("theme", "default")
    level = user.get("level", 1)
    title = user.get("title", "Intern")
    streak = user.get("streak", 0)

    # --- Character ---
    if "vest" in owned and equipped.get("cosmetic") == "vest":
        character = "🧑‍💼"
    elif level >= 7:
        character = "👔"
    else:
        character = "🧑‍💻"

    # --- Monitor(s) ---
    screen_color = "#00ff00" if theme == "bloomberg_theme" else "#4a90d9" if theme == "default" else "#555"
    screen_bg = "#000" if theme == "bloomberg_theme" else "#1a2233" if theme == "default" else "#111"
    monitor_glow = "0 0 12px #00ff00" if theme == "bloomberg_theme" else "0 0 8px #4a90d9"

    monitor1 = f"""
    <div style="display:inline-block;text-align:center;margin:0 6px;">
      <div style="width:80px;height:52px;background:{screen_bg};border:2px solid {screen_color};
                  border-radius:4px;box-shadow:{monitor_glow};display:flex;align-items:center;
                  justify-content:center;font-size:10px;color:{screen_color};font-family:monospace;">
        {'BLOOMBERG' if theme == 'bloomberg_theme' else '📈'}
      </div>
      <div style="width:20px;height:6px;background:#555;margin:0 auto;"></div>
      <div style="width:40px;height:3px;background:#444;margin:0 auto;border-radius:2px;"></div>
    </div>"""

    monitor2 = ""
    if "extra_monitor" in owned:
        monitor2 = f"""
        <div style="display:inline-block;text-align:center;margin:0 6px;">
          <div style="width:80px;height:52px;background:{screen_bg};border:2px solid {screen_color};
                      border-radius:4px;box-shadow:{monitor_glow};display:flex;align-items:center;
                      justify-content:center;font-size:10px;color:{screen_color};font-family:monospace;">
            {'TERMINAL' if theme == 'bloomberg_theme' else '📊'}
          </div>
          <div style="width:20px;height:6px;background:#555;margin:0 auto;"></div>
          <div style="width:40px;height:3px;background:#444;margin:0 auto;border-radius:2px;"></div>
        </div>"""

    # --- Desk items ---
    items_html = ""
    if "coffee_cup" in owned:
        items_html += '<span style="font-size:22px;margin:0 4px;" title="Coffee">☕</span>'
    if "desk_plant" in owned:
        items_html += '<span style="font-size:22px;margin:0 4px;" title="Desk plant">🪴</span>'

    # Streak flame
    if streak >= 3:
        items_html += f'<span style="font-size:18px;margin:0 4px;" title="{streak}-day streak">🔥</span>'

    # Keyboard
    items_html += '<span style="font-size:18px;margin:0 4px;" title="Keyboard">⌨️</span>'

    # Desk background color
    desk_bg = "#0a0a00" if theme == "bloomberg_theme" else "#1a2233" if theme == "default" else "#111"
    desk_surface = "#1a1200" if theme == "bloomberg_theme" else "#2a3450" if theme == "default" else "#222"
    border_color = "#ff6600" if theme == "bloomberg_theme" else "#4a90d9" if theme == "default" else "#444"

    html = f"""
    <div style="background:{desk_bg};border:1px solid {border_color};border-radius:12px;
                padding:20px 24px 12px;margin:12px 0;text-align:center;max-width:480px;">

      <!-- character -->
      <div style="font-size:52px;line-height:1;margin-bottom:6px;">{character}</div>
      <div style="font-size:11px;color:#888;margin-bottom:10px;">{user['name']} · {title}</div>

      <!-- monitors -->
      <div style="margin-bottom:10px;">
        {monitor1}
        {monitor2}
      </div>

      <!-- desk surface -->
      <div style="background:{desk_surface};border-radius:6px 6px 4px 4px;
                  border-top:3px solid {border_color};padding:8px 12px;
                  display:flex;align-items:center;justify-content:center;gap:4px;flex-wrap:wrap;">
        {items_html if items_html else '<span style="font-size:18px;">📋</span>'}
      </div>

      <div style="font-size:10px;color:#555;margin-top:8px;">
        Visit the Shop to customize your desk
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
