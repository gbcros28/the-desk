"""CSS themes applied via st.markdown."""
import streamlit as st

THEMES = {
    "default": """
        <style>
        .stApp { background-color: #0f1117; color: #e8eaf0; }
        .lesson-why { background: #1a2233; border-left: 3px solid #4a90d9; padding: 12px 16px; border-radius: 4px; margin-bottom: 12px; }
        .callout-interview_trap { background: #2d1a1a; border-left: 4px solid #e05252; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .callout-key_insight    { background: #1a2d1a; border-left: 4px solid #52c452; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .callout-watch_out      { background: #2d2a1a; border-left: 4px solid #e0a030; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .formula-box { background: #1c1f2e; border: 1px solid #3a3f5c; border-radius: 6px; padding: 14px 18px; font-family: monospace; margin: 10px 0; }
        .reward-card { background: linear-gradient(135deg, #1a2d3d, #0f1117); border: 1px solid #4a90d9; border-radius: 8px; padding: 20px; text-align: center; }
        .mastery-bar-bg { background: #1e2230; border-radius: 4px; height: 8px; }
        .lock-icon { opacity: 0.4; }
        h1, h2, h3 { color: #c8d8f0; }
        </style>
    """,
    "bloomberg_theme": """
        <style>
        .stApp { background-color: #000000; color: #ff6600; font-family: monospace; }
        .lesson-why { background: #0a0a00; border-left: 3px solid #ff6600; padding: 12px 16px; border-radius: 2px; margin-bottom: 12px; }
        .callout-interview_trap { background: #1a0000; border-left: 4px solid #ff3333; padding: 10px 14px; margin: 8px 0; }
        .callout-key_insight    { background: #001a00; border-left: 4px solid #00ff00; padding: 10px 14px; margin: 8px 0; }
        .callout-watch_out      { background: #1a0f00; border-left: 4px solid #ffaa00; padding: 10px 14px; margin: 8px 0; }
        .formula-box { background: #0a0a0a; border: 1px solid #ff6600; padding: 14px 18px; font-family: monospace; margin: 10px 0; color: #ff9900; }
        .reward-card { background: #0a0a00; border: 1px solid #ff6600; padding: 20px; text-align: center; }
        h1, h2, h3 { color: #ff6600; font-family: monospace; }
        .stButton>button { background-color: #1a0800; color: #ff6600; border: 1px solid #ff6600; }
        </style>
    """,
    "dark_theme": """
        <style>
        .stApp { background-color: #0a0a0a; color: #cccccc; }
        .lesson-why { background: #141414; border-left: 3px solid #888; padding: 12px 16px; border-radius: 4px; margin-bottom: 12px; }
        .callout-interview_trap { background: #1a0f0f; border-left: 4px solid #cc4444; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .callout-key_insight    { background: #0f1a0f; border-left: 4px solid #44cc44; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .callout-watch_out      { background: #1a1a0f; border-left: 4px solid #ccaa00; padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
        .formula-box { background: #111; border: 1px solid #333; border-radius: 4px; padding: 14px 18px; font-family: monospace; margin: 10px 0; }
        .reward-card { background: #111; border: 1px solid #444; border-radius: 8px; padding: 20px; text-align: center; }
        h1, h2, h3 { color: #dddddd; }
        </style>
    """,
}


def apply_theme(theme_id: str):
    css = THEMES.get(theme_id, THEMES["default"])
    st.markdown(css, unsafe_allow_html=True)


def callout_html(variant: str, body: str) -> str:
    icons = {"interview_trap": "⚠️ Interview Trap", "key_insight": "💡 Key Insight", "watch_out": "👀 Watch Out"}
    label = icons.get(variant, variant)
    return f'<div class="callout-{variant}"><strong>{label}</strong><br>{body}</div>'


def formula_html(label: str, expression: str, note: str = "") -> str:
    note_html = f"<br><small style='opacity:0.7'>{note}</small>" if note else ""
    return f'<div class="formula-box"><strong>{label}</strong><br><code>{expression}</code>{note_html}</div>'


def why_html(why: str, in_the_seat: str = "") -> str:
    seat_html = f'<br><small style="opacity:0.65">On the job: {in_the_seat}</small>' if in_the_seat else ""
    return f'<div class="lesson-why">🎯 <strong>{why}</strong>{seat_html}</div>'


def reward_card_html(title: str, body: str) -> str:
    return f'<div class="reward-card"><h2>{title}</h2><p>{body}</p></div>'


def mastery_badge(mastery: float) -> str:
    if mastery >= 90:
        return "🥇"
    elif mastery >= 70:
        return "🥈"
    elif mastery >= 40:
        return "🥉"
    elif mastery > 0:
        return "📗"
    return "🔒"
