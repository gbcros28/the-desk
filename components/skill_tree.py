"""Renders the dynamic skill tree built from loaded content."""
import streamlit as st
import scheduler
import storage
from components.theme import mastery_badge


def render_skill_tree(track_tree: dict, user_id: int, lessons: dict):
    lp = storage.get_all_lesson_progress(user_id)

    for track_letter, track in track_tree.items():
        with st.expander(f"**Track {track_letter}: {track['track_name']}**", expanded=True):
            for unit_key, unit in track["units"].items():
                st.markdown(f"##### {unit['unit_name']}")
                for lesson in unit["lessons"]:
                    lid = lesson["id"]
                    prereqs = lesson.get("prerequisites", [])
                    prereqs_met = scheduler.prerequisites_met(user_id, prereqs)
                    ldata = lp.get(lid, {})
                    mastery   = ldata.get("mastery", 0.0)
                    completed = bool(ldata.get("completed", 0))

                    if not prereqs_met:
                        st.markdown(
                            f'<div style="opacity:0.45;margin:4px 0">🔒 '
                            f'<span style="text-decoration:line-through">{lesson["title"]}</span>'
                            f' <span style="font-size:12px">· Complete prerequisites first</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        badge = mastery_badge(mastery)
                        if completed:
                            label = f"{badge} {lesson['title']} — {mastery:.0f}%"
                        else:
                            label = f"▶ {lesson['title']}"
                        if st.button(label, key=f"tree_{lid}"):
                            # Clear any stale "done" state so lesson starts fresh
                            stale_key = f"lesson_{lid}"
                            if st.session_state.get(stale_key, {}).get("phase") == "done":
                                del st.session_state[stale_key]
                            st.session_state["active_lesson"] = lid
                            st.rerun()
                st.markdown("")


def render_weak_spots(user_id: int, lessons: dict):
    lp = storage.get_all_lesson_progress(user_id)
    started = [(lid, data) for lid, data in lp.items() if data.get("mastery", 0) > 0]
    started.sort(key=lambda x: x[1]["mastery"])
    weak = started[:5]

    if not weak:
        st.info("Complete some lessons first — then your weak spots will show up here.")
        return

    st.markdown("### Your weakest areas")
    for lid, data in weak:
        lesson = lessons.get(lid)
        if not lesson:
            continue
        mastery = data["mastery"]
        badge = mastery_badge(mastery)
        st.markdown(f"{badge} **{lesson['title']}** — {mastery:.0f}%")
        if st.button(f"Review {lesson['title']}", key=f"weak_{lid}"):
            st.session_state["active_lesson"] = lid
            st.session_state["page"] = "lesson"
            st.rerun()
