"""Plain inert local display, without HTML, Markdown evaluation or terminal escapes."""

import json


def render_text(packet):
    return (
        "Operator-supervised document verification\n"
        "Citation validity does not certify semantic support.\n"
        + json.dumps(packet, ensure_ascii=True, indent=2, sort_keys=True)
        + "\n"
    )
