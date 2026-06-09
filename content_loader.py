"""
Load and validate all lesson JSON files from content/.
Fails loudly on schema violations — bad content cannot silently break the app.
"""
import json
from pathlib import Path
from typing import Any

CONTENT_DIR = Path(__file__).parent / "content"

VALID_SECTION_TYPES = {"text", "callout", "formula"}
VALID_CALLOUT_VARIANTS = {"interview_trap", "key_insight", "watch_out"}
VALID_QUESTION_TYPES = {"mcq", "numeric", "fill_blank", "ordering", "matching", "free_response"}


class ContentError(Exception):
    pass


def _require(obj: dict, field: str, file_label: str, typ=None):
    if field not in obj:
        raise ContentError(f"[{file_label}] Missing required field: '{field}'")
    if typ is not None and not isinstance(obj[field], typ):
        raise ContentError(f"[{file_label}] Field '{field}' must be {typ.__name__}, got {type(obj[field]).__name__}")
    return obj[field]


def validate_lesson(data: dict, file_label: str) -> dict:
    for f in ("id", "title", "track", "track_name", "unit", "unit_name", "why_it_matters"):
        _require(data, f, file_label, str)

    _require(data, "prerequisites", file_label, list)
    concept = _require(data, "concept", file_label, list)
    for i, sec in enumerate(concept):
        label = f"{file_label} concept[{i}]"
        if "type" not in sec:
            raise ContentError(f"[{label}] Missing 'type'")
        if sec["type"] not in VALID_SECTION_TYPES:
            raise ContentError(f"[{label}] Unknown section type '{sec['type']}'. Valid: {VALID_SECTION_TYPES}")
        if sec["type"] == "callout":
            if sec.get("variant") not in VALID_CALLOUT_VARIANTS:
                raise ContentError(f"[{label}] Callout must have variant in {VALID_CALLOUT_VARIANTS}")
        if sec["type"] in ("text", "callout") and "body" not in sec:
            raise ContentError(f"[{label}] Section type '{sec['type']}' requires 'body'")
        if sec["type"] == "formula":
            for ff in ("label", "expression"):
                if ff not in sec:
                    raise ContentError(f"[{label}] Formula section requires '{ff}'")

    we = _require(data, "worked_example", file_label, dict)
    for ff in ("title", "body"):
        _require(we, ff, f"{file_label} worked_example", str)

    glossary = _require(data, "glossary", file_label, list)
    for i, g in enumerate(glossary):
        for ff in ("term", "definition"):
            _require(g, ff, f"{file_label} glossary[{i}]", str)

    questions = _require(data, "questions", file_label, list)
    seen_ids = set()
    for i, q in enumerate(questions):
        label = f"{file_label} questions[{i}]"
        qid = _require(q, "id", label, str)
        if qid in seen_ids:
            raise ContentError(f"[{label}] Duplicate question id '{qid}'")
        seen_ids.add(qid)
        qt = _require(q, "type", label, str)
        if qt not in VALID_QUESTION_TYPES:
            raise ContentError(f"[{label}] Unknown question type '{qt}'")
        _require(q, "prompt", label, str)
        _require(q, "explanation", label, str)

        if qt == "mcq":
            _require(q, "choices", label, list)
            _require(q, "answer_index", label, int)
        elif qt == "numeric":
            _require(q, "answer", label)
            _require(q, "tolerance", label)
            _require(q, "unit", label, str)
        elif qt == "fill_blank":
            _require(q, "accepted", label, list)
        elif qt == "ordering":
            _require(q, "items", label, list)
        elif qt == "matching":
            pairs = _require(q, "pairs", label, list)
            for j, p in enumerate(pairs):
                for side in ("left", "right"):
                    _require(p, side, f"{label} pairs[{j}]", str)
        elif qt == "free_response":
            _require(q, "model_answer", label, str)
            _require(q, "rubric", label, list)

    cr = _require(data, "completion_reward", file_label, dict)
    _require(cr, "title", f"{file_label} completion_reward", str)
    _require(cr, "body", f"{file_label} completion_reward", str)

    return data


def validate_jargon(data: dict, file_label: str) -> dict:
    terms = _require(data, "terms", file_label, list)
    for i, t in enumerate(terms):
        _require(t, "term", f"{file_label} terms[{i}]", str)
        _require(t, "definition", f"{file_label} terms[{i}]", str)
    return data


def load_lesson_file(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ContentError(f"[{path.name}] Invalid JSON: {e}")
    return validate_lesson(data, path.name)


def load_all_lessons() -> dict:
    lessons = {}
    errors = []
    for path in sorted(CONTENT_DIR.glob("*.json")):
        if path.name == "jargon.json":
            continue
        try:
            lesson = load_lesson_file(path)
            lid = lesson["id"]
            if lid in lessons:
                errors.append(f"[{path.name}] Duplicate lesson id '{lid}' (already loaded from another file)")
            else:
                lessons[lid] = lesson
        except ContentError as e:
            errors.append(str(e))
    if errors:
        raise ContentError("Content errors found:\n" + "\n".join(errors))
    return lessons


def load_jargon() -> list:
    path = CONTENT_DIR / "jargon.json"
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        validate_jargon(data, "jargon.json")
        return data["terms"]
    except ContentError as e:
        raise ContentError(f"jargon.json is invalid: {e}")


def save_lesson_file(data: dict) -> Path:
    """Save a validated lesson dict to content/ and return its path."""
    path = CONTENT_DIR / f"{data['id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


def build_track_tree(lessons: dict) -> dict:
    """Return {track_letter: {track_name, units: {unit: {unit_name, lessons: [lesson]}}}}"""
    tree = {}
    for lesson in lessons.values():
        track = lesson["track"]
        if track not in tree:
            tree[track] = {"track_name": lesson["track_name"], "units": {}}
        unit = lesson["unit"]
        if unit not in tree[track]["units"]:
            tree[track]["units"][unit] = {"unit_name": lesson["unit_name"], "lessons": []}
        tree[track]["units"][unit]["lessons"].append(lesson)
    # sort lessons within each unit by id
    for track in tree.values():
        for unit in track["units"].values():
            unit["lessons"].sort(key=lambda l: l["id"])
    return dict(sorted(tree.items()))
