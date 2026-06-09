"""
SM-2 spaced repetition scheduler + mastery decay.
Quality scores: 0=Again, 1=Hard, 2=Good, 3=Easy (auto/self-rated)
"""
from datetime import date, timedelta
from typing import Optional
import storage

MASTERY_THRESHOLD = 70.0  # mastery >= this to count as "mastered" for prereq gating

# SM-2 quality mapping
QUALITY_MAP = {
    "again": 0,
    "hard":  2,
    "good":  3,
    "easy":  5,
    # auto-grade mappings
    "wrong":   0,
    "partial": 2,
    "correct": 4,
    "first_try_correct": 5,
}


def _sm2(ease_factor: float, interval: int, repetitions: int, quality: int):
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)
        repetitions += 1

    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(1.3, ease_factor)
    due_date = str(date.today() + timedelta(days=interval))
    mastery = min(100.0, repetitions * 20.0 * (ease_factor / 2.5))
    return ease_factor, interval, repetitions, due_date, mastery


def process_answer(user_id: int, question_id: str, lesson_id: str, outcome: str):
    quality = QUALITY_MAP.get(outcome, 3)
    existing = storage.get_progress(user_id, question_id)
    if existing:
        ef = existing["ease_factor"]
        iv = existing["interval"]
        rp = existing["repetitions"]
    else:
        ef, iv, rp = 2.5, 0, 0

    ef, iv, rp, due_date, mastery = _sm2(ef, iv, rp, quality)
    storage.upsert_progress(user_id, question_id, lesson_id, ef, iv, rp, due_date, quality, mastery)
    return mastery


def get_lesson_mastery(user_id: int, lesson_id: str, question_ids: list) -> float:
    if not question_ids:
        return 0.0
    total = 0.0
    for qid in question_ids:
        p = storage.get_progress(user_id, qid)
        total += p["mastery"] if p else 0.0
    raw = total / len(question_ids)

    # decay: if last review was > 14 days ago, reduce mastery
    lp = storage.get_lesson_progress(user_id, lesson_id)
    if lp and lp.get("completed_at"):
        last = date.fromisoformat(lp["completed_at"])
        days_since = (date.today() - last).days
        if days_since > 14:
            decay = min(0.5, (days_since - 14) * 0.02)
            raw = raw * (1 - decay)
    return round(raw, 1)


def update_lesson_mastery(user_id: int, lesson_id: str, question_ids: list):
    mastery = get_lesson_mastery(user_id, lesson_id, question_ids)
    lp = storage.get_lesson_progress(user_id, lesson_id)
    completed = lp["completed"] if lp else (mastery >= MASTERY_THRESHOLD)
    storage.upsert_lesson_progress(user_id, lesson_id, completed, mastery)
    return mastery


def is_mastered(user_id: int, lesson_id: str) -> bool:
    lp = storage.get_lesson_progress(user_id, lesson_id)
    if not lp:
        return False
    return lp["mastery"] >= MASTERY_THRESHOLD


def prerequisites_met(user_id: int, prereqs: list) -> bool:
    for pid in prereqs:
        if not is_mastered(user_id, pid):
            return False
    return True


def get_due_count(user_id: int) -> int:
    return len(storage.get_due_cards(user_id))
