"""
Load and validate all lesson JSON files from content/.
Accepts two file shapes:

  Shape 1 — single lesson object (id at top level):
    { "id": "A1", "track": "A", ..., "questions": [...] }

  Shape 2 — container holding multiple lessons (no id at top level):
    { "track": "A", "track_name": "...", "lessons": [ {lesson}, {lesson} ] }

Also accepts jargon files with a top-level "terms" array.
Fails loudly with a clear message naming the offending file/field.
"""
import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

VALID_SECTION_TYPES    = {"text", "callout", "formula"}
VALID_CALLOUT_VARIANTS = {"interview_trap", "key_insight", "watch_out"}
VALID_QUESTION_TYPES   = {"mcq", "numeric", "fill_blank", "ordering", "matching", "free_response"}


class ContentError(Exception):
    pass


def _require(obj: dict, field: str, label: str, typ=None):
    if field not in obj:
        raise ContentError(f"[{label}] Missing required field: '{field}'")
    if typ is not None and not isinstance(obj[field], typ):
        raise ContentError(
            f"[{label}] Field '{field}' must be {typ.__name__}, "
            f"got {type(obj[field]).__name__}"
        )
    return obj[field]


def validate_lesson(data: dict, label: str) -> dict:
    """Validate a single lesson object. Raises ContentError on any violation."""
    # Coerce unit/order to str — schema allows integers here
    for coerce_field in ("unit", "unit_name", "order"):
        if coerce_field in data and not isinstance(data[coerce_field], str):
            data[coerce_field] = str(data[coerce_field])

    for f in ("id", "title", "track", "track_name", "unit", "why_it_matters"):
        _require(data, f, label, str)

    # unit_name is optional (some files omit it — default to unit value)
    if "unit_name" not in data:
        data["unit_name"] = data.get("unit", "")

    _require(data, "prerequisites", label, list)

    concept = _require(data, "concept", label, list)
    for i, sec in enumerate(concept):
        slabel = f"{label} concept[{i}]"
        if "type" not in sec:
            raise ContentError(f"[{slabel}] Missing 'type'")
        if sec["type"] not in VALID_SECTION_TYPES:
            raise ContentError(f"[{slabel}] Unknown section type '{sec['type']}'. Valid: {VALID_SECTION_TYPES}")
        if sec["type"] == "callout" and sec.get("variant") not in VALID_CALLOUT_VARIANTS:
            raise ContentError(f"[{slabel}] Callout must have variant in {VALID_CALLOUT_VARIANTS}")
        if sec["type"] in ("text", "callout") and "body" not in sec:
            raise ContentError(f"[{slabel}] Section type '{sec['type']}' requires 'body'")
        if sec["type"] == "formula":
            # "heading" and "label" are interchangeable; "body" and "expression" likewise
            if "label" not in sec and "heading" not in sec:
                raise ContentError(f"[{slabel}] Formula section requires 'label' or 'heading'")
            if "expression" not in sec and "body" not in sec:
                raise ContentError(f"[{slabel}] Formula section requires 'expression' or 'body'")

    we = _require(data, "worked_example", label, dict)
    # Accept both schema shapes: {title,body} and {title,setup,steps,takeaway}
    _require(we, "title", f"{label} worked_example", str)
    if "body" not in we and "setup" not in we:
        raise ContentError(f"[{label}] worked_example requires 'body' or 'setup'+'steps'+'takeaway'")

    glossary = _require(data, "glossary", label, list)
    for i, g in enumerate(glossary):
        for ff in ("term", "definition"):
            _require(g, ff, f"{label} glossary[{i}]", str)

    questions = _require(data, "questions", label, list)
    seen_ids = set()
    for i, q in enumerate(questions):
        qlabel = f"{label} questions[{i}]"
        qid = _require(q, "id", qlabel, str)
        if qid in seen_ids:
            raise ContentError(f"[{qlabel}] Duplicate question id '{qid}'")
        seen_ids.add(qid)
        qt = _require(q, "type", qlabel, str)
        if qt not in VALID_QUESTION_TYPES:
            raise ContentError(f"[{qlabel}] Unknown question type '{qt}'. Valid: {VALID_QUESTION_TYPES}")
        _require(q, "prompt", qlabel, str)
        _require(q, "explanation", qlabel, str)

        if qt == "mcq":
            _require(q, "choices", qlabel, list)
            _require(q, "answer_index", qlabel, int)
        elif qt == "numeric":
            _require(q, "answer", qlabel)
            _require(q, "tolerance", qlabel)
            _require(q, "unit", qlabel, str)
        elif qt == "fill_blank":
            _require(q, "accepted", qlabel, list)
        elif qt == "ordering":
            _require(q, "items", qlabel, list)
        elif qt == "matching":
            pairs = _require(q, "pairs", qlabel, list)
            for j, p in enumerate(pairs):
                for side in ("left", "right"):
                    _require(p, side, f"{qlabel} pairs[{j}]", str)
        elif qt == "free_response":
            _require(q, "model_answer", qlabel, str)
            _require(q, "rubric", qlabel, list)

    cr = _require(data, "completion_reward", label, dict)
    _require(cr, "title", f"{label} completion_reward", str)
    # Schema uses "copy" or "body" interchangeably
    if "body" not in cr and "copy" not in cr:
        raise ContentError(f"[{label} completion_reward] Missing required field: 'body' or 'copy'")

    return data


def validate_jargon(data: dict, label: str) -> dict:
    terms = _require(data, "terms", label, list)
    for i, t in enumerate(terms):
        _require(t, "term",       f"{label} terms[{i}]", str)
        _require(t, "definition", f"{label} terms[{i}]", str)
    return data


def _extract_lessons_from_file(path: Path) -> list:
    """
    Parse one JSON file and return a list of validated lesson dicts.
    Handles both shapes and jargon files (returns [] for jargon).
    Raises ContentError with the file name on any problem.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ContentError(f"[{path.name}] Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise ContentError(f"[{path.name}] Top-level value must be a JSON object.")

    # Jargon file — skip
    if "terms" in data:
        return []

    # Shape 2: container with a "lessons" array
    if "lessons" in data:
        raw_lessons = data["lessons"]
        if not isinstance(raw_lessons, list):
            raise ContentError(f"[{path.name}] 'lessons' must be an array.")
        results = []
        for i, lesson in enumerate(raw_lessons):
            if not isinstance(lesson, dict):
                raise ContentError(f"[{path.name}] lessons[{i}] must be an object.")
            # Inherit track/track_name/unit/unit_name from container if missing
            for inherit_field in ("track", "track_name", "unit", "unit_name"):
                if inherit_field not in lesson and inherit_field in data:
                    lesson[inherit_field] = data[inherit_field]
            # Coerce container-level unit to str before inheritance check
            for coerce_field in ("unit", "order"):
                if coerce_field in data and not isinstance(data[coerce_field], str):
                    data[coerce_field] = str(data[coerce_field])
            label = f"{path.name} lessons[{i}]"
            results.append(validate_lesson(lesson, label))
        return results

    # Shape 1: single lesson object
    return [validate_lesson(data, path.name)]


def load_lesson_file(path: Path) -> list:
    """Public entry point used by the uploader. Returns list of lesson dicts."""
    return _extract_lessons_from_file(path)


def load_all_lessons() -> dict:
    """Load every *.json in content/ (except jargon.json). Returns {id: lesson}."""
    lessons = {}
    errors  = []

    for path in sorted(CONTENT_DIR.glob("*.json")):
        if path.name == "jargon.json":
            continue
        try:
            for lesson in _extract_lessons_from_file(path):
                lid = lesson["id"]
                if lid in lessons:
                    errors.append(
                        f"[{path.name}] Duplicate lesson id '{lid}' "
                        f"(already loaded from another file)"
                    )
                else:
                    lessons[lid] = lesson
        except ContentError as e:
            errors.append(str(e))

    if errors:
        raise ContentError("Content errors:\n" + "\n".join(errors))
    return lessons


def load_jargon() -> list:
    path = CONTENT_DIR / "jargon.json"
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        # Accept {"terms": [...]} or {"jargon": [...]}
        terms = data.get("jargon") or data.get("terms") or []
        return terms
    except Exception as e:
        raise ContentError(f"jargon.json is invalid: {e}")


def save_lesson_file(data: dict) -> Path:
    """Save a single validated lesson dict to content/<id>.json."""
    path = CONTENT_DIR / f"{data['id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


def build_track_tree(lessons: dict) -> dict:
    """Return {track: {track_name, units: {unit: {unit_name, lessons: [...]}}}}"""
    tree = {}
    for lesson in lessons.values():
        track = lesson["track"]
        if track not in tree:
            tree[track] = {"track_name": lesson["track_name"], "units": {}}
        unit = lesson["unit"]
        if unit not in tree[track]["units"]:
            tree[track]["units"][unit] = {"unit_name": lesson["unit_name"], "lessons": []}
        tree[track]["units"][unit]["lessons"].append(lesson)
    for track in tree.values():
        for unit in track["units"].values():
            unit["lessons"].sort(key=lambda l: l["id"])
    return dict(sorted(tree.items()))
