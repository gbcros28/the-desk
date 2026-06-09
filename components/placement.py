"""Placement diagnostic — first-launch quiz, skippable, re-takeable."""
import random
import streamlit as st
import scheduler
import storage
from components.question_renderer import render_question


DIAGNOSTIC_PREF_KEY = "placement_done"


def should_show_placement(user_id: int) -> bool:
    return not storage.check_milestone(user_id, DIAGNOSTIC_PREF_KEY)


def render_placement(lessons: dict, user_id: int):
    st.markdown("## Placement Diagnostic")
    st.caption("A short quiz to calibrate your starting point. Correctly answered topics get a head start. Skippable anytime.")

    if st.button("Skip — start from the beginning"):
        storage.record_milestone(user_id, DIAGNOSTIC_PREF_KEY)
        st.session_state["page"] = "tree"
        st.rerun()

    key = "placement_state"
    if key not in st.session_state:
        # sample one representative question per early lesson (first 10 max)
        pool = []
        for lesson in list(lessons.values())[:10]:
            if lesson["questions"]:
                q = lesson["questions"][0]
                pool.append((lesson, q))
        random.shuffle(pool)
        pool = pool[:12]
        st.session_state[key] = {
            "pool": pool,
            "index": 0,
            "results": [],
            "phase": "quiz",
        }

    state = st.session_state[key]

    if state["phase"] == "quiz":
        pool = state["pool"]
        idx = state["index"]
        if idx >= len(pool):
            state["phase"] = "done"
            st.rerun()
            return

        lesson, q = pool[idx]
        st.markdown(f"**{idx + 1}/{len(pool)} — {lesson['title']}**")
        answered, correct, outcome = render_question(q, key_prefix=f"diag_{idx}")

        if answered:
            state["results"].append({"lesson": lesson, "q": q, "correct": correct})
            if st.button("Next →", key=f"diag_next_{idx}"):
                state["index"] += 1
                st.rerun()

    elif state["phase"] == "done":
        correct_lessons = set()
        for r in state["results"]:
            if r["correct"]:
                correct_lessons.add(r["lesson"]["id"])

        # pre-credit correctly answered lessons
        for lid in correct_lessons:
            lesson = lessons[lid]
            for q in lesson["questions"]:
                scheduler.process_answer(user_id, q["id"], lid, "good")
            scheduler.update_lesson_mastery(user_id, lid, [q["id"] for q in lesson["questions"]])

        storage.record_milestone(user_id, DIAGNOSTIC_PREF_KEY)
        st.success(f"Diagnostic complete. {len(correct_lessons)} topic(s) pre-credited.")
        from rewards import get_reward_card
        card = get_reward_card("placement_done")
        st.markdown(f"**{card['title']}** — {card['body']}")
        if st.button("Go to skill tree →"):
            del st.session_state[key]
            st.session_state["page"] = "tree"
            st.rerun()
