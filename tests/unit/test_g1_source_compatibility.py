"""The G1 source exception is exact, mandatory and limited to reviewed hunks."""

from hashlib import sha256
from pathlib import Path

import pytest

from tests.g1_source_compatibility import source_before_g1

ROOT = Path(__file__).resolve().parents[2]


def historical_g1_source(path):
    # The fixed G1 patch predates v5's intentional prompt-only context edits.
    # Exercise its exact projection on the pinned v4/G1 source, not a refreshed patch.
    if path == "documents/digestion/managed.py":
        source = (ROOT / "tests/fixtures/digestion_contracts/managed_prompt4.py.txt").read_bytes()
        assert sha256(source).hexdigest() == "36e0fba04c1dd952dc7617759fc36f2106d407578ecba194204a215b1ef88a36"
        return source.decode()
    return (ROOT / path).read_text()


@pytest.mark.parametrize(
    "path,before,after",
    [
        ("managed.py", "gt=1024", "gt=1023"),
        ("models.py", "if self.managed_input_budget is None:", "if True:"),
        ("validation.py", "result_contribution(result) + CHILD_WRAPPER_BYTES >",
         "result_contribution(result) + CHILD_WRAPPER_BYTES >="),
    ],
)
def test_admission_extension_cannot_be_changed_or_removed(path, before, after):
    path = "documents/digestion/" + path
    source = historical_g1_source(path)
    assert source.count(before) == 1
    with pytest.raises(AssertionError, match="Reviewed G1 source delta changed"):
        source_before_g1(source.replace(before, after), path)
    with pytest.raises(AssertionError, match="Reviewed G1 source delta changed"):
        source_before_g1(source_before_g1(source, path), path)


@pytest.mark.parametrize("name", ["managed.py", "models.py", "validation.py"])
def test_unrelated_changes_remain_visible_to_frozen_comparison(name):
    path = "documents/digestion/" + name
    source = historical_g1_source(path)
    approved = source_before_g1(source, path)
    changed = source_before_g1(source + "\nUNAPPROVED = True\n", path)
    assert changed == approved + "\nUNAPPROVED = True\n"
    assert changed != approved


def test_unknown_module_cannot_use_source_exception():
    with pytest.raises(ValueError, match="Unknown G1 source contract"):
        source_before_g1("", "unrelated.py")
