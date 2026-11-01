# Test configuration

Run the configured offline suite with `python -m pytest -q` from the repository
root. Tests use synthetic providers and temporary local state; live benchmark
commands under `tests/performance/` require separate explicit authorization.

## Offline suites and live boundaries

From the repository root, these existing pytest paths select offline regression
tests (commands verified against `pytest.ini` and the module inventory):

```bash
python -m pytest tests/unit -q
python -m pytest tests/integration -q
```

Unit tests cover isolated contracts; integration tests compose real application
components with fake providers and temporary authorities. Synthetic Foundry tests
exercise strict JSON Schema compatibility, application domain rejection, bounded
transport, RPM/TPM admission and synthetic financial reservation/settlement. They
do not establish Azure service acceptance, model quality or billing accuracy.
Synthetic approval/RSA fixtures can sign and consume temporary test approvals;
they never supply live trust, real operator authorization or actual financial funds.

[Frozen digestion contracts](fixtures/digestion_contracts/README.md) distinguish
historical `managed-prompt/3` source/request witnesses from active
`managed-prompt/4` fixtures. Source-token checks protect domain declarations and
acceptance predicates independently of Python AST serialization. Strict provider
schema success is distinct from local domain acceptance: non-factual populated
subjects remain rejected locally.

Performance harnesses are outside default pytest collection. Some modules are
offline only; the Foundry L1 and single-analysis CLIs are live-capable and require
separate authorization, exact source/configuration bindings, verified identity,
financial approval and independent RSA approval. Ordinary regression commands
must not select their live mode. Attempt 6's successful one-call evaluation does
not authorize another call or establish full live L1 digestion; see its
[closure](../docs/codex/reports/phase_17hl_attempt6_closure_and_phase17h_gate_assessment.md).

## Settings and network isolation

`tests/conftest.py` installs settings isolation when pytest loads the root test
configuration, before collecting/importing test modules. For the application
`config.settings.Settings` model and its subclasses, an omitted `_env_file`
constructor argument becomes the supported Pydantic `_env_file=None`. This also
covers the singleton constructed while importing `config.settings`.

Explicit `_env_file=path` (including a controlled `.env`), `_env_file=None`,
environment variables, constructor values, defaults and validators retain their
usual behavior and precedence. Use temporary files for intentional dotenv tests.
Exported application environment variables remain effective; they are deliberate
configuration, unlike the implicitly loaded operator dotenv file. Tests requiring
specific values should supply them explicitly and restore mutations with
`monkeypatch`.

The adapter wraps the public `BaseSettings.__init__` boundary, forwards unrelated
settings models unchanged, and preserves positional arguments and introspection.
It does not patch Pydantic's private source readers or change `Settings.model_config`.
Filtering sources with `settings_customise_sources` would run after dotenv source
construction has already read the file in the pinned pydantic-settings version.
The wrapper is undone by `pytest_unconfigure`, including after collection errors.
Application settings imported by an external pytest startup plugin before this
conftest are reported as a configuration error; remove that plugin's early import.
The adapter does not retroactively replace singleton references.

Synthetic OIDC/governance tests must still provide complete validated settings,
identities, authorities and provider admission context. Isolation does not change
authorization checks, quota policy or financial accounting. Standalone tests use
application defaults or explicitly select the supported standalone mode.

Network denial is a separate verification safeguard. The phase report records
the pre-collection socket/DNS guard used for verification, including a counter
that fails the session even if a network exception is swallowed. No temporary
settings-isolation plugin is needed. The regression subprocesses install their
own network denial before application imports.

Settings isolation alone does not block network access or clear exported
credentials. For a no-network verification, install an inspected socket/DNS guard
before collection/imports, clear application and credential environment inputs,
and place caches, authorities and output under disposable storage. The historical
reports describe their external guard; it is not a checked-in pytest plugin or a
command prerequisite assumed to exist. No such guard was run by this documentation
remediation task, which uses static checks only.

See [the isolation report](../docs/codex/reports/phase_17hl_full_suite_configuration_isolation.md)
for baseline reconciliation, all 64 affected node IDs, verification and limits.
