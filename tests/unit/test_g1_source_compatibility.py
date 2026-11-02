"""The G1 source exception is exact, mandatory and limited to reviewed hunks."""

from pathlib import Path

import pytest

from tests.g1_source_compatibility import source_before_g1

ROOT = Path(__file__).resolve().parents[2]


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
    source = (ROOT / path).read_text()
    assert source.count(before) == 1
    with pytest.raises(AssertionError, match="Reviewed G1 source delta changed"):
        source_before_g1(source.replace(before, after), path)
    with pytest.raises(AssertionError, match="Reviewed G1 source delta changed"):
        source_before_g1(source_before_g1(source, path), path)


@pytest.mark.parametrize("name", ["managed.py", "models.py", "validation.py"])
def test_unrelated_changes_remain_visible_to_frozen_comparison(name):
    path = "documents/digestion/" + name
    source = (ROOT / path).read_text()
    approved = source_before_g1(source, path)
    changed = source_before_g1(source + "\nUNAPPROVED = True\n", path)
    assert changed == approved + "\nUNAPPROVED = True\n"
    assert changed != approved


def test_unknown_module_cannot_use_source_exception():
    with pytest.raises(ValueError, match="Unknown G1 source contract"):
        source_before_g1("", "unrelated.py")
