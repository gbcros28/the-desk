"""The Desk — entry point. Run with: streamlit run app.py"""
import streamlit as st
import storage
import content_loader
import gamification
import scheduler
from components.theme import apply_theme
from components.skill_tree import render_skill_tree, render_weak_spots
from components.lesson_view import render_lesson
from components.profile import render_profile
from components.shop import render_shop
from components.interview_sim import render_interview_sim
from components.jargon_deck import render_jargon_deck
from components.stock_pitch import render_stock_pitch
from components.content_upload import render_content_upload
from components.placement import render_placement, should_show_placement
from components.desk_scene import render_desk_scene
from components.calendar_view import render_calendar
from components.todo import render_todo

st.set_page_config(page_title="The Desk", page_icon="📊", layout="wide",
                   initial_sidebar_state="collapsed")

# ── Init ──────────────────────────────────────────────────────────────────
storage.init_db()

if "lessons" not in st.session_state:
    try:
        lessons   = content_loader.load_all_lessons()
        track_tree = content_loader.build_track_tree(lessons)
        jargon    = content_loader.load_jargon()
        st.session_state["lessons"]    = lessons
        st.session_state["track_tree"] = track_tree
        st.session_state["jargon"]     = jargon
    except content_loader.ContentError as e:
        st.error(f"**Content error — fix before continuing:**\n\n```\n{e}\n```")
        st.stop()

lessons    = st.session_state["lessons"]
track_tree = st.session_state["track_tree"]
jargon     = st.session_state["jargon"]

# ── Login ─────────────────────────────────────────────────────────────────
if "user_id" not in st.session_state:
    apply_theme("default")
    st.title("The Desk")
    st.caption("Asset management recruiting — structured, offline, self-paced.")
    st.markdown("---")

    users = storage.get_all_users()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Sign in")
        if users:
            names    = [u["name"] for u in users]
            selected = st.selectbox("Profile", names, label_visibility="collapsed")
            if st.button("Continue →"):
                user = storage.get_user_by_name(selected)
                st.session_state["user_id"] = user["user_id"]
                st.rerun()
        else:
            st.caption("No profiles yet.")

    with col2:
        st.markdown("#### New profile")
        new_name = st.text_input("Name", label_visibility="collapsed",
                                 placeholder="Your name")
        if st.button("Create →"):
            if not new_name.strip():
                st.warning("Enter a name.")
            elif storage.get_user_by_name(new_name.strip()):
                st.warning("Name already taken.")
            else:
                user = storage.create_user(new_name.strip())
                st.session_state["user_id"]   = user["user_id"]
                st.session_state["new_user"]  = True
                st.rerun()
    st.stop()

# ── Logged in ─────────────────────────────────────────────────────────────
user_id = st.session_state["user_id"]
user    = storage.get_user(user_id)
if not user:
    del st.session_state["user_id"]
    st.rerun()

storage.record_streak(user_id)
user  = storage.get_user(user_id)
theme = gamification.get_active_theme(user)
apply_theme(theme)

# ── Placement diagnostic (new users) ─────────────────────────────────────
if should_show_placement(user_id):
    render_placement(lessons, user_id)
    st.stop()

# ── Top bar ───────────────────────────────────────────────────────────────
due = scheduler.get_due_count(user_id)

col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown(
        f'<div class="desk-topbar">'
        f'<div class="desk-user-info">'
        f'<strong>{user["name"]}</strong> &nbsp;·&nbsp; {user["title"]}'
        f' &nbsp;·&nbsp; Level {user["level"]}'
        f' &nbsp;·&nbsp; {user["xp"]:,} XP'
        f' &nbsp;·&nbsp; {user["bps"]:,} bps'
        f' &nbsp;·&nbsp; 🔥 {user["streak"]}'
        + (f' &nbsp;·&nbsp; <span style="color:#4a8fe8">{due} due</span>' if due > 0 else '')
        + f'</div></div>',
        unsafe_allow_html=True
    )
with col_right:
    if st.button("Switch profile", key="switch_profile"):
        del st.session_state["user_id"]
        st.rerun()

# ── Navigation — grouped tabs ─────────────────────────────────────────────
# Tab groups: Learn | Practice | Tools | Profile
tab_learn, tab_practice, tab_tools, tab_me = st.tabs([
    "📚  Learn",
    "🎯  Practice",
    "🔧  Tools",
    "👤  Me",
])

# ── Learn tab ─────────────────────────────────────────────────────────────
with tab_learn:
    active_lesson = st.session_state.get("active_lesson")

    if active_lesson and active_lesson in lessons:
        if st.button("← Back to skill tree"):
            del st.session_state["active_lesson"]
            st.rerun()
        render_lesson(lessons[active_lesson], user_id)
    else:
        render_skill_tree(track_tree, user_id, lessons)

# ── Practice tab ──────────────────────────────────────────────────────────
with tab_practice:
    sub_review, sub_interview, sub_weak = st.tabs([
        f"Daily Review{'  ·  ' + str(due) + ' due' if due > 0 else ''}",
        "Interview Sim",
        "Weak Spots",
    ])

    with sub_review:
        due_cards = storage.get_due_cards(user_id)
        if not due_cards:
            st.success("You're all caught up — nothing due today.")
            from rewards import get_reward_card
            from components.theme import reward_card_html
            card = get_reward_card("review_clear")
            st.markdown(reward_card_html(card["title"], card["body"]),
                        unsafe_allow_html=True)
        else:
            lesson_ids = list({c["lesson_id"] for c in due_cards})
            st.markdown(f"**{len(due_cards)} card{'s' if len(due_cards) > 1 else ''} due** across {len(lesson_ids)} lesson{'s' if len(lesson_ids) > 1 else ''}")
            st.markdown("---")
            for lid in lesson_ids:
                if lid in lessons:
                    st.markdown(f"### {lessons[lid]['title']}")
                    render_lesson(lessons[lid], user_id)

    with sub_interview:
        render_interview_sim(lessons, user_id)

    with sub_weak:
        render_weak_spots(user_id, lessons)

# ── Tools tab ─────────────────────────────────────────────────────────────
with tab_tools:
    sub_jargon, sub_pitch, sub_cal, sub_todo = st.tabs([
        "Jargon Deck",
        "Stock Pitch",
        "Calendar",
        "To-Do",
    ])

    with sub_jargon:
        render_jargon_deck(jargon)

    with sub_pitch:
        render_stock_pitch(user_id)

    with sub_cal:
        render_calendar(user_id, lessons)

    with sub_todo:
        render_todo(user_id)

# ── Me tab ────────────────────────────────────────────────────────────────
with tab_me:
    sub_profile, sub_shop, sub_upload = st.tabs([
        "Profile",
        "Shop",
        "Add Content",
    ])

    with sub_profile:
        render_desk_scene(user)
        st.markdown("---")
        render_profile(user)

    with sub_shop:
        render_shop(user)

    with sub_upload:
        render_content_upload()
