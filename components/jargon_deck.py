"""Searchable, always-accessible jargon reference."""
import streamlit as st


def render_jargon_deck(terms: list):
    st.markdown("## Jargon Deck")
    st.caption("Quick reference for finance terms. Not gated — always available.")

    if not terms:
        st.info("No terms yet. Add a jargon.json to content/ to populate this.")
        return

    search = st.text_input("Search terms", placeholder="e.g. EBITDA, beta, covenant…")
    filtered = terms
    if search:
        q = search.lower()
        filtered = [t for t in terms if q in t["term"].lower() or q in t["definition"].lower()]

    if not filtered:
        st.warning("No matching terms.")
        return

    for t in sorted(filtered, key=lambda x: x["term"].lower()):
        track_tag = f" `{t['track']}`" if t.get("track") else ""
        st.markdown(f"**{t['term']}**{track_tag}  \n{t['definition']}")
        st.markdown("---")
