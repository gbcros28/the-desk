"""Reward card copy pool. Edit freely — no code changes needed."""
import random

MILESTONE_CARDS = {
    "lesson_first": [
        {"title": "Day one.", "body": "One lesson down. The person next to you in the final-round interview hasn't started yet."},
        {"title": "First rep.", "body": "Muscle memory starts here. Come back tomorrow."},
    ],
    "streak_3": [
        {"title": "Three days.", "body": "That's two more than most people manage before checking Instagram."},
    ],
    "streak_7": [
        {"title": "One week.", "body": "Seven consecutive days of not having to say 'I'm still learning the basics' in an interview."},
    ],
    "streak_30": [
        {"title": "Thirty days.", "body": "At this point you're not studying for recruiting. You're just doing the job early."},
    ],
    "level_up": [
        {"title": "Level up.", "body": "New title loading. Don't let it go to your head until you can walk through a DCF cold."},
        {"title": "Promoted.", "body": "Figuratively. The real one requires two years and a supportive MD."},
    ],
    "track_complete": [
        {"title": "Track cleared.", "body": "Full marks. The froyo is on you — the large is a tell."},
        {"title": "Mastered.", "body": "One more track down. The tree doesn't lie."},
    ],
    "review_clear": [
        {"title": "Queue empty.", "body": "Inbox zero, but for your brain."},
        {"title": "All caught up.", "body": "Nothing due. Enjoy it for exactly twelve hours."},
    ],
    "placement_done": [
        {"title": "Diagnostic complete.", "body": "Results are in. The tree has been calibrated accordingly."},
    ],
}


def get_reward_card(milestone_key: str) -> dict:
    pool = MILESTONE_CARDS.get(milestone_key)
    if not pool:
        return {"title": "Nice work.", "body": "Keep going."}
    return random.choice(pool)
