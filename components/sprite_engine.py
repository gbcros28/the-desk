"""
Sprite loading + composite rendering for the office scene.
All sprites are served as base64 data-URIs so Streamlit doesn't need
a separate static file server.
"""
import base64, io, os
from functools import lru_cache
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "assets" / "processed"


@lru_cache(maxsize=64)
def _img_b64(filename: str) -> str:
    """Load a processed PNG and return a data-URI string (cached)."""
    path = PROCESSED / filename
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def img_tag(filename: str, width: str = "100%", extra_style: str = "") -> str:
    src = _img_b64(filename)
    if not src:
        return ""
    return f'<img src="{src}" style="width:{width};{extra_style}" />'


def composite_html(layers: list[dict], container_style: str = "") -> str:
    """
    Render a list of absolutely-positioned image layers.
    Each layer: {file, left, top, width, z, extra_style (optional)}
    container_style: additional CSS on the outer wrapper.
    """
    inner = ""
    for layer in layers:
        src = _img_b64(layer["file"])
        if not src:
            continue
        z    = layer.get("z", 1)
        left = layer.get("left", 0)
        top  = layer.get("top", 0)
        w    = layer.get("width", "auto")
        extra = layer.get("extra_style", "")
        inner += (
            f'<img src="{src}" style="position:absolute;left:{left}px;top:{top}px;'
            f'width:{w};z-index:{z};image-rendering:auto;{extra}"/>'
        )
    return (
        f'<div style="position:relative;overflow:hidden;{container_style}">'
        + inner
        + "</div>"
    )
