# Phase 2 Deployment Guide

This is a stub for future hosted deployment. The app is designed for this — it just needs a database swap and a host.

## What changes

Only `storage.py` needs to change. Everything else stays identical.

## Steps

1. **Create a free Postgres instance** — Supabase (supabase.com) or Neon (neon.tech) both have free tiers. Copy the connection string.

2. **Set the environment variable**
   ```
   DATABASE_URL=postgresql://user:password@host/dbname
   ```
   When `DATABASE_URL` is set, `storage.py` uses Postgres automatically. When it's unset, it uses local SQLite.

3. **Install psycopg2**
   ```
   pip install psycopg2-binary
   ```

4. **Deploy to Streamlit Community Cloud**
   - Push the repo to GitHub (keep `data/` in `.gitignore`)
   - Go to share.streamlit.io, connect your repo, set `DATABASE_URL` as a secret
   - The app runs at a public URL — share it with the club

5. **Multi-user profiles** already work. The login screen lets each club member create and switch profiles. All progress is keyed by `user_id`, never shared.

## What this unlocks

- Progress syncs across your own machines (laptop + desktop)
- Club members get a shared URL instead of needing to clone the repo
- No code changes required — it's a one-variable swap
