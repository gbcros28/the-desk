"""Profile display, daily goal, and streak info."""
import streamlit as st
import gamification
import storage
import rewards
import scheduler


def render_profile(user: dict):
    xp = user["xp"]
    level = gamification.xp_to_level(xp)
    title = gamification.xp_to_title(xp)
    equipped = gamification.get_equipped(user)
    owned = gamification.get_owned_cosmetics(user)

    theme = equipped.get("theme", "default")
    cosmetics_display = ", ".join(owned) if owned else "none"

    st.markdown(f"## {user['name']}")
    st.markdown(f"**{title}** · Level {level} · {xp:,} XP · {user['bps']:,} bps")

    # streak
    streak = user.get("streak", 0)
    freeze = user.get("streak_freeze", 0)
    streak_display = f"🔥 {streak}-day streak"
    if freeze:
        streak_display += f" (❄️ {freeze} freeze{'s' if freeze > 1 else ''} banked)"
    st.markdown(streak_display)

    # daily goal
    goal = user.get("daily_goal", 5)
    done = user.get("daily_done", 0)
    progress = min(done / goal, 1.0) if goal else 0
    st.progress(progress, text=f"Daily goal: {done}/{goal} questions")

    # next level
    next_threshold, next_level = gamification.xp_for_next_level(xp)
    if next_threshold:
        st.caption(f"Next level ({next_level}): {next_threshold - xp:,} XP to go")

    # review queue
    due = scheduler.get_due_count(user["user_id"])
    if due > 0:
        st.warning(f"📚 {due} card{'s' if due > 1 else ''} due for review")

    # cosmetics
    if owned:
        st.caption(f"Equipped: {', '.join(equipped.values()) or 'nothing'} | Owned: {cosmetics_display}")

    # social: streaks this week
    st.markdown("---")
    st.markdown("#### Who's on a streak this week")
    streakers = storage.get_streaks_this_week()
    if streakers:
        for s in streakers:
            you = " ← you" if s["name"] == user["name"] else ""
            st.markdown(f"🔥 **{s['name']}** — {s['streak']} days{you}")
    else:
        st.caption("No active streaks this week. First one back wins.")

    # daily goal setter
    st.markdown("---")
    with st.expander("Set daily goal"):
        new_goal = st.number_input("Questions per day", min_value=1, max_value=100,
                                    value=goal, step=1, key="daily_goal_input")
        if st.button("Save goal"):
            storage.update_user(user["user_id"], daily_goal=new_goal)
            st.success("Goal updated.")
            st.rerun()
