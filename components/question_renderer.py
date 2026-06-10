"""Renders and grades all question types. Returns (correct: bool, outcome: str)."""
import random
import streamlit as st


def render_question(q: dict, key_prefix: str = "") -> tuple:
    """
    Returns (answered: bool, correct: bool, outcome: str)
    outcome is one of: correct, wrong, partial, again, hard, good, easy
    """
    qt = q["type"]
    key = f"{key_prefix}_{q['id']}"
    st.markdown(f"**{q['prompt']}**")

    if qt == "mcq":
        return _mcq(q, key)
    elif qt == "numeric":
        return _numeric(q, key)
    elif qt == "fill_blank":
        return _fill_blank(q, key)
    elif qt == "ordering":
        return _ordering(q, key)
    elif qt == "matching":
        return _matching(q, key)
    elif qt == "free_response":
        return _free_response(q, key)
    elif qt == "linked_statements":
        return _linked_statements(q, key)
    else:
        st.warning(f"Unknown question type: {qt}")
        return False, False, "wrong"


def _mcq(q, key):
    state_key = f"{key}_ans"
    submitted_key = f"{key}_submitted"

    if submitted_key not in st.session_state:
        choice = st.radio("", q["choices"], key=state_key, index=None)
        if st.button("Submit", key=f"{key}_btn"):
            if choice is None:
                st.warning("Select an answer first.")
                return False, False, ""
            st.session_state[submitted_key] = q["choices"].index(choice)
            st.rerun()
        return False, False, ""

    chosen_idx = st.session_state[submitted_key]
    correct_idx = q["answer_index"]
    for i, c in enumerate(q["choices"]):
        if i == correct_idx:
            st.markdown(f"✅ **{c}**")
        elif i == chosen_idx and chosen_idx != correct_idx:
            st.markdown(f"❌ ~~{c}~~")
        else:
            st.markdown(f"&nbsp;&nbsp;&nbsp;{c}")
    correct = chosen_idx == correct_idx
    st.info(f"**Explanation:** {q['explanation']}")
    return True, correct, "correct" if correct else "wrong"


def _numeric(q, key):
    submitted_key = f"{key}_submitted"
    val_key = f"{key}_val"

    if submitted_key not in st.session_state:
        val = st.number_input(f"Your answer ({q['unit']})", key=val_key, value=0.0, format="%.4f")
        if st.button("Submit", key=f"{key}_btn"):
            st.session_state[submitted_key] = val
            st.rerun()
        return False, False, ""

    val = st.session_state[submitted_key]
    answer = float(q["answer"])
    tol = float(q["tolerance"])
    correct = abs(val - answer) <= tol
    if correct:
        st.success(f"✅ Correct! Answer: {answer} {q['unit']}")
    else:
        st.error(f"❌ Your answer: {val} {q['unit']} | Correct: {answer} {q['unit']} (±{tol})")
    st.info(f"**Explanation:** {q['explanation']}")
    return True, correct, "correct" if correct else "wrong"


def _fill_blank(q, key):
    submitted_key = f"{key}_submitted"
    inp_key = f"{key}_inp"

    if submitted_key not in st.session_state:
        ans = st.text_input("Your answer:", key=inp_key)
        if st.button("Submit", key=f"{key}_btn"):
            if not ans.strip():
                st.warning("Enter an answer first.")
                return False, False, ""
            st.session_state[submitted_key] = ans.strip()
            st.rerun()
        return False, False, ""

    ans = st.session_state[submitted_key]
    accepted = [a.lower() for a in q["accepted"]]
    correct = ans.lower() in accepted
    if correct:
        st.success(f"✅ Correct! ({ans})")
    else:
        st.error(f"❌ Your answer: {ans} | Accepted: {', '.join(q['accepted'])}")
    st.info(f"**Explanation:** {q['explanation']}")
    return True, correct, "correct" if correct else "wrong"


def _ordering(q, key):
    submitted_key = f"{key}_submitted"
    shuffle_key = f"{key}_shuffled"

    if shuffle_key not in st.session_state:
        shuffled = q["items"][:]
        random.shuffle(shuffled)
        st.session_state[shuffle_key] = shuffled

    shuffled = st.session_state[shuffle_key]

    if submitted_key not in st.session_state:
        st.markdown("*Drag to reorder — or number them:*")
        order = []
        for i, item in enumerate(shuffled):
            rank = st.number_input(f"{item}", min_value=1, max_value=len(shuffled),
                                   value=i + 1, key=f"{key}_ord_{i}", step=1)
            order.append((rank, item))
        if st.button("Submit", key=f"{key}_btn"):
            user_order = [item for _, item in sorted(order, key=lambda x: x[0])]
            st.session_state[submitted_key] = user_order
            st.rerun()
        return False, False, ""

    user_order = st.session_state[submitted_key]
    correct_order = q["items"]
    correct = user_order == correct_order
    if correct:
        st.success("✅ Correct order!")
    else:
        st.error("❌ Not quite.")
        st.markdown("**Correct order:**")
        for i, item in enumerate(correct_order, 1):
            st.markdown(f"{i}. {item}")
    st.info(f"**Explanation:** {q['explanation']}")
    return True, correct, "correct" if correct else "wrong"


def _matching(q, key):
    submitted_key = f"{key}_submitted"
    pairs = q["pairs"]
    rights = [p["right"] for p in pairs]

    if submitted_key not in st.session_state:
        user_matches = {}
        for p in pairs:
            choice = st.selectbox(f"{p['left']} →", options=["-- select --"] + rights,
                                  key=f"{key}_match_{p['left']}")
            user_matches[p["left"]] = choice
        if st.button("Submit", key=f"{key}_btn"):
            if any(v == "-- select --" for v in user_matches.values()):
                st.warning("Complete all matches first.")
                return False, False, ""
            st.session_state[submitted_key] = user_matches
            st.rerun()
        return False, False, ""

    user_matches = st.session_state[submitted_key]
    correct_map = {p["left"]: p["right"] for p in pairs}
    num_correct = sum(1 for left, right in user_matches.items() if correct_map.get(left) == right)
    correct = num_correct == len(pairs)
    for p in pairs:
        icon = "✅" if user_matches.get(p["left"]) == p["right"] else "❌"
        st.markdown(f"{icon} **{p['left']}** → {p['right']}")
    if not correct:
        st.error(f"{num_correct}/{len(pairs)} correct")
    else:
        st.success("✅ All matched!")
    st.info(f"**Explanation:** {q['explanation']}")
    return True, correct, "correct" if correct else ("partial" if num_correct > 0 else "wrong")


def _free_response(q, key):
    attempt_key = f"{key}_attempt"
    revealed_key = f"{key}_revealed"
    rated_key = f"{key}_rated"

    if attempt_key not in st.session_state:
        st.text_area("Your answer:", key=attempt_key, height=100)
        if st.button("Reveal answer", key=f"{key}_reveal_btn"):
            if not st.session_state.get(attempt_key, "").strip():
                st.warning("Write something first — even a rough attempt.")
                return False, False, ""
            st.session_state[revealed_key] = True
            st.rerun()
        return False, False, ""

    if not st.session_state.get(revealed_key):
        st.session_state[revealed_key] = True

    st.markdown(f"**Model answer:** {q['model_answer']}")
    if q.get("rubric"):
        st.markdown("**Rubric:**")
        for point in q["rubric"]:
            st.markdown(f"- {point}")
    st.info(f"**Explanation:** {q['explanation']}")

    if rated_key not in st.session_state:
        st.markdown("**How did you do?**")
        cols = st.columns(4)
        outcomes = [("Again", "again"), ("Hard", "hard"), ("Good", "good"), ("Easy", "easy")]
        for col, (label, outcome) in zip(cols, outcomes):
            if col.button(label, key=f"{key}_{outcome}_btn"):
                st.session_state[rated_key] = outcome
                st.rerun()
        return False, False, ""

    outcome = st.session_state[rated_key]
    correct = outcome in ("good", "easy")
    return True, correct, outcome


# ── 3-Statement Linked Sandbox ─────────────────────────────────────────────

def _validate_accounting_transaction(user_inputs: dict, expected: dict, tol: float = 0.5) -> dict:
    """
    Validate a set of accounting inputs against expected deltas.
    Also enforces the Balance Sheet equation: ΔAssets == ΔLiabilities + ΔEquity.
    Returns {field: (user_val, expected_val, ok), ..., 'bs_check': bool, 'all_correct': bool}
    """
    results = {}
    for field, exp_val in expected.items():
        user_val = float(user_inputs.get(field, 0))
        ok = abs(user_val - exp_val) <= tol
        results[field] = (user_val, exp_val, ok)

    # Balance sheet assertion: ΔTotal_Assets == ΔTotal_Liabilities + ΔRetained_Earnings
    da  = user_inputs.get("Delta_Total_Assets", 0)
    dl  = user_inputs.get("Delta_Total_Liabilities", 0)
    dre = user_inputs.get("Delta_Retained_Earnings", 0)
    bs_ok = abs(float(da) - (float(dl) + float(dre))) <= tol
    results["_bs_check"] = (float(da), float(dl) + float(dre), bs_ok)

    results["_all_correct"] = all(v[2] for k, v in results.items() if k.startswith("_") is False) and bs_ok
    return results


def _linked_statements(q: dict, key: str):
    """
    Renders an interactive 3-statement sandbox question.
    q must have:
      prompt, scenario (str), fields (list of {id, label, statement}),
      expected (dict {field_id: delta_value}), explanation, tolerance (float, optional)
    """
    submitted_key = f"{key}_submitted"
    tol = float(q.get("tolerance", 0.5))

    scenario = q.get("scenario", "")
    fields   = q.get("fields", [])   # [{id, label, statement: IS/CFS/BS}]

    if scenario:
        st.markdown(
            f'<div style="background:#1a2030;border-left:3px solid #4a8fe8;'
            f'padding:10px 14px;border-radius:4px;margin:8px 0;font-size:13px">'
            f'📋 <b>Scenario:</b> {scenario}</div>',
            unsafe_allow_html=True
        )

    # Group by statement
    statements = {"IS": [], "CFS": [], "BS": []}
    for f in fields:
        stmt = f.get("statement", "BS")
        statements.setdefault(stmt, []).append(f)

    if submitted_key not in st.session_state:
        user_inputs = {}

        st.markdown("*Enter the **change (Δ)** in each line item caused by the scenario:*")

        for stmt_id, stmt_name, stmt_color in [
            ("IS",  "Income Statement",      "#4a8fe8"),
            ("CFS", "Cash Flow Statement",   "#8ab44a"),
            ("BS",  "Balance Sheet",         "#c8a428"),
        ]:
            stmt_fields = statements.get(stmt_id, [])
            if not stmt_fields:
                continue
            st.markdown(
                f'<div style="color:{stmt_color};font-weight:600;margin-top:12px;'
                f'font-size:13px;border-bottom:1px solid {stmt_color}44;padding-bottom:4px">'
                f'{stmt_name}</div>',
                unsafe_allow_html=True
            )
            for f in stmt_fields:
                val = st.number_input(
                    f['label'], key=f"{key}_field_{f['id']}",
                    value=0.0, format="%.2f",
                    help=f"Enter the delta (positive = increase, negative = decrease)"
                )
                user_inputs[f["id"]] = val

        # BS balance check note
        st.caption("💡 Reminder: ΔAssets must equal ΔLiabilities + ΔRetained Earnings")

        if st.button("Submit", key=f"{key}_btn"):
            # Collect current values from session state
            collected = {}
            for f in fields:
                collected[f["id"]] = st.session_state.get(f"{key}_field_{f['id']}", 0.0)
            st.session_state[submitted_key] = collected
            st.rerun()
        return False, False, ""

    # ── Show graded results ────────────────────────────────────────────────
    user_inputs = st.session_state[submitted_key]
    expected    = q.get("expected", {})
    results     = _validate_accounting_transaction(user_inputs, expected, tol)

    all_correct = results.pop("_all_correct", False)
    bs_check    = results.pop("_bs_check", (0, 0, True))

    for stmt_id, stmt_name, stmt_color in [
        ("IS",  "Income Statement",      "#4a8fe8"),
        ("CFS", "Cash Flow Statement",   "#8ab44a"),
        ("BS",  "Balance Sheet",         "#c8a428"),
    ]:
        stmt_fields = [f for f in fields if f.get("statement") == stmt_id]
        if not stmt_fields:
            continue
        st.markdown(
            f'<div style="color:{stmt_color};font-weight:600;margin-top:12px">{stmt_name}</div>',
            unsafe_allow_html=True
        )
        for f in stmt_fields:
            fid = f["id"]
            if fid not in results:
                continue
            user_val, exp_val, ok = results[fid]
            icon = "✅" if ok else "❌"
            st.markdown(
                f'{icon} **{f["label"]}**: you entered **{user_val:+.2f}**, '
                f'correct: **{exp_val:+.2f}**'
            )

    # BS balance assertion
    bs_icon = "✅" if bs_check[2] else "❌"
    st.markdown(
        f'{bs_icon} **Balance Sheet Check**: ΔAssets ({bs_check[0]:+.2f}) '
        f'= ΔLiab + ΔEquity ({bs_check[1]:+.2f})'
    )

    if all_correct:
        st.success("✅ All statements balance correctly!")
    else:
        st.error("❌ Some entries need correction — review the deltas above.")

    st.info(f"**Explanation:** {q['explanation']}")
    return True, all_correct, "correct" if all_correct else "wrong"
