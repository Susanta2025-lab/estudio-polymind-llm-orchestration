"""Install configuration isolation before test-module collection imports."""

import sys

import pytest

from tests.settings_isolation import isolate_application_settings

if "config.settings" in sys.modules:
    raise pytest.UsageError(
        "Application settings were imported before test configuration isolation. "
        "Remove the early application import from the pytest startup plugin."
    )

_settings_patch = pytest.MonkeyPatch()
isolate_application_settings(_settings_patch)


def pytest_unconfigure(config):
    """Restore the public constructor even when collection or tests fail."""
    _settings_patch.undo()


@pytest.fixture
def managed_v9(monkeypatch):
    """Explicit historical generation; current G1/G2 and durable storage remain real."""
    from tests.historical_managed import activate
    with activate(monkeypatch):
        yield


@pytest.fixture(scope="module", params=["managed-prompt/10", "managed-prompt/11"])
def managed_wire_version(request):
    """Exercise the same wire/G1/G2/durability cases under both explicit profiles."""
    from functools import partial

    from documents.digestion import managed

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            managed,
            "StageProfile",
            partial(managed.StageProfile, template_version=request.param),
        )
        yield request.param
