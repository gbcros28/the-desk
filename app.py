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

st.set_page_config(page_title="The Desk", page_icon="📊", layout="wide")

# --- Init DB ---
storage.init_db()

# --- Load content (cached in session) ---
if "lessons" not in st.session_state or "track_tree" not in st.session_state:
    try:
        lessons = content_loader.load_all_lessons()
        track_tree = content_loader.build_track_tree(lessons)
        jargon = content_loader.load_jargon()
        st.session_state["lessons"] = lessons
        st.session_state["track_tree"] = track_tree
        st.session_state["jargon"] = jargon
    except content_loader.ContentError as e:
        st.error(f"**Content error — fix this before continuing:**\n\n```\n{e}\n```")
        st.stop()

lessons = st.session_state["lessons"]
track_tree = st.session_state["track_tree"]
jargon = st.session_state["jargon"]

# --- User selection / creation ---
if "user_id" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state.get("page") == "login" or "user_id" not in st.session_state:
    st.title("📊 The Desk")
    st.markdown("Asset management recruiting, one rep at a time.")
    st.markdown("---")

    users = storage.get_all_users()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Select profile")
        if users:
            names = [u["name"] for u in users]
            selected = st.selectbox("Existing profiles", names)
            if st.button("Continue"):
                user = storage.get_user_by_name(selected)
                st.session_state["user_id"] = user["user_id"]
                st.session_state["page"] = "tree"
                st.rerun()
        else:
            st.info("No profiles yet. Create one →")

    with col2:
        st.markdown("### New profile")
        new_name = st.text_input("Your name")
        if st.button("Create profile"):
            if not new_name.strip():
                st.warning("Enter a name.")
            elif storage.get_user_by_name(new_name.strip()):
                st.warning("Name already taken.")
            else:
                user = storage.create_user(new_name.strip())
                st.session_state["user_id"] = user["user_id"]
                st.session_state["page"] = "placement"
                st.rerun()
    st.stop()

# --- Logged in ---
user_id = st.session_state["user_id"]
user = storage.get_user(user_id)
if not user:
    del st.session_state["user_id"]
    st.rerun()

storage.record_streak(user_id)
user = storage.get_user(user_id)  # refresh after streak update

# Apply theme
theme = gamification.get_active_theme(user)
apply_theme(theme)

# --- Top nav bar ---
page = st.session_state.get("page", "tree")
due  = scheduler.get_due_count(user_id)

NAV_PAGES = [
    ("tree",      "SKILLS"),
    ("review",    f"REVIEW{'  !' if due > 0 else ''}"),
    ("interview", "MOCK INT"),
    ("weak",      "WEAK SPOTS"),
    ("jargon",    "JARGON"),
    ("pitch",     "PITCH"),
    ("calendar",  "CALENDAR"),
    ("todo",      "TO-DO"),
    ("profile",   "PROFILE"),
    ("shop",      "SHOP"),
    ("upload",    "+ CONTENT"),
]

# Render nav as clickable Streamlit buttons styled like boxes
st.markdown(
    f"""<div style="font-family:'Press Start 2P',monospace;font-size:10px;
         color:var(--accent);letter-spacing:1px;margin-bottom:4px">
         ► {user['name'].upper()} &nbsp;·&nbsp; {user['title'].upper()} &nbsp;·&nbsp;
         LV {user['level']} &nbsp;·&nbsp; {user['xp']:,} XP &nbsp;·&nbsp;
         {user['bps']:,} BPS &nbsp;·&nbsp; 🔥 {user['streak']}
    </div>""",
    unsafe_allow_html=True
)

# Build one row of buttons
nav_cols = st.columns(len(NAV_PAGES))
for col, (pkey, label) in zip(nav_cols, NAV_PAGES):
    active_style = "background:var(--accent);color:var(--bg);" if pkey == page else ""
    # Use a regular Streamlit button; CSS handles hover
    if col.button(label, key=f"nav_{pkey}"):
        st.session_state["page"] = pkey
        st.rerun()

st.markdown('<hr style="margin:4px 0 16px">', unsafe_allow_html=True)

# Switch profile link
if st.button("↩ SWITCH PROFILE", key="switch_profile"):
    del st.session_state["user_id"]
    st.session_state["page"] = "login"
    st.rerun()

# --- Placement diagnostic on first launch ---
if page not in ("login",) and should_show_placement(user_id):
    page = "placement"
    st.session_state["page"] = "placement"

# --- Page routing ---
if page == "placement":
    render_placement(lessons, user_id)

elif page == "tree":
    st.title("Skill Tree")
    render_skill_tree(track_tree, user_id, lessons)

elif page == "lesson":
    lid = st.session_state.get("active_lesson")
    if lid and lid in lessons:
        if st.button("← Back to tree"):
            st.session_state["page"] = "tree"
            st.rerun()
        render_lesson(lessons[lid], user_id)
    else:
        st.warning("No lesson selected.")
        st.session_state["page"] = "tree"
        st.rerun()

elif page == "review":
    st.title("Daily Review")
    due_cards = storage.get_due_cards(user_id)
    if not due_cards:
        st.success("You're all caught up. Nothing due today.")
        from rewards import get_reward_card
        from components.theme import reward_card_html
        card = get_reward_card("review_clear")
        st.markdown(reward_card_html(card["title"], card["body"]), unsafe_allow_html=True)
    else:
        # Find and render lessons that have due cards
        lesson_ids = list({c["lesson_id"] for c in due_cards})
        st.markdown(f"**{len(due_cards)} card(s) due across {len(lesson_ids)} lesson(s)**")
        for lid in lesson_ids:
            if lid in lessons:
                lesson = lessons[lid]
                st.markdown(f"### {lesson['title']}")
                render_lesson(lesson, user_id)
                st.markdown("---")

elif page == "interview":
    render_interview_sim(lessons, user_id)

elif page == "weak":
    render_weak_spots(user_id, lessons)

elif page == "jargon":
    render_jargon_deck(jargon)

elif page == "pitch":
    render_stock_pitch(user_id)

elif page == "calendar":
    render_calendar(user_id, lessons)

elif page == "todo":
    render_todo(user_id)

elif page == "profile":
    col1, col2 = st.columns([1, 2])
    with col1:
        render_desk_scene(user)
    with col2:
        render_profile(user)

elif page == "shop":
    render_shop(user)

elif page == "upload":
    render_content_upload()

else:
    st.session_state["page"] = "tree"
    st.rerun()
