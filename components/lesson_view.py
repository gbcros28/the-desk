"""Renders the full lesson: concept → worked example → glossary → questions."""
import streamlit as st
import scheduler
import gamification
import rewards
import storage
from components.theme import callout_html, formula_html, why_html, reward_card_html
from components.question_renderer import render_question


def render_lesson(lesson: dict, user_id: int):
    lid = lesson["id"]
    session_key = f"lesson_{lid}"

    if session_key not in st.session_state:
        st.session_state[session_key] = {
            "phase": "content",   # content → questions → done
            "q_index": 0,
            "results": [],
            "first_attempt": True,
        }

    state = st.session_state[session_key]

    st.markdown(why_html(lesson["why_it_matters"], lesson.get("in_the_seat", "")), unsafe_allow_html=True)

    if state["phase"] == "content":
        _render_content(lesson)
        if st.button("Start questions →", key=f"{lid}_start_q"):
            state["phase"] = "questions"
            st.rerun()

    elif state["phase"] == "questions":
        questions = lesson["questions"]
        idx = state["q_index"]
        if idx >= len(questions):
            state["phase"] = "done"
            st.rerun()
            return

        q = questions[idx]
        st.markdown(f"**Question {idx + 1} of {len(questions)}**")
        answered, correct, outcome = render_question(q, key_prefix=f"{lid}_{idx}")

        if answered:
            state["results"].append({"qid": q["id"], "correct": correct, "outcome": outcome,
                                     "first": state.get("first_attempt", True)})
            xp, bps = gamification.award_question(user_id, first_try=state["first_attempt"], correct=correct)
            state["first_attempt"] = True  # reset for next question

            if st.button("Next →", key=f"{lid}_next_{idx}"):
                # clear per-question state so next render is fresh
                _clear_question_state(q["id"], f"{lid}_{idx}")
                state["q_index"] += 1
                state["first_attempt"] = True
                st.rerun()

    elif state["phase"] == "done":
        _render_completion(lesson, user_id, state["results"])


def _render_content(lesson: dict):
    st.subheader(lesson["title"])

    for sec in lesson["concept"]:
        if sec["type"] == "text":
            st.markdown(sec["body"])
        elif sec["type"] == "callout":
            st.markdown(callout_html(sec["variant"], sec["body"]), unsafe_allow_html=True)
        elif sec["type"] == "formula":
            st.markdown(formula_html(sec["label"], sec["expression"], sec.get("note", "")),
                        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### 📋 Worked Example: {lesson['worked_example']['title']}")
    st.markdown(lesson["worked_example"]["body"])

    if lesson.get("glossary"):
        with st.expander("📖 Glossary"):
            for g in lesson["glossary"]:
                st.markdown(f"**{g['term']}** — {g['definition']}")


def _render_completion(lesson: dict, user_id: int, results: list):
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = int(correct / total * 100) if total else 0

    gamification.award_lesson_complete(user_id)
    question_ids = [q["id"] for q in lesson["questions"]]
    mastery = scheduler.update_lesson_mastery(user_id, lesson["id"], question_ids)

    cr = lesson["completion_reward"]
    st.markdown(reward_card_html(cr["title"], cr["body"]), unsafe_allow_html=True)
    st.markdown(f"**Accuracy:** {correct}/{total} ({accuracy}%)  |  **Mastery:** {mastery:.0f}/100")

    milestone_card = rewards.get_reward_card("lesson_first")
    if not storage.check_milestone(user_id, f"lesson_{lesson['id']}"):
        storage.record_milestone(user_id, f"lesson_{lesson['id']}")
        st.markdown(reward_card_html(milestone_card["title"], milestone_card["body"]), unsafe_allow_html=True)


def _clear_question_state(question_id: str, prefix: str):
    key = f"{prefix}_{question_id}"
    for suffix in ("_ans", "_submitted", "_val", "_inp", "_shuffled", "_attempt", "_revealed", "_rated"):
        k = key + suffix
        if k in st.session_state:
            del st.session_state[k]
