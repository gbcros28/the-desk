"""
CSS themes — clean, professional dark UI with subtle monospace accents.
Body text uses Inter (readable). Monospace only for formulas/code.
Each theme is a single accent color on a dark base.
"""
import streamlit as st

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 900px !important;
}
[data-testid="stSidebar"] { display: none !important; }

/* ── Headings ────────────────────────────────────────────────────── */
h1 { font-size: 22px !important; font-weight: 600 !important;
     letter-spacing: -0.3px; margin-bottom: 6px !important; }
h2 { font-size: 18px !important; font-weight: 600 !important;
     margin-bottom: 4px !important; }
h3 { font-size: 15px !important; font-weight: 600 !important;
     margin-bottom: 2px !important; }
p, li { font-size: 15px !important; line-height: 1.75 !important; }
label { font-size: 13px !important; font-weight: 500 !important; }
small, .stCaption, caption { font-size: 13px !important; opacity: 0.6; }

/* ── Buttons ─────────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--border) !important;
    transition: background 0.15s, border-color 0.15s !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background: var(--accent-muted) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Tab nav ─────────────────────────────────────────────────────── */
.desk-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 12px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.desk-user-info {
    font-size: 13px;
    color: var(--fg-muted);
    font-weight: 500;
}
.desk-user-info strong { color: var(--fg); }

/* st.tabs() overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 1px solid var(--border) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--fg-muted) !important;
    padding: 8px 16px !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    transition: color 0.15s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--fg) !important; }
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Inputs ──────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: var(--surface) !important;
    color: var(--fg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}
.stSelectbox > div > div {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* ── Lesson content ──────────────────────────────────────────────── */
.lesson-why {
    padding: 14px 18px;
    border-left: 3px solid var(--accent);
    background: var(--surface);
    border-radius: 0 4px 4px 0;
    margin-bottom: 20px;
    font-size: 15px !important;
    line-height: 1.7;
}
.lesson-why .why-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 4px;
}
.lesson-why .why-seat {
    font-size: 13px;
    color: var(--fg-muted);
    margin-top: 6px;
}

.concept-section { margin: 18px 0; }
.concept-heading {
    font-size: 14px;
    font-weight: 600;
    color: var(--fg);
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border);
}
.concept-body { font-size: 15px !important; line-height: 1.8 !important; }

.callout-interview_trap,
.callout-key_insight,
.callout-watch_out {
    padding: 14px 18px;
    border-radius: 0 4px 4px 0;
    margin: 16px 0;
    font-size: 14px !important;
    line-height: 1.75;
}
.callout-interview_trap { border-left: 3px solid #e05252; background: #1f0e0e; }
.callout-key_insight    { border-left: 3px solid #4caf82; background: #0e1f14; }
.callout-watch_out      { border-left: 3px solid #d4a017; background: #1f1a0e; }
.callout-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.callout-interview_trap .callout-label { color: #e05252; }
.callout-key_insight    .callout-label { color: #4caf82; }
.callout-watch_out      .callout-label { color: #d4a017; }

.formula-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 16px 20px;
    margin: 16px 0;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
    line-height: 1.8;
}
.formula-label {
    font-family: 'Inter', sans-serif !important;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
}

.worked-example {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 20px 24px;
    margin: 20px 0;
}
.worked-example-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
}
.worked-step {
    display: flex;
    gap: 12px;
    margin: 10px 0;
    font-size: 14px;
    line-height: 1.7;
}
.worked-step-num {
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    min-width: 20px;
    margin-top: 3px;
}
.worked-takeaway {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
    font-size: 13px;
    color: var(--fg-muted);
    font-style: italic;
}

.reward-card {
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 24px;
    text-align: center;
    background: var(--surface);
    margin: 20px 0;
}

/* ── Skill tree ──────────────────────────────────────────────────── */
.track-header {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--fg-muted);
    padding: 8px 0 4px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.lesson-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 4px;
    margin: 3px 0;
    transition: background 0.1s;
    cursor: pointer;
}
.lesson-row:hover { background: var(--surface); }
.lesson-row.locked { opacity: 0.35; cursor: default; }
.mastery-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── Misc ────────────────────────────────────────────────────────── */
hr { border: none; border-top: 1px solid var(--border) !important; margin: 16px 0 !important; }
.stExpander { border: 1px solid var(--border) !important; border-radius: 4px !important; }
details summary { font-size: 14px !important; font-weight: 500 !important; }
.stProgress > div > div > div { border-radius: 2px !important; }
.stAlert { border-radius: 4px !important; font-size: 14px !important; }
"""

THEME_VARS = {
    "default": """
        :root {
            --bg:          #0f1117;
            --surface:     #171c27;
            --border:      #252d3d;
            --accent:      #4a8fe8;
            --accent-muted:#1a2d4a;
            --fg:          #e2e8f4;
            --fg-muted:    #8898aa;
        }
        .stApp { background-color: #0f1117; }
        h1,h2,h3 { color: #e2e8f4; }
        p, li, .stMarkdown p { color: #c8d6e8; }
    """,

    "bloomberg_theme": """
        :root {
            --bg:          #0a0600;
            --surface:     #120d00;
            --border:      #2a1a00;
            --accent:      #e87d2a;
            --accent-muted:#1a0e00;
            --fg:          #f0c080;
            --fg-muted:    #7a5030;
        }
        .stApp {
            background-color: #0a0600;
            background-image: repeating-linear-gradient(
                0deg, transparent, transparent 3px,
                rgba(232,125,42,0.025) 3px, rgba(232,125,42,0.025) 4px
            );
        }
        h1,h2,h3 { color: #f0c080; }
        p, li, .stMarkdown p { color: #d4a060; }
        .formula-box { font-family: 'JetBrains Mono', monospace !important; }
    """,

    "stardew_theme": """
        :root {
            --bg:          #1a2812;
            --surface:     #223318;
            --border:      #3a4e24;
            --accent:      #8ab44a;
            --accent-muted:#1e2e10;
            --fg:          #e8f0d0;
            --fg-muted:    #7a9050;
        }
        .stApp { background-color: #1a2812; }
        h1,h2,h3 { color: #e8f0d0; }
        p, li, .stMarkdown p { color: #c8daa8; }
    """,

    "cherry_theme": """
        :root {
            --bg:          #120810;
            --surface:     #1c1018;
            --border:      #2e1424;
            --accent:      #d4608a;
            --accent-muted:#1e0e18;
            --fg:          #f0dce8;
            --fg-muted:    #886070;
        }
        .stApp { background-color: #120810; }
        h1,h2,h3 { color: #f0dce8; }
        p, li, .stMarkdown p { color: #d8b8cc; }
    """,

    "midnight_theme": """
        :root {
            --bg:          #080012;
            --surface:     #10001e;
            --border:      #201030;
            --accent:      #7c4dff;
            --accent-muted:#120820;
            --fg:          #e0d8f8;
            --fg-muted:    #6050a0;
        }
        .stApp { background-color: #080012; }
        h1,h2,h3 { color: #e0d8f8; }
        p, li, .stMarkdown p { color: #c0b8e0; }
    """,

    "gold_theme": """
        :root {
            --bg:          #0a0800;
            --surface:     #141000;
            --border:      #2a2000;
            --accent:      #c8a428;
            --accent-muted:#1a1400;
            --fg:          #f0e8c0;
            --fg-muted:    #806820;
        }
        .stApp { background-color: #0a0800; }
        h1,h2,h3 { color: #f0e8c0; }
        p, li, .stMarkdown p { color: #d8cc90; }
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


def all_theme_ids():
    return list(THEMES.keys())


# ── HTML helpers ──────────────────────────────────────────────────────────

def callout_html(variant: str, body: str, heading: str = "") -> str:
    labels = {
        "interview_trap": "Interview Trap",
        "key_insight":    "Key Insight",
        "watch_out":      "Watch Out",
    }
    label = labels.get(variant, variant.replace("_", " ").title())
    heading_html = f"<div style='font-weight:600;margin-bottom:4px'>{heading}</div>" if heading else ""
    return (f'<div class="callout-{variant}">'
            f'<div class="callout-label">{label}</div>'
            f'{heading_html}{body}</div>')


def formula_html(label: str, body: str) -> str:
    return (f'<div class="formula-box">'
            f'<div class="formula-label">{label}</div>'
            f'<div>{body}</div></div>')


def why_html(why: str, in_the_seat: str = "") -> str:
    seat = (f'<div class="why-seat">On the job — {in_the_seat}</div>'
            if in_the_seat else "")
    return (f'<div class="lesson-why">'
            f'<div class="why-label">Why this matters</div>'
            f'<div>{why}</div>{seat}</div>')


def reward_card_html(title: str, body: str) -> str:
    return (f'<div class="reward-card">'
            f'<div style="font-weight:600;font-size:16px;margin-bottom:8px">{title}</div>'
            f'<div style="font-size:14px;opacity:0.75">{body}</div></div>')


def mastery_color(mastery: float) -> str:
    if mastery >= 90: return "#4caf82"
    elif mastery >= 70: return "#4a8fe8"
    elif mastery >= 40: return "#d4a017"
    elif mastery > 0:  return "#666"
    return "#333"


def mastery_badge(mastery: float) -> str:
    if mastery >= 90: return "●"
    elif mastery >= 70: return "●"
    elif mastery >= 40: return "●"
    elif mastery > 0:  return "○"
    return "🔒"
