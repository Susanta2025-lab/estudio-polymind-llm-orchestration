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


@pytest.fixture(scope="session", autouse=True)
def stable_reference_job_clock():
    """Keep default job time advancing despite host wall-clock corrections.

    Queue-draining fixtures do not wait for a backwards-adjusted host clock to
    catch up with newly recorded outbox timestamps. Anchor UTC once per session,
    then advance by actual monotonic elapsed time. Explicit fake clocks and the
    production SystemClock implementation remain unchanged. Lease timeout tests
    still observe real elapsed time unless they inject their own clock.
    """
    from datetime import datetime, timedelta, timezone
    import time

    # Configuration-isolation tests also copy this conftest into a minimal
    # project containing no document package. Never import an application plane
    # just to install a test clock; collection already loads it where relevant.
    models = sys.modules.get("documents.jobs.models")
    if models is None:
        yield
        return

    anchor, started = datetime.now(timezone.utc), time.monotonic()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(models.SystemClock, "now", lambda self: anchor + timedelta(seconds=time.monotonic() - started))
        yield


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
