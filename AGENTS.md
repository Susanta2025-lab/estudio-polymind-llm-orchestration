# AGENTS.md

## Purpose

These instructions apply to all Codex work in this repository:

`Susanta2025-lab/estudio-polymind-llm-orchestration`

Estudio PolyMind is a production-style AI Engineering platform. Changes should prioritize architectural clarity, backward compatibility, testability, operational safety, and production-oriented engineering practices.

Codex must treat these rules as persistent repository-level guidance unless a phase prompt explicitly overrides them.

---

## 1. Inspect Before Editing

Before making changes:

* inspect the relevant implementation;
* inspect existing tests;
* inspect configuration and documentation related to the task;
* search for all consumers of interfaces being modified;
* verify actual repository state rather than relying only on the task description.

Do not implement based solely on assumptions from the prompt.

---

## 2. Preserve Existing Architecture

Do not rewrite stable architecture unless the current phase explicitly requires it.

Preserve existing functionality whenever possible, including:

* RAG;
* LangGraph orchestration;
* routing;
* tools;
* memory;
* FastAPI;
* Streamlit;
* Ollama support;
* OpenAI-compatible inference support;
* Docker workflows;
* existing API contracts.

Prefer incremental changes over broad redesigns.

---

## 3. Provider-Neutral Inference Boundary

Maintain the architecture:

```text
Application / LangGraph / RAG
            ↓
     InferenceProvider
       ↙           ↘
    Ollama     OpenAI-compatible
```

Provider-specific behavior must remain inside provider/configuration infrastructure.

Do not scatter runtime-specific conditions through:

* graph;
* API;
* UI;
* RAG;
* tools;
* memory.

vLLM should be treated as an external inference service unless a future phase explicitly changes that architecture.

---

## 4. Git Safety

Unless explicitly instructed otherwise, Codex MUST NOT:

* commit;
* push;
* merge;
* rebase;
* create tags;
* rewrite history;
* delete branches;
* modify GitHub settings;
* modify remote state.

Leave implementation changes uncommitted for user review.

At the end of major tasks, report:

```bash
git status
git diff --stat
```

Explicitly state whether any commit or push occurred.

---

## 5. Scope Discipline

Implement only the requested phase or task.

Do not introduce unrelated:

* refactors;
* dependencies;
* infrastructure;
* frameworks;
* cloud services;
* model runtimes;
* observability platforms;
* security systems;
* database migrations.

If an out-of-scope change appears necessary, explain why before expanding scope.

Prefer the smallest sound implementation.

---

## 6. Backward Compatibility

Before changing an existing interface or API:

* identify all repository consumers;
* check tests;
* check documentation;
* assess external compatibility risk.

Breaking changes must be intentional and documented.

Do not silently change:

* endpoint behavior;
* response formats;
* streaming protocols;
* model-routing semantics;
* configuration names;
* memory behavior.

If a breaking change is required, clearly report it.

---

## 7. Testing

Every material implementation change should include automated tests where practical.

Prefer:

```text
tests/
├── unit/
└── integration/
```

Do not treat scripts under `experiments/` as the primary production test suite.

Tests should avoid requiring:

* live Ollama;
* live vLLM;
* GPUs;
* cloud services;
* external API credentials;

unless the phase explicitly requires live integration testing.

Use mocks, fakes, and contract tests appropriately.

---

## 8. Validation

For major implementation phases, run relevant validation before reporting completion.

At minimum where applicable:

```bash
pytest
git diff --check
python -m compileall .
```

If the local `memory/__pycache__` ownership issue prevents normal compile output, use an external bytecode-cache location rather than changing unrelated filesystem ownership unless explicitly requested.

Also run when relevant:

```bash
docker compose config --quiet
docker build .
```

Run configured linting or formatting tools if available.

Do not claim a check passed unless it was actually run.

If a check cannot be run, report why.

---

## 9. Implementation Self-Review

After implementation and initial tests:

* inspect the complete diff;
* review architecture;
* check compatibility;
* check resource handling;
* check error paths;
* check tests for meaningful coverage;
* look for duplication;
* look for provider-specific leakage;
* look for accidental behavior changes.

Fix meaningful findings before final reporting.

---

## 10. Pre-Commit Review

Before declaring a major phase complete, perform a separate pre-commit review.

Check for:

* secrets;
* credentials;
* private keys;
* `.env` files;
* hard-coded local paths;
* debug statements;
* temporary files;
* generated artifacts;
* stale TODOs introduced by the phase;
* dead code;
* accidental dependencies;
* unrelated changes;
* broken documentation;
* unintended API changes.

Do not commit during this review.

---

## 11. Secrets and Sensitive Configuration

Never commit:

* API keys;
* access tokens;
* passwords;
* private keys;
* real `.env` files;
* credentials embedded in URLs.

Use environment variables and `.env.example`.

Ensure Docker build context excludes runtime secret files.

Do not include secrets or upstream response bodies in logs or user-facing errors.

---

## 12. Error Handling

Prefer normalized application/provider errors over raw infrastructure exceptions.

Do not expose:

* upstream HTTP response bodies;
* credentials;
* connection strings;
* internal stack traces;

to application users.

Do not silently swallow malformed protocol or streaming errors.

Log enough structured information for debugging without leaking sensitive data.

---

## 13. Configuration

Keep configuration centralized and environment-driven.

Avoid:

* hard-coded endpoints;
* machine-specific filesystem paths;
* runtime-specific model identifiers scattered through application code.

Logical model roles should remain separate from served model identifiers.

Validate configuration early where practical.

---

## 14. Docker Rules

Reuse Docker cache.

Do NOT use:

```bash
docker build --no-cache
```

unless explicitly required.

Do not prune Docker globally without explicit user approval.

Do not run:

```bash
docker system prune -a
```

without explicit approval.

Do not delete Docker images automatically.

If an obsolete or sensitive image should be removed:

1. identify the exact image;
2. explain why removal is recommended;
3. request approval;
4. remove only that image.

Avoid creating unnecessary additional tagged validation images.

Do not rebuild unrelated services.

---

## 15. Dependency Installation

Do not install new dependencies merely for convenience.

Before adding a dependency:

* verify it is genuinely needed;
* prefer existing dependencies where appropriate;
* consider maintenance and image-size impact;
* explain the reason.

Request user approval before installing new system-level or substantial project dependencies when Codex execution policy requires it.

Do not install vLLM, CUDA, GPU runtimes, or large model packages unless the active phase explicitly requires them.

---

## 16. Docker Image Size

The current ML dependency stack can produce large Docker images.

Avoid making image size materially worse without justification.

When a phase changes dependencies or Docker configuration, consider:

* layer caching;
* dependency separation;
* unnecessary CUDA packages;
* control-plane versus inference-plane concerns.

Do not perform broad Docker optimization unless the phase explicitly includes it.

---

## 17. vLLM Architecture

The intended production direction is:

```text
PolyMind control plane
        ↓
InferenceProvider
        ↓
OpenAI-compatible adapter
        ↓
External vLLM inference platform
```

Do not embed vLLM into the existing PolyMind application container unless a future phase explicitly requires that deployment architecture.

Keep:

* control plane;
* inference data plane;

logically separable.

---

## 18. API Streaming Boundary

Maintain the distinction:

```text
External vLLM
   ↓
OpenAI-compatible SSE
   ↓
OpenAI-compatible provider
   ↓
provider-neutral token stream
   ↓
PolyMind orchestration
   ↓
PolyMind NDJSON API
   ↓
UI/client
```

Do not expose upstream SSE directly to PolyMind clients without an explicit architectural decision.

---

## 19. Documentation

Update documentation when a task materially changes:

* architecture;
* configuration;
* API contracts;
* setup;
* testing;
* deployment;
* developer workflow.

Do not update documentation merely to create activity.

Documentation must describe only implemented capabilities.

Do not claim future functionality is complete.

---

## 20. Phase Prompts and Reports

For major implementation phases, preserve important Codex artifacts under:

```text
docs/codex/
├── prompts/
└── reports/
```

Recommended naming:

```text
docs/codex/prompts/phase_8c.md
docs/codex/reports/phase_8c_report.md
```

Store only major phase prompts/reports.

Do NOT store:

* routine questions;
* one-line fixes;
* temporary debugging conversations.

If a phase prompt was supplied externally and is practical to preserve, save a clean Markdown copy.

Final reports should explain:

* what changed;
* why;
* architecture impact;
* tests;
* validation;
* self-review findings;
* pre-commit findings;
* documentation changes;
* remaining risks;
* next-phase readiness.

---

## 21. Report Quality

Major-phase reports should be explanatory, not merely terse bullet lists.

Include enough detail for another engineer to understand:

* the implementation;
* design rationale;
* validation evidence;
* known limitations.

Use exact test counts and command outcomes when available.

---

## 22. Phase-Gated Development

Major project work should normally follow:

```text
Assessment
    ↓
Implementation
    ↓
Automated testing
    ↓
Implementation self-review
    ↓
Fixes
    ↓
Pre-commit review
    ↓
Documentation
    ↓
Final validation
    ↓
Phase report
    ↓
User review
    ↓
Commit/push by user
```

Do not automatically start the next major phase.

---

## 23. Production-Oriented Standard

When making architectural choices, optimize for credible production-style engineering rather than demo-only shortcuts.

Consider where relevant:

* explicit boundaries;
* dependency inversion;
* timeouts;
* resource cleanup;
* concurrency;
* health/readiness;
* failure modes;
* structured logging;
* configuration validation;
* security boundaries;
* observability;
* scalability;
* deployment portability.

Do not implement all of these in every phase; apply them according to scope.

---

## 24. Avoid Overengineering

Production-style does not mean maximum abstraction.

Prefer:

* narrow interfaces;
* explicit code;
* testable modules;
* small abstractions;
* standard protocols.

Avoid speculative frameworks or abstractions for requirements that do not yet exist.

---

## 25. Final Rule

If a phase objective conflicts with the current repository architecture or would require a risky/unexpected redesign:

* stop expanding the change;
* explain the conflict;
* implement only what is safe;
* report the limitation clearly.

Never mask unresolved architectural problems simply to return `PASS`.



## 26. Docker & Kubernetes Authorization

The user explicitly authorizes all necessary, scoped, non-destructive Docker and Kubernetes operations required for this assessment.

Docker Desktop is running.

You do NOT need to ask the user for additional authorization before performing appropriate tasks such as:

- `docker build`
- `docker run`
- `docker inspect`
- `docker image inspect`
- `docker history`
- `docker compose config`
- `docker compose build`
- `docker compose up/down` for scoped project services
- Kind cluster inspection or validation
- `kubectl get`
- `kubectl describe`
- `kubectl logs`
- `kubectl rollout status`
- `kubectl apply` / `delete` when strictly limited to dedicated PolyMind test resources
- Helm linting, templating, installation, upgrade, rollback, or uninstall against the dedicated PolyMind Kind environment
- creation/removal of temporary PolyMind test pods, deployments, services, namespaces, or other scoped validation resources

For Kubernetes mutations:

1. Explicitly verify the active context before mutation.
2. Only mutate the dedicated PolyMind local/Kind test environment.
3. Never mutate an ambiguous, remote, shared, or production cluster.
4. If the Kubernetes context cannot be positively identified as the dedicated test environment, stop rather than mutate it.

For Docker:

- use normal build cache;
- do not use `--no-cache` unless technically necessary;
- do not run global Docker prune operations;
- do not delete unrelated images, containers, networks, or volumes;
- temporary Phase-specific resources may be removed when they are clearly scoped and safe.

This authorization is already granted by the user and should not be treated as requiring conversational confirmation.

However, the Codex CLI sandbox/execution-safety system may independently require approval for particular commands. That policy takes precedence and cannot be overridden by this prompt or by `AGENTS.md`. If Codex itself presents an execution approval dialog, follow that mechanism rather than repeatedly asking the user conversationally.
