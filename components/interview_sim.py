"""Interview Simulation mode — assembles free_response questions into a mock round."""
import streamlit as st
import storage
import scheduler


def render_interview_sim(lessons: dict, user_id: int):
    st.markdown("## Interview Simulation")
    st.caption("Answer all questions, then see every model answer and self-score. No per-question reveals.")

    # collect all free_response questions from unlocked lessons
    lp = storage.get_all_lesson_progress(user_id)
    candidates = []
    for lesson in lessons.values():
        prereqs_met = scheduler.prerequisites_met(user_id, lesson.get("prerequisites", []))
        is_started = lesson["id"] in lp
        if prereqs_met or is_started:
            for q in lesson["questions"]:
                if q["type"] == "free_response" and "interview" in q.get("tags", []):
                    candidates.append((lesson["title"], q))

    if not candidates:
        # fall back to all free_response from unlocked lessons
        for lesson in lessons.values():
            prereqs_met = scheduler.prerequisites_met(user_id, lesson.get("prerequisites", []))
            is_started = lesson["id"] in lp
            if prereqs_met or is_started:
                for q in lesson["questions"]:
                    if q["type"] == "free_response":
                        candidates.append((lesson["title"], q))

    if not candidates:
        st.info("No interview questions available yet. Complete a lesson first to unlock your first mock round.")
        return

    sim_key = "interview_sim_state"
    if sim_key not in st.session_state:
        import random
        selected = random.sample(candidates, min(6, len(candidates)))
        st.session_state[sim_key] = {
            "questions": selected,
            "answers": {},
            "phase": "answering",
        }

    state = st.session_state[sim_key]

    if state["phase"] == "answering":
        st.markdown(f"**{len(state['questions'])} questions — write your answers, then review all at once.**")
        for i, (lesson_title, q) in enumerate(state["questions"]):
            st.markdown(f"**Q{i+1}. [{lesson_title}]** {q['prompt']}")
            ans = st.text_area("", key=f"sim_ans_{i}", height=80, label_visibility="collapsed")
            state["answers"][i] = ans

        if st.button("Review all answers →"):
            state["phase"] = "review"
            st.rerun()

        if st.button("Start over", key="sim_reset"):
            del st.session_state[sim_key]
            st.rerun()

    elif state["phase"] == "review":
        st.markdown("### Review")
        scores = state.get("scores", {})
        all_rated = len(scores) == len(state["questions"])

        for i, (lesson_title, q) in enumerate(state["questions"]):
            st.markdown(f"---\n**Q{i+1}. [{lesson_title}]** {q['prompt']}")
            user_ans = state["answers"].get(i, "*(no answer)*")
            st.markdown(f"*Your answer:* {user_ans}")
            st.markdown(f"**Model answer:** {q['model_answer']}")
            if q.get("rubric"):
                for point in q["rubric"]:
                    st.markdown(f"- {point}")

            if i not in scores:
                c = st.columns(4)
                for col, label in zip(c, ["Again", "Hard", "Good", "Easy"]):
                    if col.button(label, key=f"sim_rate_{i}_{label}"):
                        scores[i] = label.lower()
                        state["scores"] = scores
                        st.rerun()

        if all_rated:
            goods = sum(1 for s in scores.values() if s in ("good", "easy"))
            st.markdown(f"---\n**Round complete.** {goods}/{len(state['questions'])} ≥ Good")
            if st.button("New round"):
                del st.session_state[sim_key]
                st.rerun()
