"""bps shop — cosmetics, consumables, and themes."""
import streamlit as st
import gamification
import storage
from components.theme import get_theme_name, THEMES


def render_shop(user: dict):
    owned = gamification.get_owned_cosmetics(user)
    equipped = gamification.get_equipped(user)
    uid = user["user_id"]
    active_theme = equipped.get("theme", "default")

    st.markdown("## [ SHOP ]")
    st.markdown(f"You have **{user['bps']:,} bps** to spend.")
    st.caption("Earn bps by answering questions correctly.")
    st.markdown("---")

    # Group by category
    categories = [
        ("consumable", "⚡ POWER-UPS"),
        ("cosmetic",   "🖥 DESK ITEMS"),
        ("theme",      "🎨 THEMES"),
    ]

    for cat_key, cat_label in categories:
        items = [i for i in gamification.SHOP_ITEMS if i["category"] == cat_key]
        st.markdown(f"### {cat_label}")

        for item in items:
            is_owned = item["id"] in owned
            is_consumable = item["category"] == "consumable"
            is_active_theme = item["id"] == active_theme
            is_equipped_cosmetic = equipped.get("cosmetic") == item["id"]
            can_afford = user["bps"] >= item["cost"]

            # Theme preview swatch
            theme_preview = ""
            if cat_key == "theme" and item["id"] in THEMES:
                theme_css = THEMES[item["id"]]
                colors = {
                    "bloomberg_theme": ["#000", "#ff6600", "#ff9900"],
                    "stardew_theme":   ["#2d4a1e", "#ffe87a", "#8b6914"],
                    "cherry_theme":    ["#1a0a14", "#ff8fab", "#8b3050"],
                    "midnight_theme":  ["#080010", "#00ffff", "#aa55ff"],
                    "gold_theme":      ["#080600", "#ffd700", "#7a5c00"],
                    "default":         ["#0d1117", "#4a90d9", "#1e2d4a"],
                }.get(item["id"], ["#111", "#888", "#444"])
                swatches = "".join(
                    f'<span style="display:inline-block;width:14px;height:14px;background:{c};'
                    f'border:1px solid #333;margin-right:2px;"></span>' for c in colors
                )
                theme_preview = f'<span style="vertical-align:middle;">{swatches}</span>'

            # Build row
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                status = ""
                if is_active_theme:
                    status = " ✨ ACTIVE"
                elif is_equipped_cosmetic:
                    status = " ✨ EQUIPPED"
                elif is_owned and not is_consumable:
                    status = " ✓ OWNED"

                emoji = item.get("emoji", "")
                st.markdown(
                    f"**{emoji} {item['name']}**{status}"
                    + (f"  {theme_preview}" if theme_preview else ""),
                    unsafe_allow_html=True
                )
                cost_color = "#4a90d9" if can_afford else "#e05252"
                st.markdown(
                    f'<span style="font-size:7px;color:{cost_color}">{item["cost"]} bps</span>'
                    f'<span style="font-size:7px;color:#888"> — {item["description"]}</span>',
                    unsafe_allow_html=True
                )

            with col2:
                if not is_owned or is_consumable:
                    if not is_active_theme:
                        btn_label = "BUY" if can_afford else "···"
                        if st.button(btn_label, key=f"buy_{item['id']}", disabled=not can_afford):
                            ok, msg = gamification.buy_item(uid, item["id"])
                            if ok:
                                st.success(msg)
                            else:
                                st.error(msg)
                            st.rerun()

            with col3:
                # Equip button for owned non-consumables
                if is_owned and not is_consumable and not is_active_theme and not is_equipped_cosmetic:
                    if st.button("EQUIP", key=f"equip_{item['id']}"):
                        gamification.equip_item(uid, item["id"])
                        st.success(f"Equipped {item['name']}.")
                        st.rerun()

            st.markdown('<hr style="border-color:#1e2230;margin:6px 0">', unsafe_allow_html=True)

        st.markdown("")
