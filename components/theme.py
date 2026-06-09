"""
CSS themes — Stardew Valley x Bloomberg pixel aesthetic.
Each theme is a complete visual identity.
"""
import streamlit as st

# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------

THEMES = {

    # ── Default: clean dark desk ──────────────────────────────────────────
    "default": {
        "name": "The Desk",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #0d1117;
            background-image:
                linear-gradient(rgba(74,144,217,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(74,144,217,0.03) 1px, transparent 1px);
            background-size: 24px 24px;
        }
        h1 { font-size: 14px !important; color: #4a90d9; letter-spacing: 2px; }
        h2 { font-size: 11px !important; color: #7ab8f5; letter-spacing: 1px; }
        h3 { font-size: 9px  !important; color: #a0c8ff; }
        p, li, label, .stMarkdown { font-size: 8px !important; line-height: 2; color: #c8d8f0; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0d1117;
            color: #4a90d9;
            border: 2px solid #4a90d9;
            border-radius: 0;
            padding: 8px 12px;
            box-shadow: 3px 3px 0 #2a5090;
            transition: none;
        }
        .stButton > button:hover {
            background: #4a90d9;
            color: #0d1117;
            box-shadow: 1px 1px 0 #2a5090;
            transform: translate(2px, 2px);
        }
        .stButton > button:active {
            box-shadow: none;
            transform: translate(3px, 3px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0d1117 !important;
            color: #4a90d9 !important;
            border: 2px solid #2a3a5c !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0d1117 !important;
            border: 2px solid #2a3a5c !important;
            border-radius: 0 !important;
        }
        /* Pixel card / panel */
        .pixel-card {
            background: #111827;
            border: 3px solid #4a90d9;
            box-shadow: 4px 4px 0 #1a3060, inset 0 0 0 1px #1e2d4a;
            padding: 16px;
            margin: 8px 0;
        }
        .lesson-why {
            background: #0d1a2e;
            border-left: 4px solid #4a90d9;
            border-top: 2px solid #2a5090;
            padding: 10px 14px;
            font-size: 7px !important;
            line-height: 2;
            box-shadow: 3px 3px 0 #0a1020;
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #1a0808;
            border: 2px solid #e05252;
            box-shadow: 3px 3px 0 #600;
            padding: 10px 14px;
            margin: 8px 0;
            font-size: 7px !important;
            line-height: 2;
        }
        .callout-key_insight {
            background: #081a08;
            border: 2px solid #52c452;
            box-shadow: 3px 3px 0 #060;
            padding: 10px 14px;
            margin: 8px 0;
            font-size: 7px !important;
            line-height: 2;
        }
        .callout-watch_out {
            background: #1a1208;
            border: 2px solid #e0a030;
            box-shadow: 3px 3px 0 #640;
            padding: 10px 14px;
            margin: 8px 0;
            font-size: 7px !important;
            line-height: 2;
        }
        .formula-box {
            background: #080d14;
            border: 2px solid #2a5090;
            box-shadow: 4px 4px 0 #0a1a30;
            padding: 14px;
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            margin: 10px 0;
            line-height: 2;
        }
        .reward-card {
            background: #0d1117;
            border: 3px solid #4a90d9;
            box-shadow: 6px 6px 0 #1a3060;
            padding: 20px;
            text-align: center;
            margin: 12px 0;
        }
        [data-testid="stSidebar"] {
            background: #080d14 !important;
            border-right: 3px solid #1e2d4a;
        }
        """,
    },

    # ── Bloomberg Terminal ────────────────────────────────────────────────
    "bloomberg_theme": {
        "name": "Bloomberg Terminal",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #000000;
            background-image: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(255,102,0,0.03) 2px,
                rgba(255,102,0,0.03) 4px
            );
        }
        h1 { font-size: 12px !important; color: #ff6600; letter-spacing: 3px; text-transform: uppercase; }
        h2 { font-size: 10px !important; color: #ff9900; letter-spacing: 2px; text-transform: uppercase; }
        h3 { font-size: 8px  !important; color: #ffaa33; text-transform: uppercase; }
        p, li, label, .stMarkdown { font-size: 7px !important; line-height: 2.2; color: #ff8800; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 6px !important;
            background: #000;
            color: #ff6600;
            border: 2px solid #ff6600;
            border-radius: 0;
            padding: 8px 12px;
            box-shadow: 3px 3px 0 #802000;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton > button:hover {
            background: #ff6600;
            color: #000;
            box-shadow: 1px 1px 0 #802000;
            transform: translate(2px, 2px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0a0500 !important;
            color: #ff6600 !important;
            border: 2px solid #ff6600 !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            background: #0a0500 !important;
            border: 2px solid #ff6600 !important;
            border-radius: 0 !important;
        }
        .pixel-card {
            background: #0a0500;
            border: 3px solid #ff6600;
            box-shadow: 4px 4px 0 #802000;
            padding: 16px;
        }
        .lesson-why {
            background: #0a0500;
            border-left: 4px solid #ff6600;
            padding: 10px 14px;
            font-size: 7px !important;
            line-height: 2;
            box-shadow: 3px 3px 0 #400;
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #0a0000;
            border: 2px solid #ff3333;
            box-shadow: 3px 3px 0 #500;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-key_insight {
            background: #000a00;
            border: 2px solid #00ff00;
            box-shadow: 3px 3px 0 #050;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-watch_out {
            background: #0a0800;
            border: 2px solid #ffaa00;
            box-shadow: 3px 3px 0 #640;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .formula-box {
            background: #050300;
            border: 2px solid #ff6600;
            box-shadow: 4px 4px 0 #802000;
            padding: 14px;
            font-size: 7px !important; line-height: 2;
            color: #ff9900;
        }
        .reward-card {
            background: #0a0500;
            border: 3px solid #ff6600;
            box-shadow: 6px 6px 0 #802000;
            padding: 20px; text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #050300 !important;
            border-right: 3px solid #ff6600;
        }
        """,
    },

    # ── Stardew Farm ─────────────────────────────────────────────────────
    "stardew_theme": {
        "name": "Stardew Farm",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #2d4a1e;
            background-image:
                radial-gradient(circle, rgba(255,220,120,0.08) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        h1 { font-size: 12px !important; color: #ffe87a; letter-spacing: 2px;
             text-shadow: 2px 2px 0 #7a5c00; }
        h2 { font-size: 10px !important; color: #ffd54f; text-shadow: 2px 2px 0 #5a4000; }
        h3 { font-size: 8px  !important; color: #ffe099; }
        p, li, label, .stMarkdown { font-size: 8px !important; line-height: 2.2; color: #f5e6c8; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #5a3e1b;
            color: #ffe87a;
            border: 3px solid #8b6914;
            border-radius: 0;
            padding: 8px 14px;
            box-shadow: 4px 4px 0 #2a1a06, inset 0 1px 0 rgba(255,255,255,0.1);
        }
        .stButton > button:hover {
            background: #7a5520;
            box-shadow: 2px 2px 0 #2a1a06;
            transform: translate(2px, 2px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #1e3010 !important;
            color: #f5e6c8 !important;
            border: 3px solid #8b6914 !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            background: #1e3010 !important;
            border: 3px solid #8b6914 !important;
            border-radius: 0 !important;
        }
        .pixel-card {
            background: #1e3010;
            border: 4px solid #8b6914;
            box-shadow: 5px 5px 0 #0d1808, inset 0 0 0 1px rgba(255,220,120,0.1);
            padding: 16px;
        }
        .lesson-why {
            background: #1a2e0e;
            border-left: 4px solid #ffe87a;
            border-top: 2px solid #8b6914;
            padding: 10px 14px;
            font-size: 7px !important; line-height: 2.2;
            box-shadow: 3px 3px 0 #0a1406;
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #2a0e0e;
            border: 3px solid #e05252;
            box-shadow: 3px 3px 0 #600;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-key_insight {
            background: #0e2a0e;
            border: 3px solid #7acc5a;
            box-shadow: 3px 3px 0 #1a5a10;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-watch_out {
            background: #2a2006;
            border: 3px solid #ffd54f;
            box-shadow: 3px 3px 0 #7a5000;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .formula-box {
            background: #141e0a;
            border: 3px solid #8b6914;
            box-shadow: 4px 4px 0 #0d1406;
            padding: 14px;
            font-size: 7px !important; line-height: 2;
            color: #ffe099;
        }
        .reward-card {
            background: #1e3010;
            border: 4px solid #ffe87a;
            box-shadow: 6px 6px 0 #0d1406;
            padding: 20px; text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #182810 !important;
            border-right: 4px solid #8b6914;
        }
        """,
    },

    # ── Cherry Analyst ───────────────────────────────────────────────────
    "cherry_theme": {
        "name": "Cherry Analyst",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #1a0a14;
            background-image:
                radial-gradient(circle at 20% 50%, rgba(255,182,193,0.06) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255,105,135,0.06) 0%, transparent 50%);
        }
        h1 { font-size: 12px !important; color: #ff8fab; letter-spacing: 2px;
             text-shadow: 2px 2px 0 #7a0030; }
        h2 { font-size: 10px !important; color: #ffb3c6; text-shadow: 2px 2px 0 #5a0020; }
        h3 { font-size: 8px  !important; color: #ffc8d8; }
        p, li, label, .stMarkdown { font-size: 8px !important; line-height: 2.2; color: #ffe0eb; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #2a0a1a;
            color: #ff8fab;
            border: 2px solid #ff8fab;
            border-radius: 0;
            padding: 8px 14px;
            box-shadow: 3px 3px 0 #7a0030;
        }
        .stButton > button:hover {
            background: #ff8fab;
            color: #1a0a14;
            box-shadow: 1px 1px 0 #7a0030;
            transform: translate(2px, 2px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #150818 !important;
            color: #ffb3c6 !important;
            border: 2px solid #8b3050 !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            background: #150818 !important;
            border: 2px solid #8b3050 !important;
            border-radius: 0 !important;
        }
        .pixel-card {
            background: #1f0c18;
            border: 3px solid #ff8fab;
            box-shadow: 4px 4px 0 #7a0030;
            padding: 16px;
        }
        .lesson-why {
            background: #180a14;
            border-left: 4px solid #ff8fab;
            border-top: 2px solid #8b3050;
            padding: 10px 14px;
            font-size: 7px !important; line-height: 2.2;
            box-shadow: 3px 3px 0 #300010;
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #200808;
            border: 2px solid #ff5555;
            box-shadow: 3px 3px 0 #600;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-key_insight {
            background: #0a1a10;
            border: 2px solid #88cc99;
            box-shadow: 3px 3px 0 #205030;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-watch_out {
            background: #1a1008;
            border: 2px solid #ffcc77;
            box-shadow: 3px 3px 0 #7a4400;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .formula-box {
            background: #120810;
            border: 2px solid #8b3050;
            box-shadow: 4px 4px 0 #300010;
            padding: 14px;
            font-size: 7px !important; line-height: 2;
            color: #ffb3c6;
        }
        .reward-card {
            background: #1f0c18;
            border: 3px solid #ff8fab;
            box-shadow: 6px 6px 0 #7a0030;
            padding: 20px; text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #120810 !important;
            border-right: 3px solid #8b3050;
        }
        """,
    },

    # ── Midnight Terminal ─────────────────────────────────────────────────
    "midnight_theme": {
        "name": "Midnight Terminal",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #080010;
            background-image:
                linear-gradient(rgba(100,0,255,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(100,0,255,0.05) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        h1 { font-size: 12px !important; color: #00ffff;
             text-shadow: 0 0 8px #00ffff, 2px 2px 0 #004444; letter-spacing: 2px; }
        h2 { font-size: 10px !important; color: #aa55ff;
             text-shadow: 0 0 6px #aa55ff; letter-spacing: 1px; }
        h3 { font-size: 8px  !important; color: #cc88ff; }
        p, li, label, .stMarkdown { font-size: 8px !important; line-height: 2.2; color: #c8b8f0; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #080010;
            color: #00ffff;
            border: 2px solid #00ffff;
            border-radius: 0;
            padding: 8px 14px;
            box-shadow: 3px 3px 0 #004444, 0 0 8px rgba(0,255,255,0.2);
        }
        .stButton > button:hover {
            background: #00ffff;
            color: #080010;
            box-shadow: 1px 1px 0 #004444, 0 0 12px #00ffff;
            transform: translate(2px, 2px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #050008 !important;
            color: #00ffff !important;
            border: 2px solid #aa55ff !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            background: #050008 !important;
            border: 2px solid #aa55ff !important;
            border-radius: 0 !important;
        }
        .pixel-card {
            background: #0d0018;
            border: 3px solid #aa55ff;
            box-shadow: 4px 4px 0 #220044, 0 0 10px rgba(170,85,255,0.15);
            padding: 16px;
        }
        .lesson-why {
            background: #0a0015;
            border-left: 4px solid #00ffff;
            border-top: 2px solid #aa55ff;
            padding: 10px 14px;
            font-size: 7px !important; line-height: 2.2;
            box-shadow: 3px 3px 0 #110022, 0 0 8px rgba(0,255,255,0.1);
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #150005;
            border: 2px solid #ff4488;
            box-shadow: 3px 3px 0 #550022, 0 0 6px rgba(255,68,136,0.2);
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-key_insight {
            background: #001510;
            border: 2px solid #00ffbb;
            box-shadow: 3px 3px 0 #005544, 0 0 6px rgba(0,255,187,0.2);
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-watch_out {
            background: #120e00;
            border: 2px solid #ffcc00;
            box-shadow: 3px 3px 0 #554400, 0 0 6px rgba(255,204,0,0.2);
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .formula-box {
            background: #050008;
            border: 2px solid #aa55ff;
            box-shadow: 4px 4px 0 #220044, 0 0 8px rgba(170,85,255,0.15);
            padding: 14px;
            font-size: 7px !important; line-height: 2;
            color: #cc88ff;
        }
        .reward-card {
            background: #0d0018;
            border: 3px solid #00ffff;
            box-shadow: 6px 6px 0 #004444, 0 0 16px rgba(0,255,255,0.2);
            padding: 20px; text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #050008 !important;
            border-right: 3px solid #aa55ff;
        }
        """,
    },

    # ── Gold Tier ─────────────────────────────────────────────────────────
    "gold_theme": {
        "name": "Gold Tier",
        "css": """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        html, body, [class*="css"] {
            font-family: 'Press Start 2P', 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #080600;
            background-image:
                linear-gradient(rgba(200,160,0,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(200,160,0,0.04) 1px, transparent 1px);
            background-size: 24px 24px;
        }
        h1 { font-size: 12px !important; color: #ffd700;
             text-shadow: 2px 2px 0 #7a5c00, 0 0 8px rgba(255,215,0,0.3);
             letter-spacing: 2px; }
        h2 { font-size: 10px !important; color: #ffcc00;
             text-shadow: 2px 2px 0 #5a4000; }
        h3 { font-size: 8px  !important; color: #ffe566; }
        p, li, label, .stMarkdown { font-size: 8px !important; line-height: 2.2; color: #e8d888; }
        .stButton > button {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0f0c00;
            color: #ffd700;
            border: 2px solid #ffd700;
            border-radius: 0;
            padding: 8px 14px;
            box-shadow: 3px 3px 0 #5a3a00, 0 0 6px rgba(255,215,0,0.15);
        }
        .stButton > button:hover {
            background: #ffd700;
            color: #080600;
            box-shadow: 1px 1px 0 #5a3a00;
            transform: translate(2px, 2px);
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            font-family: 'Press Start 2P', monospace !important;
            font-size: 7px !important;
            background: #0a0800 !important;
            color: #ffd700 !important;
            border: 2px solid #7a5c00 !important;
            border-radius: 0 !important;
        }
        .stSelectbox > div > div {
            font-family: 'Press Start 2P', monospace !important;
            background: #0a0800 !important;
            border: 2px solid #7a5c00 !important;
            border-radius: 0 !important;
        }
        .pixel-card {
            background: #0f0c00;
            border: 3px solid #ffd700;
            box-shadow: 4px 4px 0 #3a2a00, 0 0 8px rgba(255,215,0,0.1);
            padding: 16px;
        }
        .lesson-why {
            background: #0a0800;
            border-left: 4px solid #ffd700;
            border-top: 2px solid #7a5c00;
            padding: 10px 14px;
            font-size: 7px !important; line-height: 2.2;
            box-shadow: 3px 3px 0 #1a1400;
            margin-bottom: 12px;
        }
        .callout-interview_trap {
            background: #150a00;
            border: 2px solid #ff8844;
            box-shadow: 3px 3px 0 #5a2000;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-key_insight {
            background: #081208;
            border: 2px solid #88cc44;
            box-shadow: 3px 3px 0 #204400;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .callout-watch_out {
            background: #0f0e00;
            border: 2px solid #ffd700;
            box-shadow: 3px 3px 0 #5a4400;
            padding: 10px 14px; margin: 8px 0;
            font-size: 7px !important; line-height: 2;
        }
        .formula-box {
            background: #080600;
            border: 2px solid #7a5c00;
            box-shadow: 4px 4px 0 #2a1a00;
            padding: 14px;
            font-size: 7px !important; line-height: 2;
            color: #ffe566;
        }
        .reward-card {
            background: #0f0c00;
            border: 3px solid #ffd700;
            box-shadow: 6px 6px 0 #3a2a00, 0 0 12px rgba(255,215,0,0.2);
            padding: 20px; text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #080600 !important;
            border-right: 3px solid #7a5c00;
        }
        """,
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def apply_theme(theme_id: str):
    theme = THEMES.get(theme_id, THEMES["default"])
    st.markdown(f"<style>{theme['css']}</style>", unsafe_allow_html=True)


def get_theme_name(theme_id: str) -> str:
    return THEMES.get(theme_id, THEMES["default"])["name"]


def all_theme_ids() -> list:
    return list(THEMES.keys())


def callout_html(variant: str, body: str) -> str:
    icons = {
        "interview_trap": "⚠ INTERVIEW TRAP",
        "key_insight":    "★ KEY INSIGHT",
        "watch_out":      "► WATCH OUT",
    }
    label = icons.get(variant, variant.upper())
    return f'<div class="callout-{variant}"><strong>{label}</strong><br><br>{body}</div>'


def formula_html(label: str, expression: str, note: str = "") -> str:
    note_html = f"<br><br><span style='opacity:0.7;font-size:6px'>{note}</span>" if note else ""
    return f'<div class="formula-box">[ {label} ]<br><br>{expression}{note_html}</div>'


def why_html(why: str, in_the_seat: str = "") -> str:
    seat_html = f'<br><br><span style="opacity:0.65;font-size:6px">► ON THE JOB: {in_the_seat}</span>' if in_the_seat else ""
    return f'<div class="lesson-why">★ {why}{seat_html}</div>'


def reward_card_html(title: str, body: str) -> str:
    return f'<div class="reward-card"><br>★ {title} ★<br><br><span style="font-size:7px">{body}</span><br></div>'


def mastery_badge(mastery: float) -> str:
    if mastery >= 90: return "★"
    elif mastery >= 70: return "◆"
    elif mastery >= 40: return "●"
    elif mastery > 0:  return "○"
    return "🔒"
