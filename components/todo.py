"""To-do list — per user, stored in SQLite."""
import streamlit as st
import storage
from datetime import date


def render_todo(user_id: int):
    st.markdown("## To-Do List")

    # --- Add new task ---
    with st.form("add_todo_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            text = st.text_input("New task", placeholder="e.g. Review DCF lesson, prep stock pitch…")
        with col2:
            due = st.date_input("Due date (optional)", value=None)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Add")
        if submitted and text.strip():
            due_str = str(due) if due else None
            storage.add_todo(user_id, text.strip(), due_str)
            st.rerun()

    st.markdown("---")

    # --- Active tasks ---
    todos = storage.get_todos(user_id, include_done=False)
    today = str(date.today())

    if not todos:
        st.info("Nothing on the list. Add a task above.")
    else:
        for t in todos:
            col1, col2, col3 = st.columns([6, 2, 1])
            with col1:
                overdue = t["due_date"] and t["due_date"] < today
                prefix = "🔴 " if overdue else "📌 "
                label = f"{prefix}{t['text']}"
                st.markdown(label)
            with col2:
                if t["due_date"]:
                    due_label = f"Due {t['due_date']}"
                    if overdue:
                        st.markdown(f"<span style='color:#e05252'>{due_label}</span>", unsafe_allow_html=True)
                    else:
                        st.caption(due_label)
            with col3:
                if st.button("✓", key=f"done_{t['id']}", help="Mark complete"):
                    storage.complete_todo(t["id"], user_id)
                    st.rerun()

    # --- Completed tasks (collapsible) ---
    done_todos = storage.get_todos(user_id, include_done=True)
    done_todos = [t for t in done_todos if t["done"]]
    if done_todos:
        with st.expander(f"✅ Completed ({len(done_todos)})"):
            for t in done_todos:
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.markdown(f"~~{t['text']}~~")
                with col2:
                    if st.button("🗑", key=f"del_{t['id']}", help="Delete"):
                        storage.delete_todo(t["id"], user_id)
                        st.rerun()
