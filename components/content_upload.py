"""In-app lesson upload with schema validation."""
import json
import streamlit as st
import content_loader


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
        validated = content_loader.validate_lesson(data, uploaded.name)
    except content_loader.ContentError as e:
        st.error(f"❌ Validation failed:\n\n{e}")
        return

    lid = validated["id"]
    existing_path = content_loader.CONTENT_DIR / f"{lid}.json"
    is_duplicate = existing_path.exists()

    st.success(f"✅ Validation passed: **{validated['title']}** (id: `{lid}`)")
    st.json({"id": lid, "title": validated["title"], "track": validated["track"],
             "unit": validated["unit"], "questions": len(validated["questions"])})

    if is_duplicate:
        st.warning(f"⚠️ A lesson with id `{lid}` already exists. Saving will overwrite it.")
        if st.button("Overwrite existing lesson"):
            _save_and_reload(validated)
    else:
        if st.button("Save lesson"):
            _save_and_reload(validated)


def _save_and_reload(validated: dict):
    path = content_loader.save_lesson_file(validated)
    st.success(f"Saved to {path.name}. Reloading content tree...")
    # force content reload on next run
    if "lessons" in st.session_state:
        del st.session_state["lessons"]
    if "track_tree" in st.session_state:
        del st.session_state["track_tree"]
    st.rerun()
