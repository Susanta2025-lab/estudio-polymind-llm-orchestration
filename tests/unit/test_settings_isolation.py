"""Synthetic configuration contracts; never read the operator's dotenv file."""

import builtins
import importlib
import json
import os
import shutil
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.settings import Settings
from tests.unit.test_governance import configuration, execution
from tests.unit.test_security_configuration import configured

# Deliberately constructed during collection, before any function-scoped fixture.
COLLECTED_SETTINGS = Settings()
COLLECTED_MEMORY_HISTORY = COLLECTED_SETTINGS.MEMORY_HISTORY
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def synthetic_environment(monkeypatch):
    for name in tuple(os.environ):
        if name.upper() in Settings.model_fields:
            monkeypatch.delenv(name)


@pytest.mark.parametrize(
    "dotenv",
    [
        "MEMORY_HISTORY=73\nAPI_AUTH_MODE=disabled\n",
        (
            "API_AUTH_MODE=oidc_jwt\nGOVERNANCE_ENABLED=true\n"
            "OIDC_CONFIGURATION=not-valid-json\n"
        ),
    ],
    ids=["standalone-operator", "governed-operator"],
)
def test_implicit_dotenv_is_not_even_opened(tmp_path, monkeypatch, dotenv):
    monkeypatch.chdir(tmp_path)
    implicit = tmp_path / ".env"
    implicit.write_text(dotenv)
    original = builtins.open

    def guarded_open(file, *args, **kwargs):
        if isinstance(file, (str, os.PathLike)) and Path(file).absolute() == implicit:
            pytest.fail("Implicit dotenv must not be opened")
        return original(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    result = Settings()
    assert result.MEMORY_HISTORY == 6
    assert result.authentication_mode == "disabled"
    assert result.model_config["env_file"] == ".env"


def test_explicit_environment_and_constructor_precedence(monkeypatch):
    monkeypatch.setenv("MEMORY_HISTORY", "19")
    assert Settings().MEMORY_HISTORY == 19
    assert Settings(MEMORY_HISTORY=23).MEMORY_HISTORY == 23


@pytest.mark.parametrize("filename", ["synthetic.env", ".env"])
def test_explicit_dotenv_and_source_precedence(tmp_path, monkeypatch, filename):
    monkeypatch.chdir(tmp_path)
    selected = tmp_path / filename
    selected.write_text("MEMORY_HISTORY=17\n")
    assert Settings(_env_file=selected).MEMORY_HISTORY == 17
    assert Settings(_env_file=None).MEMORY_HISTORY == 6
    monkeypatch.setenv("MEMORY_HISTORY", "19")
    assert Settings(_env_file=selected).MEMORY_HISTORY == 19
    assert Settings(_env_file=selected, MEMORY_HISTORY=23).MEMORY_HISTORY == 23


def test_positional_explicit_dotenv_is_preserved(tmp_path):
    selected = tmp_path / "positional.env"
    selected.write_text("MEMORY_HISTORY=29\n")
    # Public BaseSettings configuration arguments preceding _env_file.
    assert Settings(None, None, None, None, selected).MEMORY_HISTORY == 29


@pytest.mark.parametrize(
    "invalid",
    [
        {"MEMORY_HISTORY": 0},
        {"API_AUTH_MODE": "oidc_jwt"},
        {"GOVERNANCE_ENABLED": True},
        {"API_AUTH_ENABLED": True, "API_AUTH_TOKEN": "short"},
        {"INFERENCE_PROVIDER": "unregistered"},
    ],
)
def test_validators_still_reject_invalid_settings(invalid):
    with pytest.raises(ValidationError):
        Settings(**invalid)


def test_oidc_and_governance_can_be_selected_via_environment(tmp_path, monkeypatch):
    values = configured(tmp_path)
    values.pop("_env_file")
    for key, value in values.items():
        if value is not None:
            monkeypatch.setenv(
                key, json.dumps(value) if isinstance(value, (dict, bool)) else value
            )
    result = Settings()
    assert result.authentication_mode == "oidc_jwt"
    assert result.GOVERNANCE_ENABLED
    assert result.GOVERNANCE_PROVIDER_KEY == "test-only"


def test_explicit_governed_dotenv_requires_complete_configuration(tmp_path):
    values = configured(tmp_path)
    values.pop("_env_file")
    selected = tmp_path / "governed.env"
    selected.write_text(
        "\n".join(
            f"{key}='{json.dumps(value) if isinstance(value, (dict, bool)) else value}'"
            for key, value in values.items()
            if value is not None
        )
    )
    result = Settings(_env_file=selected)
    assert result.authentication_mode == "oidc_jwt"
    assert result.GOVERNANCE_ENABLED
    selected.write_text("API_AUTH_MODE=oidc_jwt\nGOVERNANCE_ENABLED=true\n")
    with pytest.raises(ValidationError):
        Settings(_env_file=selected)


def test_unbound_governed_provider_still_denies_all_generation(tmp_path):
    from llm.inference import ModelRole
    from llm.provider_factory import create_inference_provider
    from security.models import SecurityError

    provider = create_inference_provider(Settings(**configured(tmp_path)))
    for method in (provider.generate, provider.generate_stream, provider.execute):
        with pytest.raises(SecurityError):
            method("unattributed", ModelRole.GENERAL)


def test_governed_execution_still_enforces_financial_admission(tmp_path, monkeypatch):
    from governance.ledger import GovernanceError, GovernanceLedger
    from security.authority import SecurityAuthority
    from security.models import _verified_principal

    module = importlib.import_module("config.settings")
    monkeypatch.setattr(module, "settings", Settings(**configured(tmp_path)))
    authority = SecurityAuthority(tmp_path / "security.sqlite")
    principal = _verified_principal(
        "issuer", "synthetic", "tenant", expires=int(time.time()) + 3600
    )
    authority.register(principal)
    ledger = GovernanceLedger(tmp_path / "governance.sqlite", *configuration())
    executor, request, calls = execution((ledger, authority, principal, principal))
    with pytest.raises(GovernanceError):
        executor.execute(request)
    assert not calls
    assert ledger.usage(principal, authority) == []


def test_standalone_cannot_enter_protected_analysis(tmp_path, monkeypatch):
    from documents.publication.analysis import DocumentAnalysis
    from security.models import SecurityError

    module = importlib.import_module("config.settings")
    governed = Settings(**configured(tmp_path))
    monkeypatch.setattr(module, "settings", governed)

    def forbidden(*args, **kwargs):
        pytest.fail("Unbound analysis reached protected data or provider")

    analysis = DocumentAnalysis(
        SimpleNamespace(pin=forbidden),
        SimpleNamespace(execute=forbidden),
        SimpleNamespace(max_output_tokens=2048),
    )
    with pytest.raises(SecurityError):
        analysis.analyze(None)


def test_new_settings_do_not_reconfigure_cached_singleton(monkeypatch):
    module = importlib.import_module("config.settings")
    singleton = module.settings
    before = singleton.MEMORY_HISTORY
    with monkeypatch.context() as change:
        change.setenv("MEMORY_HISTORY", "31")
        assert Settings().MEMORY_HISTORY == 31
        assert module.settings is singleton
        assert singleton.MEMORY_HISTORY == before
    assert Settings().MEMORY_HISTORY == 6
    assert COLLECTED_SETTINGS.MEMORY_HISTORY == COLLECTED_MEMORY_HISTORY


def test_unrelated_settings_models_keep_their_dotenv(tmp_path):
    selected = tmp_path / "other.env"
    selected.write_text("ISOLATION_SENTINEL=41\n")

    class OtherSettings(BaseSettings):
        ISOLATION_SENTINEL: int = 1
        model_config = SettingsConfigDict(env_file=selected)

    assert OtherSettings().ISOLATION_SENTINEL == 41


def test_application_subclasses_inherit_isolation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("MEMORY_HISTORY=43\n")

    class DerivedSettings(Settings):
        pass

    assert DerivedSettings().MEMORY_HISTORY == 6
    assert DerivedSettings(_env_file=tmp_path / ".env").MEMORY_HISTORY == 43


# Child interpreters also deny attempts that application code might swallow.
CHILD_GUARD = """
import socket
import sys
attempts = []
def deny(*args, **kwargs):
    attempts.append(True)
    raise AssertionError('Network forbidden in configuration subprocess')
for name in ('connect', 'connect_ex', 'sendto'):
    setattr(socket.socket, name, deny)
for name in ('create_connection', 'getaddrinfo', 'gethostbyname',
             'gethostbyname_ex', 'gethostbyaddr'):
    setattr(socket, name, deny)
def audit(event, args):
    if event in ('socket.connect', 'socket.sendto', 'socket.getaddrinfo',
                 'socket.gethostbyname', 'socket.gethostbyaddr'):
        deny()
sys.addaudithook(audit)
"""


@pytest.fixture
def isolated_project(tmp_path):
    """Copy only public source files; no operator configuration is accessed."""
    for relative in (
        "tests/conftest.py",
        "tests/settings_isolation.py",
        "config/settings.py",
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    (tmp_path / "tests/__init__.py").touch()
    (tmp_path / "config/__init__.py").touch()
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n")
    return tmp_path


def run_child(project, script):
    environment = {
        key: value
        for key, value in os.environ.items()
        if key.upper() not in Settings.model_fields and not key.startswith("PYTEST_")
    }
    environment["PYTHONPATH"] = str(project)
    # Avoid unrelated installed plugins importing application code before conftest.
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            CHILD_GUARD
            + textwrap.dedent(script)
            + "\nassert not attempts, 'Unexpected offline network attempt'\n",
        ],
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result


@pytest.mark.parametrize("outcome", ["pass", "collection-error"])
def test_collection_isolation_and_shutdown_restoration(isolated_project, outcome):
    project = isolated_project
    (project / ".env").write_text("MEMORY_HISTORY=47\n")
    test_source = (
        "from config.settings import Settings, settings\n"
        "assert Settings().MEMORY_HISTORY == 6\n"
        "assert settings.MEMORY_HISTORY == 6\n"
    )
    test_source += (
        "def test_collected(): assert settings.MEMORY_HISTORY == 6\n"
        if outcome == "pass"
        else "raise RuntimeError('synthetic collection failure')\n"
    )
    (project / "tests/test_collected.py").write_text(test_source)
    expected = 0 if outcome == "pass" else 2
    run_child(
        project,
        f"""
        from pydantic_settings import BaseSettings
        original = BaseSettings.__init__
        import pytest
        assert int(pytest.main(['-q'])) == {expected}
        assert BaseSettings.__init__ is original
        from config.settings import Settings
        assert Settings().MEMORY_HISTORY == 47
    """,
    )


def test_production_import_outside_pytest_keeps_implicit_dotenv(isolated_project):
    (isolated_project / ".env").write_text("MEMORY_HISTORY=53\n")
    run_child(
        isolated_project,
        """
        from config.settings import Settings, settings
        assert settings.MEMORY_HISTORY == 53
        assert Settings().MEMORY_HISTORY == 53
        assert Settings(_env_file=None).MEMORY_HISTORY == 6
    """,
    )


def test_preloaded_application_settings_are_reported(isolated_project):
    (isolated_project / ".env").write_text("MEMORY_HISTORY=59\n")
    run_child(
        isolated_project,
        """
        from config.settings import settings
        assert settings.MEMORY_HISTORY == 59
        import pytest
        assert int(pytest.main(['-q'])) == 4
    """,
    )
