"""Alpha Pack loot box — buy, spin, reveal."""
import streamlit as st
import json
import gamification
import storage
from gamification import ALPHA_PACK_COST, RARITY_BY_ID


def render_alpha_pack(user: dict):
    st.markdown("## 🎁 Alpha Packs")
    st.caption(
        f"Each pack costs **{ALPHA_PACK_COST} bps** and contains one random clothing item. "
        "Higher tiers are rare but grant significant XP and BPS multipliers."
    )

    user_id = user["user_id"]
    bps     = user.get("bps", 0)

    # ── Drop rate table ────────────────────────────────────────────────────
    with st.expander("📊 Drop rates"):
        for r in gamification.RARITY_TIERS:
            color = r["color"]
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'padding:4px 8px;border-left:3px solid {color};margin-bottom:4px">'
                f'<span style="color:{color};font-weight:600">{r["label"]}</span>'
                f'<span style="opacity:0.7">{r["name"]}</span>'
                f'<span>{r["weight"]}%</span>'
                f'<span>+{r["booster"]*100:.0f}% XP & BPS</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Open pack ─────────────────────────────────────────────────────────
    col_btn, col_bal = st.columns([2, 3])
    with col_btn:
        can_open = bps >= ALPHA_PACK_COST
        if st.button(
            f"🎁 Open Alpha Pack — {ALPHA_PACK_COST} bps",
            disabled=not can_open,
            use_container_width=True,
            type="primary",
        ):
            result = gamification.roll_alpha_pack(user_id)
            if result["success"]:
                st.session_state["last_pack_result"] = result
            else:
                st.error(result["error"])
            st.rerun()

    with col_bal:
        st.markdown(
            f'<div style="padding:8px 12px;background:#0d1420;border-radius:6px;'
            f'font-size:13px">Balance: <b>{bps:,} bps</b> '
            + (f'— can open <b>{bps // ALPHA_PACK_COST}</b> pack(s)' if can_open else '— <span style="color:#f44336">insufficient</span>')
            + '</div>',
            unsafe_allow_html=True,
        )

    # ── Spin ticker (show result from previous run) ────────────────────────
    result = st.session_state.get("last_pack_result")
    if result and result.get("success"):
        _render_result(result)

    # ── Pack history ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recent Pulls")
    conn = storage._get_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT item_id, rarity, bps_spent, rolled_at FROM alpha_pack_log "
        "WHERE user_id=? ORDER BY rolled_at DESC LIMIT 20",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    if not rows:
        st.caption("No packs opened yet.")
    else:
        for row in rows:
            item = gamification.CLOTHING_BY_ID.get(row[0])
            r    = RARITY_BY_ID.get(row[1], {})
            color = r.get("color", "#888")
            name  = item["name"] if item else row[0]
            st.markdown(
                f'<div style="border-left:3px solid {color};padding:3px 8px;'
                f'margin-bottom:3px;font-size:12px">'
                f'<span style="color:{color};font-weight:600">{r.get("label","?")}</span> '
                f'— {name} <span style="opacity:0.45;font-size:11px">{row[3][:10]}</span></div>',
                unsafe_allow_html=True
            )


def _render_result(result: dict):
    item   = result["item"]
    rarity = result["rarity"]
    color  = rarity["color"]
    spin   = result["spin_items"]  # 21 items, winner last

    st.markdown("---")
    st.markdown("### 🎰 Result")

    # Spin ticker strip — CSS animation showing items scrolling to winner
    spin_html = ""
    for i, s in enumerate(spin):
        sc = RARITY_BY_ID.get(s["rarity"], {}).get("color", "#888")
        is_winner = (i == len(spin) - 1)
        border = f"2px solid {sc}" if is_winner else f"1px solid {sc}44"
        bg = f"{sc}22" if is_winner else "transparent"
        spin_html += (
            f'<div style="flex:0 0 120px;border:{border};background:{bg};'
            f'border-radius:4px;padding:6px 4px;text-align:center;'
            f'{"transform:scale(1.1);box-shadow:0 0 12px " + sc + "88" if is_winner else ""}">'
            f'<div style="font-size:10px;color:{sc};font-weight:600">'
            f'{RARITY_BY_ID.get(s["rarity"],{}).get("label","?")}</div>'
            f'<div style="font-size:11px;margin-top:4px;word-break:break-word">{s["name"]}</div>'
            f'</div>'
        )

    st.markdown(
        f'<div style="overflow-x:auto;padding:8px 0">'
        f'<div style="display:flex;gap:6px;width:max-content">'
        + spin_html +
        f'</div></div>',
        unsafe_allow_html=True
    )

    # Winner callout
    st.markdown(
        f'<div style="margin-top:16px;padding:16px;background:{color}15;'
        f'border:2px solid {color};border-radius:8px;text-align:center">'
        f'<div style="font-size:20px;font-weight:700;color:{color}">'
        f'{rarity["label"].upper()} PULL!</div>'
        f'<div style="font-size:18px;font-weight:600;margin-top:8px">{item["name"]}</div>'
        f'<div style="font-size:13px;opacity:0.65;margin-top:4px">{item["desc"]}</div>'
        f'<div style="font-size:12px;margin-top:8px">'
        f'XP +{item["xp_booster"]*100:.0f}% · BPS +{item["bps_booster"]*100:.0f}%</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("Close", key="close_pack_result"):
        del st.session_state["last_pack_result"]
        st.rerun()
