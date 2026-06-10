"""XP, levels, bps, streaks, titles, cosmetics, clothing, and alpha packs."""
import json
import random
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
    # Consumables
    {"id": "streak_freeze",   "name": "Streak Freeze",      "cost": 50,  "description": "Protects your streak for one missed day.",      "category": "consumable", "emoji": "❄️"},
    # Desk cosmetics
    {"id": "coffee_cup",      "name": "Coffee Cup",         "cost": 20,  "description": "The large is a tell.",                          "category": "cosmetic",   "emoji": "☕"},
    {"id": "desk_plant",      "name": "Desk Plant",         "cost": 30,  "description": "A small succulent. Very professional.",         "category": "cosmetic",   "emoji": "🪴"},
    {"id": "extra_monitor",   "name": "Extra Monitor",      "cost": 80,  "description": "Two screens. You're serious now.",              "category": "cosmetic",   "emoji": "🖥️"},
    {"id": "vest",            "name": "The Vest",           "cost": 300, "description": "Earned. Not bought. (Actually bought.)",        "category": "cosmetic",   "emoji": "🧥"},
    {"id": "rubber_duck",     "name": "Rubber Duck",        "cost": 15,  "description": "For debugging your models out loud.",           "category": "cosmetic",   "emoji": "🦆"},
    {"id": "stress_ball",     "name": "Stress Ball",        "cost": 25,  "description": "Quarterly earnings season essential.",          "category": "cosmetic",   "emoji": "🔴"},
    {"id": "framed_cert",     "name": "Framed CFA Cert",    "cost": 120, "description": "Three exams. One piece of paper. Worth it.",   "category": "cosmetic",   "emoji": "📜"},
    # Themes
    {"id": "bloomberg_theme", "name": "Bloomberg Terminal", "cost": 150, "description": "Black/orange, scanlines, all-caps. Iconic.",   "category": "theme",      "emoji": "🟠"},
    {"id": "stardew_theme",   "name": "Stardew Farm",       "cost": 200, "description": "Warm pixels, earthy browns. Cozy finance.",    "category": "theme",      "emoji": "🌾"},
    {"id": "cherry_theme",    "name": "Cherry Analyst",     "cost": 180, "description": "Blush pink pixel aesthetic. Soft but serious.", "category": "theme",      "emoji": "🌸"},
    {"id": "midnight_theme",  "name": "Midnight Terminal",  "cost": 220, "description": "Deep purple, neon cyan. Cyberpunk pixel.",     "category": "theme",      "emoji": "🌃"},
    {"id": "gold_theme",      "name": "Gold Tier",          "cost": 400, "description": "Black and gold. For when you've made it.",     "category": "theme",      "emoji": "🏆"},
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
    user    = storage.get_user(user_id)
    boosts  = calculate_outfit_boosters(user) if user else {"xp_mult": 1.0, "bps_mult": 1.0}

    if correct:
        xp  = int((XP_PER_QUESTION + (XP_FIRST_TRY_BONUS if first_try else 0)) * boosts["xp_mult"])
        bps = int((BPS_PER_QUESTION + (1 if first_try else 0)) * boosts["bps_mult"])
    else:
        xp, bps = 2, 0
        storage.drain_mental_capital(user_id, 10)

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


# ═══════════════════════════════════════════════════════════════════════════
#  RARITY SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

RARITY_TIERS = [
    {
        "id": "common",     "name": "Retail / Back Office",
        "label": "Common",  "color": "#C2B280",
        "booster": 0.01,    "weight": 50.0,
    },
    {
        "id": "uncommon",   "name": "Boutique / High-Net-Worth",
        "label": "Uncommon","color": "#355E3B",
        "booster": 0.03,    "weight": 30.0,
    },
    {
        "id": "rare",       "name": "Bulge Bracket / Institutional",
        "label": "Rare",    "color": "#800000",
        "booster": 0.05,    "weight": 14.0,
    },
    {
        "id": "epic",       "name": "Sovereign Wealth / Smart Money",
        "label": "Epic",    "color": "#C19A6B",
        "booster": 0.10,    "weight": 5.9,
    },
    {
        "id": "legendary",  "name": "Market Titan / Monopolist",
        "label": "Legendary","color": "#FF8F00",
        "booster": 0.25,    "weight": 0.1,
    },
]

RARITY_BY_ID = {r["id"]: r for r in RARITY_TIERS}

# ═══════════════════════════════════════════════════════════════════════════
#  CLOTHING ITEM DEFINITIONS
#  Fields: id, name, slot (Accessory/Jacket/Shirt/Pants/Shoes),
#          rarity, tier (1-4), colors, xp_booster, bps_booster
# ═══════════════════════════════════════════════════════════════════════════

CLOTHING_ITEMS = [
    # ── Tier 1 — Common ──────────────────────────────────────────────────
    {"id": "fleece_pullover",  "name": "Basic Utility Fleece Pullover",
     "slot": "Jacket", "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "The unofficial uniform of every junior analyst.",
     "sheet_img": "clothing_tier1_sheet"},

    {"id": "polo_shirt",       "name": "Plain Entry-Level Polo Shirt",
     "slot": "Shirt",  "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "Technically business casual. Nobody is impressed.",
     "sheet_img": "clothing_tier1_sheet"},

    {"id": "discount_slacks_sneakers", "name": "Discount Slacks & Flat Sneakers",
     "slot": "Pants",  "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "The 'I took the bus' ensemble.",
     "sheet_img": "clothing_tier1_sheet"},

    {"id": "merino_vest",      "name": "Thin Merino Wool V-Neck Sweater Vest",
     "slot": "Jacket", "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "From the 'trying but not quite there' collection.",
     "sheet_img": "clothing_tier1_sheet"},

    {"id": "oxford_tie_kit",   "name": "Oxford Dress Shirt & Thin Solid Necktie",
     "slot": "Shirt",  "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "You look like you're interviewing. Always interviewing.",
     "sheet_img": "clothing_tier1_sheet"},

    {"id": "chino_loafers",    "name": "Pressed Cotton Chinos & Simple Leather Loafers",
     "slot": "Shoes",  "rarity": "common",  "tier": 1,
     "colors": ["Black","Blue","Grey","White","#C2B280"],
     "xp_booster": 0.01, "bps_booster": 0.01,
     "desc": "Loafers: the shoe of people who need both hands free.",
     "sheet_img": "clothing_tier1_sheet"},

    # ── Tier 2 — Uncommon ─────────────────────────────────────────────────
    {"id": "midtown_vest",     "name": "The Midtown Vest — Classic Fleece",
     "slot": "Jacket", "rarity": "uncommon","tier": 2,
     "colors": ["Black","Blue","Grey","White","#355E3B"],
     "xp_booster": 0.03, "bps_booster": 0.03,
     "desc": "The power vest. You've been promoted once.",
     "sheet_img": "clothing_tier2_sheet"},

    {"id": "oxford_uni_tie",   "name": "Oxford Shirt & University Tie",
     "slot": "Shirt",  "rarity": "uncommon","tier": 2,
     "colors": ["Black","Blue","Grey","White","#355E3B"],
     "xp_booster": 0.03, "bps_booster": 0.03,
     "desc": "The tie implies alma mater. It's doing a lot of work.",
     "sheet_img": "clothing_tier2_sheet"},

    {"id": "wool_analyst_trousers", "name": "Tailored Wool Analyst Trousers",
     "slot": "Pants",  "rarity": "uncommon","tier": 2,
     "colors": ["Black","Blue","Grey","White","#355E3B"],
     "xp_booster": 0.03, "bps_booster": 0.03,
     "desc": "Because pleats are a privilege, not a right.",
     "sheet_img": "clothing_tier2_sheet"},

    {"id": "polished_oxford_shoes", "name": "Trousers & Polished Oxford Shoes",
     "slot": "Shoes",  "rarity": "uncommon","tier": 2,
     "colors": ["Black","Blue","Grey","White","#355E3B"],
     "xp_booster": 0.03, "bps_booster": 0.03,
     "desc": "Two coats of polish. You mean business.",
     "sheet_img": "clothing_tier2_sheet"},

    {"id": "formal_dress_kit", "name": "Formal Dress Shirt Kit",
     "slot": "Shirt",  "rarity": "uncommon","tier": 2,
     "colors": ["Black","Blue","Grey","White","#355E3B"],
     "xp_booster": 0.03, "bps_booster": 0.03,
     "desc": "French cuffs on a Thursday? Ambitious.",
     "sheet_img": "clothing_tier2_sheet"},

    # ── Tier 3 — Rare ─────────────────────────────────────────────────────
    {"id": "loro_piana_blazer","name": "Loro Piana Style Cashmere Hybrid",
     "slot": "Jacket", "rarity": "rare",    "tier": 3,
     "colors": ["Black","Blue","Grey","White","#800000"],
     "xp_booster": 0.05, "bps_booster": 0.05,
     "desc": "Soft enough to make you forget about mark-to-market losses.",
     "sheet_img": "clothing_tier3_sheet"},

    {"id": "charvet_poplin",   "name": "Charvet Style Luxury Poplin Shirt",
     "slot": "Shirt",  "rarity": "rare",    "tier": 3,
     "colors": ["Black","Blue","Grey","White","#800000"],
     "xp_booster": 0.05, "bps_booster": 0.05,
     "desc": "Hand-stitched. You're writing about it in your IC memo.",
     "sheet_img": "clothing_tier3_sheet"},

    {"id": "bespoke_wool_trousers","name": "Bespoke Heavy Wool Trousers",
     "slot": "Pants",  "rarity": "rare",    "tier": 3,
     "colors": ["Black","Blue","Grey","White","#800000"],
     "xp_booster": 0.05, "bps_booster": 0.05,
     "desc": "Two tucks. A statement.",
     "sheet_img": "clothing_tier3_sheet"},

    {"id": "double_monk_shoes","name": "Bespoke Trousers & Double Monk Shoes",
     "slot": "Shoes",  "rarity": "rare",    "tier": 3,
     "colors": ["Black","Blue","Grey","White","#800000"],
     "xp_booster": 0.05, "bps_booster": 0.05,
     "desc": "Double monks: the shoe of people who've read a book on shoes.",
     "sheet_img": "clothing_tier3_sheet"},

    # ── Tier 4 — Epic ─────────────────────────────────────────────────────
    {"id": "savile_bespoke_jacket","name": "Savile Row Bespoke Suit Jacket",
     "slot": "Jacket", "rarity": "epic",    "tier": 4,
     "colors": ["Black","Blue","Grey","White","#C19A6B"],
     "xp_booster": 0.10, "bps_booster": 0.10,
     "desc": "Eighteen fittings. Worth every one.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "hermes_micro_tie", "name": "Élite Hermès Micro-Pattern Tie",
     "slot": "Accessory","rarity": "epic",  "tier": 4,
     "colors": ["Black","Blue","Grey","White","#C19A6B"],
     "xp_booster": 0.10, "bps_booster": 0.10,
     "desc": "The equivalent of a bumper sticker that costs $250.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "premium_wool_trousers","name": "Premium Wool Suit Trousers",
     "slot": "Pants",  "rarity": "epic",    "tier": 4,
     "colors": ["Black","Blue","Grey","White","#C19A6B"],
     "xp_booster": 0.10, "bps_booster": 0.10,
     "desc": "The crease holds through a 14-hour day. Barely.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "mirror_captoe",    "name": "Mirror-Shined Cap-Toe Shoes",
     "slot": "Shoes",  "rarity": "epic",    "tier": 4,
     "colors": ["Black","Blue","Grey","White","#C19A6B"],
     "xp_booster": 0.10, "bps_booster": 0.10,
     "desc": "You can see yourself in them. You look tired.",
     "sheet_img": "clothing_tier4_sheet"},

    # ── Tier 5 — Legendary (hardcoded Monopolist set) ─────────────────────
    {"id": "monopolist_blazer","name": "Savile Row Blazer (Monopolist Edition)",
     "slot": "Jacket", "rarity": "legendary","tier": 5,
     "colors": ["#FF8F00"],
     "xp_booster": 0.25, "bps_booster": 0.25,
     "desc": "One of five. If you know, you know.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "titan_tie",        "name": "Titan Tie",
     "slot": "Accessory","rarity": "legendary","tier": 5,
     "colors": ["#FF8F00"],
     "xp_booster": 0.25, "bps_booster": 0.25,
     "desc": "Woven from hubris and structured credit.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "custom_trousers",  "name": "Custom Trousers (Monopolist Edition)",
     "slot": "Pants",  "rarity": "legendary","tier": 5,
     "colors": ["#FF8F00"],
     "xp_booster": 0.25, "bps_booster": 0.25,
     "desc": "The inseam was measured in Geneva.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "cj_captoes",       "name": "C&J Cap-Toes",
     "slot": "Shoes",  "rarity": "legendary","tier": 5,
     "colors": ["#FF8F00"],
     "xp_booster": 0.25, "bps_booster": 0.25,
     "desc": "Crockett & Jones. Hand-welted. End of discussion.",
     "sheet_img": "clothing_tier4_sheet"},

    {"id": "royal_oxford",     "name": "Royal Oxford (Monopolist Edition)",
     "slot": "Shirt",  "rarity": "legendary","tier": 5,
     "colors": ["#FF8F00"],
     "xp_booster": 0.25, "bps_booster": 0.25,
     "desc": "The fabric has a thread count. You don't ask what it is.",
     "sheet_img": "clothing_tier4_sheet"},
]

MONOPOLIST_SET = {"monopolist_blazer","titan_tie","custom_trousers","cj_captoes","royal_oxford"}
CLOTHING_BY_ID = {c["id"]: c for c in CLOTHING_ITEMS}

# ─── Alpha Pack pricing ───────────────────────────────────────────────────
ALPHA_PACK_COST = 200  # bps

# ═══════════════════════════════════════════════════════════════════════════
#  DECORATION ITEMS (purely cosmetic, unlocks office layer)
# ═══════════════════════════════════════════════════════════════════════════

DECORATION_ITEMS = [
    {"id": "bankers_lamp",    "name": "Banker's Lamp",     "cost": 80,
     "desc": "Green glass. Old money aesthetic.",            "sheet_img": "office_items_sheet"},
    {"id": "fiddle_leaf",     "name": "Fiddle-Leaf Fig",   "cost": 120,
     "desc": "The plant of every aspirational LinkedIn post.","sheet_img": "office_items_sheet"},
    {"id": "espresso_machine","name": "Espresso Machine",  "cost": 180,
     "desc": "Because drip coffee is for operations.",       "sheet_img": "office_items_sheet"},
    {"id": "diploma_frame",   "name": "Framed Diploma",    "cost": 200,
     "desc": "The ROI on this is debatable.",                "sheet_img": "office_items_sheet"},
    {"id": "trophy_case",     "name": "Trophy Display Case","cost": 350,
     "desc": "For the deal tombstones you've collected.",    "sheet_img": "office_items_sheet"},
    {"id": "coat_stand",      "name": "Mahogany Coat Stand","cost": 150,
     "desc": "For the overcoat you wear to signal you own one.","sheet_img": "office_items_sheet"},
]
DECORATION_BY_ID = {d["id"]: d for d in DECORATION_ITEMS}

# ═══════════════════════════════════════════════════════════════════════════
#  OFFICE TIERS
# ═══════════════════════════════════════════════════════════════════════════

OFFICE_TIERS = {
    1: {"name": "Cubicle",          "cost": 0,    "xp_req": 0},
    2: {"name": "Shared Office",    "cost": 500,  "xp_req": 300},
    3: {"name": "Corner Office",    "cost": 2000, "xp_req": 1500},
    4: {"name": "Penthouse Suite",  "cost": 8000, "xp_req": 5000},
}

# ═══════════════════════════════════════════════════════════════════════════
#  ALPHA PACK ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def _weighted_rarity() -> dict:
    """Roll a rarity using the defined probability weights."""
    population = [r["id"] for r in RARITY_TIERS]
    weights    = [r["weight"] for r in RARITY_TIERS]
    chosen_id  = random.choices(population, weights=weights, k=1)[0]
    return RARITY_BY_ID[chosen_id]


def _random_item_of_rarity(rarity_id: str) -> dict:
    pool = [c for c in CLOTHING_ITEMS if c["rarity"] == rarity_id]
    if not pool:
        pool = CLOTHING_ITEMS  # fallback
    return random.choice(pool)


def roll_alpha_pack(user_id: int) -> dict:
    """
    Deduct ALPHA_PACK_COST bps, roll an item, return result dict:
      {success, item, rarity, spin_items, error}
    spin_items: 21-item list for the frontend ticker (20 decoys + winner last)
    """
    if not storage.spend_bps(user_id, ALPHA_PACK_COST):
        return {"success": False, "error": f"Need {ALPHA_PACK_COST} bps to open an Alpha Pack."}

    rarity  = _weighted_rarity()
    item    = _random_item_of_rarity(rarity["id"])

    # Check if user already owns it
    user    = storage.get_user(user_id)
    owned   = storage.get_owned_clothing(user)
    if item["id"] not in owned:
        storage.add_clothing_item(user_id, item["id"])
    # Log the pull
    storage.log_alpha_pack(user_id, item["id"], rarity["id"], ALPHA_PACK_COST)
    # Check monopolist set
    _check_monopolist(user_id)

    # Build 21-item spin sequence (20 random filler + winning item at position 20)
    spin_items = []
    for _ in range(20):
        filler_rarity = _weighted_rarity()
        filler_item   = _random_item_of_rarity(filler_rarity["id"])
        spin_items.append({
            "id": filler_item["id"], "name": filler_item["name"],
            "rarity": filler_rarity["id"], "color": filler_rarity["color"],
        })
    spin_items.append({
        "id": item["id"], "name": item["name"],
        "rarity": rarity["id"], "color": rarity["color"],
    })

    return {
        "success": True,
        "item": item,
        "rarity": rarity,
        "spin_items": spin_items,
    }


def _check_monopolist(user_id: int):
    user = storage.get_user(user_id)
    owned = set(storage.get_owned_clothing(user))
    if MONOPOLIST_SET.issubset(owned):
        storage.update_user(user_id, unlocked_monopolist=1)


def calculate_outfit_boosters(user: dict) -> dict:
    """Return {xp_mult, bps_mult} from 1.0 base + equipped clothing bonuses."""
    outfit  = storage.get_equipped_outfit(user)
    xp_add  = 0.0
    bps_add = 0.0
    for slot, item_id in outfit.items():
        item = CLOTHING_BY_ID.get(item_id)
        if item:
            xp_add  += item.get("xp_booster", 0)
            bps_add += item.get("bps_booster", 0)
    return {"xp_mult": 1.0 + xp_add, "bps_mult": 1.0 + bps_add}


def upgrade_office(user_id: int, target_tier: int) -> tuple[bool, str]:
    user = storage.get_user(user_id)
    tier_info = OFFICE_TIERS.get(target_tier)
    if not tier_info:
        return False, "Invalid tier."
    if user.get("office_tier", 1) >= target_tier:
        return False, "Already at this tier or higher."
    if user.get("xp", 0) < tier_info["xp_req"]:
        return False, f"Need {tier_info['xp_req']:,} XP to unlock {tier_info['name']}."
    if not storage.spend_bps(user_id, tier_info["cost"]):
        return False, f"Need {tier_info['cost']:,} bps for {tier_info['name']}."
    storage.update_user(user_id, office_tier=target_tier)
    return True, f"Welcome to your {tier_info['name']}."
