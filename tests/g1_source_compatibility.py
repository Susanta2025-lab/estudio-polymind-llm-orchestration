"""Reverse only the reviewed G1 delta before checking historical source contracts.

The fixed patch records d940443's intentional optional admission additions. Every
hunk must match exactly once; unrelated source changes remain subject to the
original frozen source/hash checks. This never modifies or executes source.
"""

import re
from pathlib import Path

_PATCH = Path(__file__).parent / "fixtures/digestion_contracts/managed_g1.patch"
_PATHS = {
    "documents/digestion/managed.py",
    "documents/digestion/models.py",
    "documents/digestion/validation.py",
}


def source_before_g1(source, path):
    """Project exact reviewed additions out of a complete module, failing closed."""
    if path not in _PATHS:
        raise ValueError("Unknown G1 source contract")
    blocks = _PATCH.read_text(encoding="utf-8").split("diff --git ")[1:]
    selected = [b for b in blocks if b.startswith(f"a/{path} b/{path}\n")]
    assert len(selected) == 1, "Missing or duplicate G1 source delta"
    hunks = re.split(r"^@@[^\n]*\n", selected[0], flags=re.MULTILINE)[1:]
    assert hunks, "Empty G1 source delta"
    for hunk in reversed(hunks):
        lines = hunk.splitlines(keepends=True)
        assert all(line[0] in " +-" for line in lines), "Invalid G1 source delta"
        before = "".join(line[1:] for line in lines if line[0] in " -")
        after = "".join(line[1:] for line in lines if line[0] in " +")
        assert after and source.count(after) == 1, "Reviewed G1 source delta changed"
        source = source.replace(after, before, 1)
    return source
