# The Desk

Spaced-repetition learning for asset management recruiting. Fully offline. Python + Streamlit + SQLite.

## Setup (Windows)

**Requirements:** Python 3.9+ ([python.org](https://python.org))

```powershell
# 1. Clone the repo (or navigate to the folder)
cd C:\Users\gcros\Documents\the-desk

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

## First run

- Create a profile on the login screen.
- Take the placement diagnostic (or skip it).
- The skill tree shows available lessons. Locked lessons unlock when prerequisites are mastered.

## Adding content

Drop lesson JSON files into `content/` — they're picked up automatically on next launch.
Or use the **Add Content** screen in the app to upload and validate a file without touching the filesystem.

Lesson files must follow the schema. The app validates on load and shows a clear error if anything's wrong.

## For club members who clone this repo

```powershell
git clone https://github.com/YOURNAME/the-desk.git
cd the-desk
pip install -r requirements.txt
streamlit run app.py
```

Your progress is stored in `data/desk.db` (local only, gitignored). Everyone has their own.

## Project structure

```
app.py              # Streamlit entry point
storage.py          # All DB access — swap SQLite for Postgres here
scheduler.py        # SM-2 spaced repetition + mastery decay
content_loader.py   # JSON loading and validation
gamification.py     # XP, levels, bps, titles, cosmetics
rewards.py          # Reward card copy pool
components/         # UI renderers
content/            # Lesson JSON files
data/               # SQLite database (gitignored)
```
