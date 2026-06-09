"""
All DB reads/writes go through this module.
To switch to Postgres: set DATABASE_URL env var to a postgres:// connection string.
No raw SQL anywhere else in the codebase.
"""
import os
import json
import sqlite3
from pathlib import Path
from typing import Optional
from datetime import date, datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "")
DB_PATH = Path(__file__).parent / "data" / "desk.db"


def _get_connection():
    if DATABASE_URL and DATABASE_URL.startswith("postgres"):
        try:
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except ImportError:
            raise RuntimeError("psycopg2 not installed for Postgres backend")
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_connection()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name      TEXT NOT NULL UNIQUE,
        xp        INTEGER DEFAULT 0,
        bps       INTEGER DEFAULT 0,
        level     INTEGER DEFAULT 1,
        streak    INTEGER DEFAULT 0,
        last_active TEXT,
        streak_freeze INTEGER DEFAULT 0,
        daily_goal    INTEGER DEFAULT 5,
        daily_done    INTEGER DEFAULT 0,
        owned_cosmetics TEXT DEFAULT '[]',
        equipped        TEXT DEFAULT '{}',
        title           TEXT DEFAULT 'Intern',
        created_at      TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS progress (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL,
        question_id  TEXT NOT NULL,
        lesson_id    TEXT NOT NULL,
        ease_factor  REAL DEFAULT 2.5,
        interval     INTEGER DEFAULT 0,
        repetitions  INTEGER DEFAULT 0,
        due_date     TEXT,
        last_grade   INTEGER DEFAULT 0,
        mastery      REAL DEFAULT 0.0,
        UNIQUE(user_id, question_id)
    );

    CREATE TABLE IF NOT EXISTS lesson_progress (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL,
        lesson_id    TEXT NOT NULL,
        completed    INTEGER DEFAULT 0,
        completed_at TEXT,
        mastery      REAL DEFAULT 0.0,
        UNIQUE(user_id, lesson_id)
    );

    CREATE TABLE IF NOT EXISTS stock_pitches (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL,
        ticker       TEXT NOT NULL,
        thesis       TEXT DEFAULT '',
        catalysts    TEXT DEFAULT '',
        valuation    TEXT DEFAULT '',
        risks        TEXT DEFAULT '',
        variant_view TEXT DEFAULT '',
        updated_at   TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, ticker)
    );

    CREATE TABLE IF NOT EXISTS milestones (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL,
        milestone_key TEXT NOT NULL,
        achieved_at  TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, milestone_key)
    );

    CREATE TABLE IF NOT EXISTS todos (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        text       TEXT NOT NULL,
        due_date   TEXT,
        done       INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS calendar_events (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        title      TEXT NOT NULL,
        event_date TEXT NOT NULL,
        note       TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS streak_log (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        UNIQUE(user_id, log_date)
    );
    """)
    conn.commit()
    conn.close()


# --- Users ---

def get_all_users() -> list:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY name")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_user(user_id: int) -> Optional[dict]:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_name(name: str) -> Optional[dict]:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(name: str) -> dict:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return get_user(uid)


def update_user(user_id: int, **kwargs):
    if not kwargs:
        return
    conn = _get_connection()
    cur = conn.cursor()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    cur.execute(f"UPDATE users SET {sets} WHERE user_id = ?", vals)
    conn.commit()
    conn.close()


def add_xp(user_id: int, amount: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()


def add_bps(user_id: int, amount: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET bps = bps + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()


def spend_bps(user_id: int, amount: int) -> bool:
    user = get_user(user_id)
    if not user or user["bps"] < amount:
        return False
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET bps = bps - ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()
    return True


def record_streak(user_id: int):
    today_d = date.today()
    today = str(today_d)
    user = get_user(user_id)
    if not user:
        return
    last = user.get("last_active") or ""
    if last == today:
        return
    if last:
        last_d = date.fromisoformat(last)
        delta = (today_d - last_d).days
        if delta == 1:
            new_streak = user["streak"] + 1
        elif delta == 2 and user.get("streak_freeze", 0) > 0:
            new_streak = user["streak"] + 1
            conn = _get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET streak_freeze = streak_freeze - 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
        else:
            new_streak = 1
    else:
        new_streak = 1
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET streak = ?, last_active = ?, daily_done = 0 WHERE user_id = ?",
                (new_streak, today, user_id))
    conn.commit()
    conn.close()
    log_streak_day(user_id, today)


def increment_daily_done(user_id: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET daily_done = daily_done + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# --- Card progress (SM-2) ---

def upsert_progress(user_id: int, question_id: str, lesson_id: str,
                    ease_factor: float, interval: int, repetitions: int,
                    due_date: str, last_grade: int, mastery: float):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO progress
            (user_id, question_id, lesson_id, ease_factor, interval, repetitions, due_date, last_grade, mastery)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, question_id) DO UPDATE SET
            ease_factor=excluded.ease_factor,
            interval=excluded.interval,
            repetitions=excluded.repetitions,
            due_date=excluded.due_date,
            last_grade=excluded.last_grade,
            mastery=excluded.mastery
    """, (user_id, question_id, lesson_id, ease_factor, interval, repetitions, due_date, last_grade, mastery))
    conn.commit()
    conn.close()


def get_progress(user_id: int, question_id: str) -> Optional[dict]:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM progress WHERE user_id = ? AND question_id = ?", (user_id, question_id))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_due_cards(user_id: int) -> list:
    today = str(date.today())
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM progress
        WHERE user_id = ? AND (due_date IS NULL OR due_date <= ?)
    """, (user_id, today))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_all_progress_for_user(user_id: int) -> list:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM progress WHERE user_id = ?", (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# --- Lesson progress ---

def get_lesson_progress(user_id: int, lesson_id: str) -> Optional[dict]:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lesson_progress WHERE user_id = ? AND lesson_id = ?", (user_id, lesson_id))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_lesson_progress(user_id: int) -> dict:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lesson_progress WHERE user_id = ?", (user_id,))
    rows = {r["lesson_id"]: dict(r) for r in cur.fetchall()}
    conn.close()
    return rows


def upsert_lesson_progress(user_id: int, lesson_id: str, completed: bool, mastery: float):
    conn = _get_connection()
    cur = conn.cursor()
    completed_at = str(date.today()) if completed else None
    cur.execute("""
        INSERT INTO lesson_progress (user_id, lesson_id, completed, completed_at, mastery)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, lesson_id) DO UPDATE SET
            completed=MAX(lesson_progress.completed, excluded.completed),
            completed_at=COALESCE(lesson_progress.completed_at, excluded.completed_at),
            mastery=excluded.mastery
    """, (user_id, lesson_id, int(completed), completed_at, mastery))
    conn.commit()
    conn.close()


# --- Stock pitches ---

def save_stock_pitch(user_id: int, ticker: str, thesis: str, catalysts: str,
                     valuation: str, risks: str, variant_view: str) -> int:
    conn = _get_connection()
    cur = conn.cursor()
    now = str(datetime.now())
    ticker = ticker.upper()
    cur.execute("""
        INSERT INTO stock_pitches (user_id, ticker, thesis, catalysts, valuation, risks, variant_view, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, ticker) DO UPDATE SET
            thesis=excluded.thesis, catalysts=excluded.catalysts, valuation=excluded.valuation,
            risks=excluded.risks, variant_view=excluded.variant_view, updated_at=excluded.updated_at
    """, (user_id, ticker, thesis, catalysts, valuation, risks, variant_view, now))
    conn.commit()
    cur.execute("SELECT id FROM stock_pitches WHERE user_id = ? AND ticker = ?", (user_id, ticker))
    pid = cur.fetchone()["id"]
    conn.close()
    return pid


def get_stock_pitches(user_id: int) -> list:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock_pitches WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_stock_pitch(user_id: int, ticker: str) -> Optional[dict]:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock_pitches WHERE user_id = ? AND ticker = ?", (user_id, ticker.upper()))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


# --- Milestones ---

def check_milestone(user_id: int, key: str) -> bool:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM milestones WHERE user_id = ? AND milestone_key = ?", (user_id, key))
    row = cur.fetchone()
    conn.close()
    return row is not None


def record_milestone(user_id: int, key: str) -> bool:
    if check_milestone(user_id, key):
        return False
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO milestones (user_id, milestone_key) VALUES (?, ?)", (user_id, key))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def get_streaks_this_week() -> list:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, streak, last_active FROM users
        WHERE streak > 0 AND last_active >= date('now', '-7 days')
        ORDER BY streak DESC LIMIT 10
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# --- To-do list ---

def get_todos(user_id: int, include_done: bool = False) -> list:
    conn = _get_connection()
    cur = conn.cursor()
    if include_done:
        cur.execute("SELECT * FROM todos WHERE user_id = ? ORDER BY due_date ASC, created_at ASC", (user_id,))
    else:
        cur.execute("SELECT * FROM todos WHERE user_id = ? AND done = 0 ORDER BY due_date ASC, created_at ASC", (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def add_todo(user_id: int, text: str, due_date: str = None) -> int:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (user_id, text, due_date) VALUES (?, ?, ?)", (user_id, text, due_date))
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    return tid


def complete_todo(todo_id: int, user_id: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET done = 1 WHERE id = ? AND user_id = ?", (todo_id, user_id))
    conn.commit()
    conn.close()


def delete_todo(todo_id: int, user_id: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
    conn.commit()
    conn.close()


# --- Calendar events ---

def get_calendar_events(user_id: int, year: int, month: int) -> list:
    conn = _get_connection()
    cur = conn.cursor()
    prefix = f"{year}-{month:02d}"
    cur.execute("SELECT * FROM calendar_events WHERE user_id = ? AND event_date LIKE ? ORDER BY event_date",
                (user_id, f"{prefix}%"))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def add_calendar_event(user_id: int, title: str, event_date: str, note: str = "") -> int:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO calendar_events (user_id, title, event_date, note) VALUES (?, ?, ?, ?)",
                (user_id, title, event_date, note))
    eid = cur.lastrowid
    conn.commit()
    conn.close()
    return eid


def delete_calendar_event(event_id: int, user_id: int):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM calendar_events WHERE id = ? AND user_id = ?", (event_id, user_id))
    conn.commit()
    conn.close()


def get_all_calendar_events(user_id: int) -> list:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM calendar_events WHERE user_id = ? ORDER BY event_date", (user_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# --- Streak log ---

def log_streak_day(user_id: int, log_date: str = None):
    from datetime import date as dt
    log_date = log_date or str(dt.today())
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT OR IGNORE INTO streak_log (user_id, log_date) VALUES (?, ?)", (user_id, log_date))
        conn.commit()
    except Exception:
        pass
    conn.close()


def get_streak_log(user_id: int, year: int, month: int) -> set:
    conn = _get_connection()
    cur = conn.cursor()
    prefix = f"{year}-{month:02d}"
    cur.execute("SELECT log_date FROM streak_log WHERE user_id = ? AND log_date LIKE ?",
                (user_id, f"{prefix}%"))
    dates = {r["log_date"] for r in cur.fetchall()}
    conn.close()
    return dates


# ── Admin / dev shortcut ──────────────────────────────────────────────────

ADMIN_FLAG_KEY = "admin_perks_applied"

def is_admin_name(name: str) -> bool:
    return name.strip().lower() == "billybob"


def apply_admin_perks(user_id: int, lessons: dict = None):
    """
    Grant the billybob account everything:
    - 999,999 XP + bps, max level/title
    - All cosmetics unlocked (no cost deducted)
    - All lessons marked complete at 100% mastery
    - 365-day streak
    Only runs once per user_id (tracked via a milestone flag).
    """
    if check_milestone(user_id, ADMIN_FLAG_KEY):
        return   # already applied

    import json as _json

    # Pull all shop item IDs and grant them for free
    from gamification import SHOP_ITEMS, TITLES, LEVELS
    all_cosmetics = [
        item["id"] for item in SHOP_ITEMS if item["category"] != "consumable"
    ]
    # Also give a pile of streak freezes
    streak_freezes = 99

    # Best title + level
    max_xp    = 9_999_999
    max_level = LEVELS[-1][1]
    max_title = TITLES[-1][1]

    equipped = _json.dumps({
        "theme":    "gold_theme",
        "cosmetic": "vest",
    })

    update_user(
        user_id,
        xp              = max_xp,
        bps             = 9_999_999,
        level           = max_level,
        title           = max_title,
        streak          = 365,
        streak_freeze   = streak_freezes,
        owned_cosmetics = _json.dumps(all_cosmetics),
        equipped        = equipped,
    )

    # Mark all loaded lessons complete at 100%
    if lessons:
        from datetime import date as _date
        today = str(_date.today())
        conn = _get_connection()
        cur  = conn.cursor()
        for lid in lessons:
            cur.execute("""
                INSERT INTO lesson_progress (user_id, lesson_id, completed, completed_at, mastery)
                VALUES (?, ?, 1, ?, 100.0)
                ON CONFLICT(user_id, lesson_id) DO UPDATE SET
                    completed=1, completed_at=?, mastery=100.0
            """, (user_id, lid, today, today))
        conn.commit()
        conn.close()

    record_milestone(user_id, ADMIN_FLAG_KEY)
