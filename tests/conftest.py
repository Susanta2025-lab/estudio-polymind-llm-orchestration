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
