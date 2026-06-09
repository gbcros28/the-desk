"""XP, levels, bps, streaks, titles, and cosmetics logic."""
import json
import storage

XP_PER_QUESTION = 10
XP_FIRST_TRY_BONUS = 5
XP_LESSON_COMPLETE = 50
XP_REVIEW_QUEUE_CLEAR = 25

BPS_PER_QUESTION = 2
BPS_LESSON_COMPLETE = 20

LEVELS = [
    (0,    1),
    (100,  2),
    (300,  3),
    (600,  4),
    (1000, 5),
    (1500, 6),
    (2500, 7),
    (4000, 8),
    (6000, 9),
    (9000, 10),
]

TITLES = [
    (0,    "Intern"),
    (200,  "Analyst"),
    (800,  "Senior Analyst"),
    (2000, "Associate"),
    (5000, "PM"),
]

SHOP_ITEMS = [
    {"id": "streak_freeze",    "name": "Streak Freeze",     "cost": 50,  "description": "Protects your streak for one missed day.", "category": "consumable"},
    {"id": "desk_plant",       "name": "Desk Plant",        "cost": 30,  "description": "A small succulent. Very professional.",     "category": "cosmetic"},
    {"id": "extra_monitor",    "name": "Extra Monitor",     "cost": 80,  "description": "Two screens. You're serious now.",           "category": "cosmetic"},
    {"id": "coffee_cup",       "name": "Coffee Cup",        "cost": 20,  "description": "The large is a tell.",                       "category": "cosmetic"},
    {"id": "bloomberg_theme",  "name": "Bloomberg Theme",   "cost": 150, "description": "Terminal green. Ambiance included.",         "category": "theme"},
    {"id": "vest",             "name": "The Vest",          "cost": 500, "description": "Earned. Not bought. (Actually bought.)",      "category": "cosmetic"},
    {"id": "dark_theme",       "name": "Dark Mode",         "cost": 40,  "description": "For late-night modeling sessions.",          "category": "theme"},
]


def xp_to_level(xp: int) -> int:
    level = 1
    for threshold, lvl in LEVELS:
        if xp >= threshold:
            level = lvl
    return level


def xp_for_next_level(xp: int) -> tuple:
    current = xp_to_level(xp)
    for threshold, lvl in LEVELS:
        if lvl == current + 1:
            return threshold, lvl
    return None, None


def xp_to_title(xp: int) -> str:
    title = "Intern"
    for threshold, t in TITLES:
        if xp >= threshold:
            title = t
    return title


def award_question(user_id: int, first_try: bool = False, correct: bool = True):
    xp = XP_PER_QUESTION if correct else 2
    bps = BPS_PER_QUESTION if correct else 0
    if first_try and correct:
        xp += XP_FIRST_TRY_BONUS
        bps += 1
    storage.add_xp(user_id, xp)
    storage.add_bps(user_id, bps)
    storage.increment_daily_done(user_id)
    _sync_level_and_title(user_id)
    return xp, bps


def award_lesson_complete(user_id: int):
    storage.add_xp(user_id, XP_LESSON_COMPLETE)
    storage.add_bps(user_id, BPS_LESSON_COMPLETE)
    _sync_level_and_title(user_id)


def award_review_clear(user_id: int):
    storage.add_xp(user_id, XP_REVIEW_QUEUE_CLEAR)
    _sync_level_and_title(user_id)


def _sync_level_and_title(user_id: int):
    user = storage.get_user(user_id)
    if not user:
        return
    new_level = xp_to_level(user["xp"])
    new_title = xp_to_title(user["xp"])
    updates = {}
    if new_level != user["level"]:
        updates["level"] = new_level
    if new_title != user["title"]:
        updates["title"] = new_title
    if updates:
        storage.update_user(user_id, **updates)


def get_owned_cosmetics(user: dict) -> list:
    try:
        return json.loads(user.get("owned_cosmetics") or "[]")
    except Exception:
        return []


def get_equipped(user: dict) -> dict:
    try:
        return json.loads(user.get("equipped") or "{}")
    except Exception:
        return {}


def buy_item(user_id: int, item_id: str) -> tuple:
    item = next((i for i in SHOP_ITEMS if i["id"] == item_id), None)
    if not item:
        return False, "Item not found."
    user = storage.get_user(user_id)
    owned = get_owned_cosmetics(user)

    if item["category"] == "consumable":
        if not storage.spend_bps(user_id, item["cost"]):
            return False, f"Not enough bps. Need {item['cost']}."
        if item_id == "streak_freeze":
            storage.update_user(user_id, streak_freeze=user.get("streak_freeze", 0) + 1)
        return True, f"Purchased {item['name']}!"

    if item_id in owned:
        return False, "Already owned."
    if not storage.spend_bps(user_id, item["cost"]):
        return False, f"Not enough bps. Need {item['cost']}."
    owned.append(item_id)
    storage.update_user(user_id, owned_cosmetics=json.dumps(owned))
    return True, f"Purchased {item['name']}!"


def equip_item(user_id: int, item_id: str) -> bool:
    user = storage.get_user(user_id)
    owned = get_owned_cosmetics(user)
    if item_id not in owned:
        return False
    item = next((i for i in SHOP_ITEMS if i["id"] == item_id), None)
    if not item:
        return False
    equipped = get_equipped(user)
    equipped[item["category"]] = item_id
    storage.update_user(user_id, equipped=json.dumps(equipped))
    return True


def get_active_theme(user: dict) -> str:
    equipped = get_equipped(user)
    return equipped.get("theme", "default")
