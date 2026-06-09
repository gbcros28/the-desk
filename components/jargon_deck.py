"""Searchable jargon reference. Handles both schema shapes."""
import streamlit as st


def render_jargon_deck(terms: list):
    st.markdown("## Jargon Deck")
    st.caption("Finance terms everyone assumes you already know. Always accessible, never gated.")

    if not terms:
        st.info("No terms yet. Add content/jargon.json to populate this.")
        return

    search = st.text_input("Search", placeholder="dry powder, carry, print, tape…",
                            label_visibility="collapsed")
    filtered = terms
    if search:
        q = search.lower()
        filtered = [
            t for t in terms
            if q in t.get("term", "").lower()
            or q in t.get("definition", "").lower()
            or q in t.get("plain", "").lower()
            or q in t.get("in_context", "").lower()
        ]

    if not filtered:
        st.warning("No matching terms.")
        return

    st.caption(f"{len(filtered)} term{'s' if len(filtered) != 1 else ''}")
    st.markdown("---")

    for t in sorted(filtered, key=lambda x: x.get("term", "").lower()):
        # Support both schema shapes:
        # Old: {term, definition, track}
        # New: {term, plain, in_context, tags}
        definition  = t.get("plain") or t.get("definition") or ""
        in_context  = t.get("in_context", "")
        track_tag   = t.get("track", "")
        tags        = t.get("tags", [])

        tag_str = ""
        if track_tag:
            tag_str = f' <span style="font-size:11px;opacity:0.5">{track_tag}</span>'
        elif tags:
            tag_str = " " + " ".join(
                f'<span style="font-size:11px;opacity:0.5">{tg}</span>'
                for tg in tags[:3]
            )

        st.markdown(
            f'<div style="margin-bottom:16px">'
            f'<div style="font-weight:600;font-size:15px">{t["term"]}{tag_str}</div>'
            f'<div style="font-size:14px;margin-top:3px">{definition}</div>'
            + (f'<div style="font-size:13px;opacity:0.55;margin-top:4px;font-style:italic">{in_context}</div>'
               if in_context else "")
            + f'</div>',
            unsafe_allow_html=True
        )
