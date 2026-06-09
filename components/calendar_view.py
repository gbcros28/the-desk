"""Calendar — shows streak days, review due dates, and custom events."""
import calendar
import streamlit as st
import storage
from datetime import date, timedelta


def render_calendar(user_id: int, lessons: dict = None):
    st.markdown("## Calendar")

    today = date.today()
    # Month navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if "cal_year" not in st.session_state:
            st.session_state["cal_year"] = today.year
        if "cal_month" not in st.session_state:
            st.session_state["cal_month"] = today.month

    with col1:
        if st.button("◀ Prev"):
            m = st.session_state["cal_month"] - 1
            y = st.session_state["cal_year"]
            if m < 1:
                m = 12
                y -= 1
            st.session_state["cal_month"] = m
            st.session_state["cal_year"] = y
            st.rerun()
    with col2:
        st.markdown(f"<h4 style='text-align:center'>{calendar.month_name[st.session_state['cal_month']]} {st.session_state['cal_year']}</h4>",
                    unsafe_allow_html=True)
    with col3:
        if st.button("Next ▶"):
            m = st.session_state["cal_month"] + 1
            y = st.session_state["cal_year"]
            if m > 12:
                m = 1
                y += 1
            st.session_state["cal_month"] = m
            st.session_state["cal_year"] = y
            st.rerun()

    year = st.session_state["cal_year"]
    month = st.session_state["cal_month"]

    # Data
    streak_days = storage.get_streak_log(user_id, year, month)
    events = storage.get_calendar_events(user_id, year, month)
    todos = storage.get_todos(user_id, include_done=False)

    # Map events and todos to dates
    event_map = {}
    for e in events:
        d = e["event_date"][:10]
        event_map.setdefault(d, []).append(("event", e["title"]))
    for t in todos:
        if t["due_date"]:
            d = t["due_date"][:10]
            event_map.setdefault(d, []).append(("todo", t["text"]))

    # Due review cards — group by lesson
    due_cards = storage.get_due_cards(user_id)
    due_dates_set = set()
    for card in due_cards:
        if card.get("due_date"):
            due_dates_set.add(card["due_date"][:10])

    # Render calendar grid
    cal = calendar.monthcalendar(year, month)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, d in enumerate(day_names):
        cols[i].markdown(f"<div style='text-align:center;font-size:11px;color:#888;'>{d}</div>",
                         unsafe_allow_html=True)

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].markdown("")
                continue
            day_str = f"{year}-{month:02d}-{day:02d}"
            is_today = (year == today.year and month == today.month and day == today.day)
            is_streak = day_str in streak_days
            has_review = day_str in due_dates_set
            has_events = day_str in event_map

            # Build cell style
            bg = "#1a3a1a" if is_streak else ("#1a2233" if is_today else "transparent")
            border = "2px solid #4a90d9" if is_today else "1px solid #2a3450" if is_streak else "1px solid #1e2230"
            indicators = ""
            if is_streak:
                indicators += "🔥"
            if has_review:
                indicators += "📚"
            if has_events:
                indicators += "📌"

            cell_html = f"""<div style="background:{bg};border:{border};border-radius:6px;
                padding:4px;text-align:center;min-height:52px;cursor:default;">
                <div style="font-size:13px;font-weight:{'bold' if is_today else 'normal'};
                color:{'#4a90d9' if is_today else '#ccc'};">{day}</div>
                <div style="font-size:11px;line-height:1.2;">{indicators}</div>
            </div>"""
            cols[i].markdown(cell_html, unsafe_allow_html=True)

    # Legend
    st.markdown("")
    st.markdown("🔥 streak day &nbsp;&nbsp; 📚 review due &nbsp;&nbsp; 📌 event/task", unsafe_allow_html=True)

    # Events list for this month
    if event_map:
        st.markdown("---")
        st.markdown("#### This month")
        for day_str in sorted(event_map.keys()):
            for kind, title in event_map[day_str]:
                icon = "📌" if kind == "event" else "✅"
                st.markdown(f"{icon} **{day_str}** — {title}")

    # --- Add event ---
    st.markdown("---")
    with st.expander("➕ Add calendar event"):
        with st.form("add_event_form", clear_on_submit=True):
            title = st.text_input("Event title", placeholder="e.g. Mock interview, recruiting deadline…")
            event_date = st.date_input("Date", value=today)
            note = st.text_input("Note (optional)")
            if st.form_submit_button("Add event"):
                if title.strip():
                    storage.add_calendar_event(user_id, title.strip(), str(event_date), note)
                    st.success("Event added.")
                    st.rerun()

    # --- Upcoming events (next 30 days) ---
    all_events = storage.get_all_calendar_events(user_id)
    upcoming = [e for e in all_events
                if today <= date.fromisoformat(e["event_date"][:10]) <= today + timedelta(days=30)]
    if upcoming:
        st.markdown("---")
        st.markdown("#### Upcoming (next 30 days)")
        for e in upcoming:
            col1, col2 = st.columns([8, 1])
            with col1:
                days_away = (date.fromisoformat(e["event_date"][:10]) - today).days
                label = "today" if days_away == 0 else f"in {days_away}d"
                st.markdown(f"📅 **{e['title']}** — {e['event_date'][:10]} *({label})*")
                if e.get("note"):
                    st.caption(e["note"])
            with col2:
                if st.button("🗑", key=f"del_event_{e['id']}"):
                    storage.delete_calendar_event(e["id"], user_id)
                    st.rerun()
