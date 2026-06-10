"""
Office environment — composite sprite scene + HUD.
Replaces the SVG pixel-art desk_scene for the main game view.
"""
import streamlit as st
import storage
import gamification
from components.sprite_engine import composite_html, img_tag, _img_b64

# ── Office tier config ─────────────────────────────────────────────────────
OFFICE_CFG = {
    1: {"bg_file": "office_tier1.png", "desk_file": "desk_tier1.png",
        "chair_file": "chair_tier1.png", "name": "Cubicle",
        "accent": "#4a8fe8"},
    2: {"bg_file": "office_tier2.png", "desk_file": "desk_tier2.png",
        "chair_file": "chair_tier2.png", "name": "Shared Office",
        "accent": "#8ab44a"},
    3: {"bg_file": "office_tier3.png", "desk_file": "desk_tier3.png",
        "chair_file": "chair_tier3.png", "name": "Corner Office",
        "accent": "#c8a428"},
    4: {"bg_file": "office_tier4.png", "desk_file": "desk_tier4.png",
        "chair_file": "chair_tier4.png", "name": "Penthouse Suite",
        "accent": "#FF8F00"},
}

# Scene dimensions (CSS px, responsive via max-width)
SCENE_W = 700
SCENE_H = 380


def render_office_view(user: dict):
    """Main office scene with HUD — called from the Profile tab."""
    tier      = user.get("office_tier", 1)
    is_sitting = bool(user.get("is_sitting", 1))
    mc        = user.get("mental_capital", 100)
    gender    = user.get("gender", "man")
    cfg       = OFFICE_CFG.get(tier, OFFICE_CFG[1])

    # ── Mental Capital tick ───────────────────────────────────────────────
    storage.tick_mental_capital(user["user_id"])
    user = storage.get_user(user["user_id"])  # refresh
    mc   = user.get("mental_capital", 100)

    # ── HUD bar ───────────────────────────────────────────────────────────
    accent = cfg["accent"]
    mc_pct = mc
    mc_color = "#4caf50" if mc > 60 else "#ff9800" if mc > 30 else "#f44336"
    boosters = gamification.calculate_outfit_boosters(user)
    xp_mult  = boosters["xp_mult"]
    bps_mult = boosters["bps_mult"]

    st.markdown(
        f"""
        <div style="display:flex;gap:16px;align-items:center;padding:10px 16px;
                    background:#0d1420;border:1px solid {accent}44;border-radius:8px;
                    margin-bottom:12px;flex-wrap:wrap">
          <div>
            <div style="font-size:11px;opacity:0.5;text-transform:uppercase;
                        letter-spacing:1px">Mental Capital</div>
            <div style="background:#1a2030;border-radius:4px;height:10px;width:140px;margin-top:4px">
              <div style="background:{mc_color};width:{mc_pct}%;height:10px;border-radius:4px;
                          transition:width .4s"></div>
            </div>
            <div style="font-size:12px;margin-top:2px;color:{mc_color}">{mc}/100</div>
          </div>
          <div style="border-left:1px solid #ffffff22;padding-left:16px">
            <div style="font-size:11px;opacity:0.5;text-transform:uppercase;letter-spacing:1px">Office</div>
            <div style="font-size:14px;font-weight:600;color:{accent}">{cfg['name']}</div>
          </div>
          <div style="border-left:1px solid #ffffff22;padding-left:16px">
            <div style="font-size:11px;opacity:0.5;text-transform:uppercase;letter-spacing:1px">Outfit Boost</div>
            <div style="font-size:13px">XP ×{xp_mult:.2f} &nbsp; BPS ×{bps_mult:.2f}</div>
          </div>
          <div style="margin-left:auto;display:flex;gap:8px">
            {'<span style="background:#1a1a2e;border:1px solid #FF8F00;padding:3px 8px;border-radius:4px;font-size:11px;color:#FF8F00">👑 MONOPOLIST</span>' if user.get('unlocked_monopolist') else ''}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Scene composite ───────────────────────────────────────────────────
    char_file = "character_seated.png" if is_sitting else (
        "char_man_stand.png" if gender == "man" else "char_woman_stand.png"
    )

    # Build layer stack
    layers = [
        # Background room (fills container)
        {"file": cfg["bg_file"],    "left": 0,   "top": 0,   "width": f"{SCENE_W}px", "z": 1},
        # Desk — positioned bottom-center
        {"file": cfg["desk_file"],  "left": 200, "top": 170, "width": "320px",        "z": 3},
        # Chair — behind desk, behind character
        {"file": cfg["chair_file"], "left": 260, "top": 180, "width": "180px",        "z": 2},
        # Character
        {"file": char_file,         "left": 255, "top": 110, "width": "200px",        "z": 4,
         "extra_style": "image-rendering:auto"},
    ]

    scene = composite_html(
        layers,
        container_style=f"width:100%;max-width:{SCENE_W}px;height:{SCENE_H}px;"
                        f"background:#111;border-radius:8px;overflow:hidden;"
                        f"border:2px solid {accent}55;"
    )

    # ── Name plate overlay ────────────────────────────────────────────────
    name_plate = (
        f'<div style="text-align:center;margin-top:6px;font-size:13px;'
        f'color:{accent};font-weight:600">'
        f'{user["name"]} · {user.get("title","Intern")} · Lv {user.get("level",1)}'
        f' · {user.get("xp",0):,} XP · {user.get("bps",0):,} bps'
        f'</div>'
    )

    st.markdown(scene + name_plate, unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────────────
    col_sit, col_gender, col_coffee = st.columns(3)

    with col_sit:
        sit_label = "🧍 Stand Up" if is_sitting else "💺 Sit Down"
        if st.button(sit_label, use_container_width=True):
            storage.update_user(user["user_id"], is_sitting=0 if is_sitting else 1)
            st.rerun()

    with col_gender:
        g_label = "♀ Switch to Woman" if gender == "man" else "♂ Switch to Man"
        if st.button(g_label, use_container_width=True):
            new_g = "woman" if gender == "man" else "man"
            storage.update_user(user["user_id"], gender=new_g)
            st.rerun()

    with col_coffee:
        coffee_cost = 50
        if st.button(f"☕ Buy Coffee (+50 MC) · {coffee_cost} bps", use_container_width=True):
            if storage.spend_bps(user["user_id"], coffee_cost):
                new_mc = storage.restore_mental_capital(user["user_id"], 50)
                st.success(f"Mental capital restored to {new_mc}/100.")
                st.rerun()
            else:
                st.error(f"Need {coffee_cost} bps.")

    # ── Mental capital warning ────────────────────────────────────────────
    if mc == 0:
        st.error("**Mental capital depleted.** Buy a coffee or wait for it to recover (+5 every 15 min) before starting new lessons.")
    elif mc <= 30:
        st.warning(f"⚠️ Mental capital low ({mc}/100). Consider a coffee break.")

    # ── Office upgrade ────────────────────────────────────────────────────
    with st.expander("🏢 Upgrade Office"):
        for t, info in gamification.OFFICE_TIERS.items():
            if t <= tier:
                st.markdown(
                    f'<span style="opacity:0.5">✓ {info["name"]} (owned)</span>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'**{info["name"]}** — {info["cost"]:,} bps · {info["xp_req"]:,} XP required'
                )
                if st.button(f"Upgrade to {info['name']}", key=f"upgrade_{t}"):
                    ok, msg = gamification.upgrade_office(user["user_id"], t)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                break  # only show next tier
