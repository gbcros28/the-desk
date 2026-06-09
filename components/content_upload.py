"""In-app lesson upload with schema validation."""
import json
import tempfile
import os
from pathlib import Path
import streamlit as st
import content_loader


def _tmp_path(filename: str, raw: str) -> Path:
    """Write raw JSON string to a temp file so load_lesson_file can parse it."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False,
        encoding="utf-8", prefix=filename.replace(".json", "_")
    )
    tmp.write(raw)
    tmp.close()
    return Path(tmp.name)


def render_content_upload():
    st.markdown("## Add Content")
    st.caption("Upload a lesson JSON file. It will be validated against the schema before saving.")

    uploaded = st.file_uploader("Choose a lesson JSON file", type=["json"])
    if not uploaded:
        return

    try:
        raw = uploaded.read().decode("utf-8")
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        st.error(f"❌ Invalid JSON: {e}")
        return
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")
        return

    # Validate strictly — never execute, treat as pure data
    try:
        validated_lessons = content_loader.load_lesson_file(
            _tmp_path(uploaded.name, raw)
        )
    except content_loader.ContentError as e:
        st.error(f"❌ Validation failed:\n\n{e}")
        return

    if not validated_lessons:
        st.warning("No lessons found in this file (jargon files go in content/jargon.json).")
        return

    st.success(f"✅ Validation passed — {len(validated_lessons)} lesson(s) found")
    for v in validated_lessons:
        st.json({"id": v["id"], "title": v["title"], "track": v["track"],
                 "unit": v["unit"], "questions": len(v["questions"])})

    # Check for duplicates
    existing = [v for v in validated_lessons
                if (content_loader.CONTENT_DIR / f"{v['id']}.json").exists()]
    if existing:
        ids = ", ".join(f"`{v['id']}`" for v in existing)
        st.warning(f"⚠️ These lesson ids already exist and will be overwritten: {ids}")

    if st.button(f"Save {len(validated_lessons)} lesson(s)"):
        for v in validated_lessons:
            _save_and_reload(v)


def _save_and_reload(validated: dict):
    path = content_loader.save_lesson_file(validated)
    st.success(f"Saved to {path.name}. Reloading content tree...")
    # force content reload on next run
    if "lessons" in st.session_state:
        del st.session_state["lessons"]
    if "track_tree" in st.session_state:
        del st.session_state["track_tree"]
    st.rerun()
