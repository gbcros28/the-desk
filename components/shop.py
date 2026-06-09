"""bps shop — cosmetics and consumables."""
import streamlit as st
import gamification
import storage


def render_shop(user: dict):
    owned = gamification.get_owned_cosmetics(user)
    equipped = gamification.get_equipped(user)
    uid = user["user_id"]

    st.markdown(f"### Shop — you have **{user['bps']:,} bps**")
    st.caption("Earn bps by answering questions correctly. Spend them on cosmetics and power-ups.")

    for item in gamification.SHOP_ITEMS:
        is_owned = item["id"] in owned
        is_consumable = item["category"] == "consumable"
        is_equipped = equipped.get(item["category"]) == item["id"]

        cols = st.columns([3, 1, 1])
        with cols[0]:
            status = ""
            if is_owned and not is_consumable:
                status = " ✅ owned"
            if is_equipped:
                status = " ✨ equipped"
            st.markdown(f"**{item['name']}**{status}")
            st.caption(f"{item['description']} — {item['cost']} bps")
        with cols[1]:
            if (not is_owned or is_consumable) and not is_equipped:
                if st.button("Buy", key=f"buy_{item['id']}"):
                    ok, msg = gamification.buy_item(uid, item["id"])
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
                    st.rerun()
        with cols[2]:
            if is_owned and not is_consumable and not is_equipped:
                if st.button("Equip", key=f"equip_{item['id']}"):
                    gamification.equip_item(uid, item["id"])
                    st.success(f"Equipped {item['name']}.")
                    st.rerun()
        st.markdown("---")
