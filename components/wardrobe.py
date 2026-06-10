"""
Wardrobe UI — shown in the standing view.
Lets players browse, equip, and inspect clothing items.
"""
import streamlit as st
import storage
import gamification
from gamification import CLOTHING_ITEMS, CLOTHING_BY_ID, RARITY_BY_ID, MONOPOLIST_SET
from components.sprite_engine import img_tag


SLOT_ORDER = ["Jacket", "Shirt", "Accessory", "Pants", "Shoes"]
SLOT_ICONS = {"Jacket": "🧥", "Shirt": "👔", "Accessory": "👔", "Pants": "👖", "Shoes": "👟"}


def _rarity_badge(rarity_id: str) -> str:
    r = RARITY_BY_ID.get(rarity_id, {})
    color = r.get("color", "#888")
    label = r.get("label", rarity_id.title())
    return (
        f'<span style="background:{color}22;border:1px solid {color};'
        f'color:{color};padding:1px 7px;border-radius:3px;font-size:10px;'
        f'font-weight:700;white-space:nowrap">{label}</span>'
    )


def render_wardrobe(user: dict):
    st.markdown("## 👔 Wardrobe")
    st.caption("Equip clothing to boost XP and BPS earnings. Standing up unlocks the fitting room.")

    user_id = user["user_id"]
    owned   = set(storage.get_owned_clothing(user))
    outfit  = storage.get_equipped_outfit(user)

    # ── Currently equipped summary ────────────────────────────────────────
    st.markdown("### Equipped Outfit")
    boosters = gamification.calculate_outfit_boosters(user)
    st.markdown(
        f'<div style="font-size:13px;margin-bottom:8px">'
        f'Active boosts — XP ×<b>{boosters["xp_mult"]:.2f}</b> &nbsp; BPS ×<b>{boosters["bps_mult"]:.2f}</b>'
        f'</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(len(SLOT_ORDER))
    for i, slot in enumerate(SLOT_ORDER):
        with cols[i]:
            equipped_id = outfit.get(slot)
            item = CLOTHING_BY_ID.get(equipped_id)
            r    = RARITY_BY_ID.get(item["rarity"]) if item else None
            color = r["color"] if r else "#444"
            st.markdown(
                f'<div style="border:1px solid {color};border-radius:6px;padding:8px;'
                f'text-align:center;min-height:80px">'
                f'<div style="font-size:11px;opacity:0.55">{SLOT_ICONS.get(slot,"")} {slot}</div>'
                f'<div style="font-size:12px;font-weight:600;margin-top:4px">'
                f'{item["name"] if item else "—"}</div>'
                + (_rarity_badge(item["rarity"]) if item else "") +
                f'</div>',
                unsafe_allow_html=True
            )
            if equipped_id and st.button("Unequip", key=f"unequip_{slot}"):
                storage.equip_clothing_item(user_id, slot, None)
                st.rerun()

    # Monopolist badge
    if user.get("unlocked_monopolist"):
        st.markdown(
            '<div style="margin-top:8px;padding:10px;background:#1a0e00;'
            'border:1px solid #FF8F00;border-radius:6px;text-align:center">'
            '👑 <b style="color:#FF8F00">MONOPOLIST STATUS UNLOCKED</b> — '
            'All 5 Market Titan pieces equipped simultaneously.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Browse by slot ─────────────────────────────────────────────────────
    st.markdown("### Inventory")
    tab_labels = [f"{SLOT_ICONS.get(s,'')} {s}" for s in SLOT_ORDER] + ["🎁 All"]
    tabs = st.tabs(tab_labels)

    def _show_items(items_to_show, tab_key):
        if not items_to_show:
            st.caption("No items in this slot yet. Open Alpha Packs to find gear.")
            return
        for item in items_to_show:
            is_owned    = item["id"] in owned
            is_equipped = outfit.get(item["slot"]) == item["id"]
            r           = RARITY_BY_ID.get(item["rarity"], {})
            color       = r.get("color", "#888")
            opacity     = "1" if is_owned else "0.4"
            border      = f"2px solid {color}" if is_equipped else f"1px solid {color}44"

            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(
                        f'<div style="opacity:{opacity};border:{border};border-radius:6px;'
                        f'padding:8px 12px;margin-bottom:6px">'
                        f'<div style="font-weight:600;font-size:13px">{item["name"]} '
                        + _rarity_badge(item["rarity"]) +
                        f'</div><div style="font-size:12px;opacity:0.65;margin-top:2px">'
                        f'{item["desc"]}</div>'
                        f'<div style="font-size:11px;margin-top:4px;opacity:0.55">'
                        f'XP +{item["xp_booster"]*100:.0f}% &nbsp;·&nbsp; '
                        f'BPS +{item["bps_booster"]*100:.0f}% &nbsp;·&nbsp; '
                        f'Tier {item["tier"]}'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    if is_owned:
                        if is_equipped:
                            st.markdown(
                                f'<div style="color:{color};font-size:12px;padding-top:18px">✓ Equipped</div>',
                                unsafe_allow_html=True
                            )
                        else:
                            if st.button("Equip", key=f"equip_{tab_key}_{item['id']}"):
                                storage.equip_clothing_item(user_id, item["slot"], item["id"])
                                gamification._check_monopolist(user_id)
                                st.rerun()
                    else:
                        st.markdown(
                            '<div style="font-size:11px;opacity:0.4;padding-top:18px">🔒 Not owned</div>',
                            unsafe_allow_html=True
                        )

    for i, slot in enumerate(SLOT_ORDER):
        with tabs[i]:
            slot_items = [c for c in CLOTHING_ITEMS if c["slot"] == slot]
            _show_items(slot_items, f"slot{i}")

    with tabs[-1]:
        _show_items(CLOTHING_ITEMS, "all")
