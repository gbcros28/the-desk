"""Renders lesson: concept → worked example → glossary → questions."""
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
            "phase": "content",
            "q_index": 0,
            "results": [],
        }

    state = st.session_state[session_key]

    # Why this matters — always shown
    st.markdown(
        why_html(lesson["why_it_matters"], lesson.get("in_the_seat", "")),
        unsafe_allow_html=True
    )

    if state["phase"] == "content":
        _render_content(lesson)
        col1, col2 = st.columns([1, 4])
        with col1:
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
        st.caption(f"Question {idx + 1} of {len(questions)}")
        answered, correct, outcome = render_question(q, key_prefix=f"{lid}_{idx}")

        if answered:
            state["results"].append({
                "qid": q["id"], "correct": correct, "outcome": outcome
            })
            xp, bps = gamification.award_question(
                user_id,
                first_try=(idx == 0 or state["results"][-2]["correct"] if len(state["results"]) > 1 else True),
                correct=correct
            )
            if st.button("Continue →", key=f"{lid}_next_{idx}"):
                _clear_question_state(q["id"], f"{lid}_{idx}")
                state["q_index"] += 1
                st.rerun()

    elif state["phase"] == "done":
        _render_completion(lesson, user_id, state["results"])


def _render_content(lesson: dict):
    st.markdown(f"## {lesson['title']}")

    # Estimated time if present
    mins = lesson.get("estimated_minutes")
    if mins:
        st.caption(f"~{mins} min")

    st.markdown("---")

    for sec in lesson["concept"]:
        _render_section(sec)

    st.markdown("---")
    _render_worked_example(lesson["worked_example"])

    if lesson.get("glossary"):
        with st.expander("Glossary"):
            for g in lesson["glossary"]:
                st.markdown(f"**{g['term']}** — {g['definition']}")


def _render_section(sec: dict):
    st.markdown('<div class="concept-section">', unsafe_allow_html=True)

    if sec["type"] == "text":
        if sec.get("heading"):
            st.markdown(
                f'<div class="concept-heading">{sec["heading"]}</div>',
                unsafe_allow_html=True
            )
        st.markdown(
            f'<div class="concept-body">{sec["body"]}</div>',
            unsafe_allow_html=True
        )

    elif sec["type"] == "callout":
        st.markdown(
            callout_html(sec["variant"], sec["body"], sec.get("heading", "")),
            unsafe_allow_html=True
        )

    elif sec["type"] == "formula":
        label = sec.get("heading") or sec.get("label") or "Formula"
        body  = sec.get("body") or sec.get("expression") or ""
        note  = sec.get("note", "")
        html  = formula_html(label, body)
        if note:
            html = html[:-6] + f'<div style="font-size:13px;opacity:0.6;margin-top:6px">{note}</div></div>'
        st.markdown(html, unsafe_allow_html=True)

    elif sec["type"] == "keyterm":
        term = sec.get("heading") or sec.get("term", "")
        body = sec.get("body") or sec.get("definition", "")
        st.markdown(
            f'<div style="padding:12px 16px;border-left:3px solid var(--accent);'
            f'margin:12px 0;font-size:14px"><strong>{term}</strong><br>{body}</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


def _render_worked_example(we: dict):
    st.markdown('<div class="worked-example">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="worked-example-title">Worked Example — {we["title"]}</div>',
        unsafe_allow_html=True
    )

    # Schema shape 1: {title, body}
    if "body" in we:
        st.markdown(we["body"])

    # Schema shape 2: {title, setup, steps, takeaway}
    else:
        if we.get("setup"):
            st.markdown(we["setup"])
        if we.get("steps"):
            steps_html = ""
            for i, step in enumerate(we["steps"], 1):
                steps_html += (f'<div class="worked-step">'
                               f'<span class="worked-step-num">{i}.</span>'
                               f'<span>{step}</span></div>')
            st.markdown(steps_html, unsafe_allow_html=True)
        if we.get("takeaway"):
            st.markdown(
                f'<div class="worked-takeaway">↳ {we["takeaway"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


def _render_completion(lesson: dict, user_id: int, results: list):
    total   = len(results)
    correct = sum(1 for r in results if r["correct"])
    acc     = int(correct / total * 100) if total else 0

    gamification.award_lesson_complete(user_id)
    question_ids = [q["id"] for q in lesson["questions"]]
    mastery = scheduler.update_lesson_mastery(user_id, lesson["id"], question_ids)

    cr = lesson.get("completion_reward", {})
    title = cr.get("title") or cr.get("copy") or "Lesson complete."
    body  = cr.get("body") or cr.get("copy") or ""
    if title == body:
        body = ""
    st.markdown(reward_card_html(title, body), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy",  f"{correct}/{total} ({acc}%)")
    col2.metric("Mastery",   f"{mastery:.0f}%")
    col3.metric("XP earned", f"+{gamification.XP_LESSON_COMPLETE}")

    if not storage.check_milestone(user_id, f"lesson_{lesson['id']}"):
        storage.record_milestone(user_id, f"lesson_{lesson['id']}")
        from rewards import get_reward_card
        card = get_reward_card("lesson_first")
        st.info(f"**{card['title']}** — {card['body']}")


def _clear_question_state(question_id: str, prefix: str):
    key = f"{prefix}_{question_id}"
    for suffix in ("_ans", "_submitted", "_val", "_inp", "_shuffled",
                   "_attempt", "_revealed", "_rated"):
        k = key + suffix
        if k in st.session_state:
            del st.session_state[k]
