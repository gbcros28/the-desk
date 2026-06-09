"""
CSS themes — pixel aesthetic, readable font sizes, hover effects.
"""
import streamlit as st

# Shared base CSS injected on every theme (layout, nav boxes, hover effects)
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

/* ── Typography ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    line-height: 1.7 !important;
}
h1 { font-family: 'Press Start 2P', monospace !important; font-size: 20px !important; letter-spacing: 2px; margin-bottom: 12px !important; }
h2 { font-family: 'Press Start 2P', monospace !important; font-size: 15px !important; letter-spacing: 1px; margin-bottom: 8px !important; }
h3 { font-family: 'Press Start 2P', monospace !important; font-size: 12px !important; margin-bottom: 6px !important; }
p, li, span, .stMarkdown p, .stMarkdown li { font-size: 18px !important; line-height: 1.8 !important; }
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 10px !important;
}
caption, .stCaption, small { font-size: 14px !important; opacity: 0.75; }

/* ── Streamlit chrome cleanup ────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 960px !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── Top nav bar ─────────────────────────────────────────────────────────── */
.desk-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 10px 0 14px;
    border-bottom: 3px solid var(--accent);
    margin-bottom: 18px;
}
.desk-nav-box {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    padding: 8px 12px;
    background: var(--surface);
    border: 2px solid var(--accent);
    box-shadow: 3px 3px 0 var(--shadow);
    color: var(--accent);
    cursor: pointer;
    transition: transform 0.08s, box-shadow 0.08s, background 0.08s;
    white-space: nowrap;
    user-select: none;
    line-height: 1.4;
}
.desk-nav-box:hover {
    transform: scale(1.12) translateY(-2px);
    box-shadow: 5px 5px 0 var(--shadow);
    background: var(--accent);
    color: var(--bg);
}
.desk-nav-box.active {
    background: var(--accent);
    color: var(--bg);
    box-shadow: 1px 1px 0 var(--shadow);
    transform: translate(2px, 2px);
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 10px !important;
    border-radius: 0 !important;
    padding: 10px 16px !important;
    background: var(--surface) !important;
    color: var(--accent) !important;
    border: 2px solid var(--accent) !important;
    box-shadow: 3px 3px 0 var(--shadow) !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg) !important;
    box-shadow: 1px 1px 0 var(--shadow) !important;
    transform: translate(2px, 2px) !important;
}
.stButton > button:active {
    box-shadow: none !important;
    transform: translate(3px, 3px) !important;
}

/* ── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    background: var(--surface) !important;
    color: var(--fg) !important;
    border: 2px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 8px !important;
}
.stSelectbox > div > div {
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: 0 !important;
}

/* ── Lesson content ──────────────────────────────────────────────────────── */
.lesson-why {
    padding: 14px 18px;
    border-left: 4px solid var(--accent);
    background: var(--surface);
    box-shadow: 3px 3px 0 var(--shadow);
    margin-bottom: 16px;
    font-size: 18px !important;
    line-height: 1.8;
}
.callout-interview_trap,
.callout-key_insight,
.callout-watch_out {
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 17px !important;
    line-height: 1.8;
}
.callout-interview_trap { border: 2px solid #e05252; box-shadow: 3px 3px 0 #600; background: #1a0808; }
.callout-key_insight    { border: 2px solid #52c452; box-shadow: 3px 3px 0 #060; background: #081a08; }
.callout-watch_out      { border: 2px solid #e0a030; box-shadow: 3px 3px 0 #640; background: #1a1208; }
.callout-interview_trap strong,
.callout-key_insight strong,
.callout-watch_out strong {
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    display: block;
    margin-bottom: 8px;
}
.formula-box {
    background: var(--surface);
    border: 2px solid var(--border);
    box-shadow: 4px 4px 0 var(--shadow);
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 18px !important;
    line-height: 1.9;
}
.formula-box strong {
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    display: block;
    margin-bottom: 8px;
}
.reward-card {
    border: 3px solid var(--accent);
    box-shadow: 6px 6px 0 var(--shadow);
    padding: 24px;
    text-align: center;
    background: var(--surface);
    margin: 16px 0;
}
.reward-card h2 { font-size: 14px !important; margin-bottom: 10px !important; }

/* ── Expanders ───────────────────────────────────────────────────────────── */
.stExpander { border: 2px solid var(--border) !important; border-radius: 0 !important; }
details summary { font-family: 'Press Start 2P', monospace !important; font-size: 10px !important; }

/* ── Progress bar ────────────────────────────────────────────────────────── */
.stProgress > div > div > div { border-radius: 0 !important; }

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 14px 0 !important; }
"""

# Per-theme variable overrides
THEME_VARS = {
    "default": """
        :root, .stApp {
            --bg:      #0d1117;
            --surface: #161c27;
            --border:  #2a3a5c;
            --accent:  #4a90d9;
            --shadow:  #1a3060;
            --fg:      #d0e4f8;
        }
        .stApp {
            background-color: #0d1117;
            background-image:
                linear-gradient(rgba(74,144,217,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(74,144,217,0.04) 1px, transparent 1px);
            background-size: 28px 28px;
        }
        h1,h2,h3 { color: #7ab8f5; }
        p, li, span, .stMarkdown p { color: #d0e4f8; }
    """,

    "bloomberg_theme": """
        :root, .stApp {
            --bg:      #000000;
            --surface: #0a0600;
            --border:  #ff6600;
            --accent:  #ff6600;
            --shadow:  #7a2000;
            --fg:      #ffaa44;
        }
        .stApp {
            background-color: #000;
            background-image: repeating-linear-gradient(
                0deg, transparent, transparent 3px,
                rgba(255,102,0,0.04) 3px, rgba(255,102,0,0.04) 4px
            );
        }
        h1,h2,h3 { color: #ff6600; text-transform: uppercase; }
        p, li, span, .stMarkdown p { color: #ffaa44; }
        .callout-interview_trap { border-color: #ff3333; background: #0d0000; }
        .callout-key_insight    { border-color: #00dd00; background: #000d00; }
        .callout-watch_out      { border-color: #ffcc00; background: #0d0a00; }
    """,

    "stardew_theme": """
        :root, .stApp {
            --bg:      #1e2e10;
            --surface: #2a4018;
            --border:  #8b6914;
            --accent:  #ffe87a;
            --shadow:  #0d1406;
            --fg:      #f5e6c8;
        }
        .stApp {
            background-color: #1e2e10;
            background-image:
                radial-gradient(circle, rgba(255,220,100,0.06) 1px, transparent 1px);
            background-size: 22px 22px;
        }
        h1,h2,h3 { color: #ffe87a; text-shadow: 2px 2px 0 #3a2800; }
        p, li, span, .stMarkdown p { color: #f5e6c8; }
        .callout-interview_trap { border-color: #e05252; background: #1a0808; }
        .callout-key_insight    { border-color: #7acc5a; background: #0a1a06; }
        .callout-watch_out      { border-color: #ffd54f; background: #1a1406; }
    """,

    "cherry_theme": """
        :root, .stApp {
            --bg:      #130810;
            --surface: #1f0c1a;
            --border:  #cc6080;
            --accent:  #ff8fab;
            --shadow:  #7a0030;
            --fg:      #ffe0eb;
        }
        .stApp {
            background-color: #130810;
            background-image:
                radial-gradient(circle at 30% 40%, rgba(255,143,171,0.05) 0%, transparent 60%);
        }
        h1,h2,h3 { color: #ff8fab; text-shadow: 2px 2px 0 #5a0020; }
        p, li, span, .stMarkdown p { color: #ffe0eb; }
        .callout-interview_trap { border-color: #ff5577; background: #1a0810; }
        .callout-key_insight    { border-color: #88cc99; background: #081810; }
        .callout-watch_out      { border-color: #ffcc88; background: #1a1408; }
    """,

    "midnight_theme": """
        :root, .stApp {
            --bg:      #080010;
            --surface: #0e0020;
            --border:  #6633cc;
            --accent:  #00e5ff;
            --shadow:  #220044;
            --fg:      #d0c0f0;
        }
        .stApp {
            background-color: #080010;
            background-image:
                linear-gradient(rgba(102,51,204,0.07) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,229,255,0.04) 1px, transparent 1px);
            background-size: 24px 24px;
        }
        h1,h2,h3 { color: #00e5ff; text-shadow: 0 0 10px rgba(0,229,255,0.4); }
        p, li, span, .stMarkdown p { color: #d0c0f0; }
        .callout-interview_trap { border-color: #ff4488; background: #140010; }
        .callout-key_insight    { border-color: #00ffbb; background: #001410; }
        .callout-watch_out      { border-color: #ffee00; background: #100e00; }
    """,

    "gold_theme": """
        :root, .stApp {
            --bg:      #080600;
            --surface: #120e00;
            --border:  #7a5c00;
            --accent:  #ffd700;
            --shadow:  #3a2800;
            --fg:      #eedda0;
        }
        .stApp {
            background-color: #080600;
            background-image:
                linear-gradient(rgba(200,160,0,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(200,160,0,0.05) 1px, transparent 1px);
            background-size: 28px 28px;
        }
        h1,h2,h3 { color: #ffd700; text-shadow: 2px 2px 0 #3a2800, 0 0 8px rgba(255,215,0,0.2); }
        p, li, span, .stMarkdown p { color: #eedda0; }
        .callout-interview_trap { border-color: #ff8844; background: #140800; }
        .callout-key_insight    { border-color: #aadd44; background: #081000; }
        .callout-watch_out      { border-color: #ffd700; background: #100e00; }
    """,
}

THEMES = {
    "default":         {"name": "The Desk"},
    "bloomberg_theme": {"name": "Bloomberg Terminal"},
    "stardew_theme":   {"name": "Stardew Farm"},
    "cherry_theme":    {"name": "Cherry Analyst"},
    "midnight_theme":  {"name": "Midnight Terminal"},
    "gold_theme":      {"name": "Gold Tier"},
}


def apply_theme(theme_id: str):
    vars_css = THEME_VARS.get(theme_id, THEME_VARS["default"])
    st.markdown(f"<style>{BASE_CSS}\n{vars_css}</style>", unsafe_allow_html=True)


def get_theme_name(theme_id: str) -> str:
    return THEMES.get(theme_id, THEMES["default"])["name"]


def all_theme_ids() -> list:
    return list(THEMES.keys())


# ── HTML helpers ──────────────────────────────────────────────────────────────

def callout_html(variant: str, body: str) -> str:
    icons = {
        "interview_trap": "⚠ INTERVIEW TRAP",
        "key_insight":    "★ KEY INSIGHT",
        "watch_out":      "► WATCH OUT",
    }
    label = icons.get(variant, variant.upper())
    return f'<div class="callout-{variant}"><strong>{label}</strong>{body}</div>'


def formula_html(label: str, expression: str, note: str = "") -> str:
    note_html = f"<br><span style='font-size:14px;opacity:0.7'>{note}</span>" if note else ""
    return f'<div class="formula-box"><strong>[ {label} ]</strong><code style="font-size:18px">{expression}</code>{note_html}</div>'


def why_html(why: str, in_the_seat: str = "") -> str:
    seat = f'<br><span style="font-size:14px;opacity:0.65">► On the job: {in_the_seat}</span>' if in_the_seat else ""
    return f'<div class="lesson-why"><strong style="font-family:\'Press Start 2P\',monospace;font-size:10px">★ WHY THIS MATTERS</strong><br><br>{why}{seat}</div>'


def reward_card_html(title: str, body: str) -> str:
    return f'<div class="reward-card"><h2>★ {title} ★</h2><p>{body}</p></div>'


def mastery_badge(mastery: float) -> str:
    if mastery >= 90: return "★"
    elif mastery >= 70: return "◆"
    elif mastery >= 40: return "●"
    elif mastery > 0:  return "○"
    return "🔒"
