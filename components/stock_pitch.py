"""Stock pitch scaffold — saveable per-ticker template."""
import streamlit as st
import storage


def render_stock_pitch(user_id: int):
    st.markdown("## Stock Pitch Scaffold")
    st.caption("Build and save a pitch for any ticker. Thesis · Catalysts · Valuation · Risks · Variant View")

    pitches = storage.get_stock_pitches(user_id)
    tickers = [p["ticker"] for p in pitches]

    col1, col2 = st.columns([3, 1])
    with col1:
        ticker_input = st.text_input("Ticker", placeholder="e.g. AAPL, BRK.B").strip().upper()
    with col2:
        if tickers:
            selected = st.selectbox("Load saved", ["-- new --"] + tickers, key="pitch_select")
            if selected != "-- new --":
                ticker_input = selected

    if not ticker_input:
        if pitches:
            st.markdown("### Saved pitches")
            for p in pitches:
                st.markdown(f"**{p['ticker']}** — last updated {p['updated_at'][:10]}")
        return

    existing = storage.get_stock_pitch(user_id, ticker_input)

    thesis = st.text_area("Thesis", value=existing["thesis"] if existing else "", height=100,
                           placeholder="Why is this a good (or bad) investment?")
    catalysts = st.text_area("Catalysts", value=existing["catalysts"] if existing else "", height=80,
                              placeholder="What near-term events could move the stock?")
    valuation = st.text_area("Valuation", value=existing["valuation"] if existing else "", height=80,
                              placeholder="How are you thinking about price target / intrinsic value?")
    risks = st.text_area("Risks", value=existing["risks"] if existing else "", height=80,
                          placeholder="What could go wrong? What would make you wrong?")
    variant_view = st.text_area("Variant View", value=existing["variant_view"] if existing else "", height=80,
                                 placeholder="Where does the market have it wrong?")

    if st.button("💾 Save pitch"):
        storage.save_stock_pitch(user_id, ticker_input, thesis, catalysts, valuation, risks, variant_view)
        st.success(f"Pitch for {ticker_input} saved.")
        st.rerun()
