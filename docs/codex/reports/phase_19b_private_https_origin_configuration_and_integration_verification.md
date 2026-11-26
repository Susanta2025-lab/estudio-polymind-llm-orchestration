# Phase 19B — Private HTTPS origin configuration and integration verification

Task begun 25 November 2026; validation continued 26 November 2026 (Europe/Lisbon, UTC).
Repository `Susanta2025-lab/estudio-polymind-llm-orchestration`.
This is a bounded Phase 19B task report, not Phase 19B completion or production acceptance.
Phase 19A Readiness Assessment is COMPLETE; Phase 19B Offline Implementation, Azure Deployment,
Live Integration and Validation is ACTIVE; Phase 19C Final Documentation and Engineering
Closure is NOT STARTED.

## 1. Executive summary

Selected `https://polymind.test:9443` for the private verification environment and
`https://polymind.test:9443/oauth2callback` for native Streamlit and Entra Web redirects.
The existing generic gateway supports this contract without application-code changes.
The Compose example now selects the origin; a new inert native OIDC template records the
matching callback and explicit unprovisioned identity/credential fields. The five-service
architecture and loopback-only publication are unchanged.

New offline coverage combines the real production TLS context with HTTP callback/WebSocket
proxying, hostname verification and negative security checks for this name and the existing
synthetic hostname. Current documentation provides independently reviewable future Entra,
Windows forwarding and private CA/trust procedures. Actual registration, consent, operational
certificates, Windows resolution/trust, runtime subject enrollment, browser login and production
HTTPS remain unverified and blocked/pending as classified below. No cloud or production action
was performed. The VM remains operator-reported deallocated.

## 2. Actual starting Git baseline

All six requested commands ran before editing. `git status --short --branch` returned only
`## master...origin/master`; tracked diff/stat, whitespace diagnostics and staged names were
empty. HEAD matched exactly **`1b11b3ab766240c162d1970bae438c00752c6c6f`**. There were no
pre-existing tracked, staged or untracked changes to preserve. No reset or branch change.
The eight starting commits were:

```text
1b11b3a docs: reconcile Phase 19B Azure evidence and verify offline readiness
7bf82dc feat: complete Phase 19B offline Azure deployment foundation
b48dde4 feat: improve local app launchers and document frontend reliability
d7d2ec2 fix(ui): resolve Streamlit document module collision and preserve legacy chat
6aedae3 docs: finalize Phase 18 local engineering closure and deployment handoff
f7d091a feat(documents): implement authenticated local document frontend and verification
f0e420b docs: assess Phase 18 frontend integration and Azure deployment readiness
faaddc2 docs: finalize Phase 17I engineering closure with external verification deferred
```

The previous reconciliation report's uncommitted `7bf82dc` handoff describes its historical
run. Its work is now committed in `1b11b3a`; that historical statement was not rewritten.

## 3. Scope and authorization boundaries

Authorized: repository inspection, selected-origin templates, narrow synthetic offline tests,
local inert Compose parsing, compilation, self-review/pre-commit review, documentation and
operator-executable future procedures. No Azure CLI, Graph/Entra operation, remote SSH, browser
login/token acquisition, VM activation, production Compose/authorities, operational certificate
or trust/hosts provisioning, external inference, financial/permission mutation or Git index/history/remote writes
were performed. Public documentation was read without tenant authentication. Test keys/certs
and synthetic authorities live only in dedicated temporary test state.

No dependencies, runtime source, network topology, service count, provider behavior, financial
policies or API contracts were changed. Local Chat/Ollama and development Documents origins
remain intact. Configuration selection is not production activation authorization.

## 4. Source documents and provenance

Read root [AGENTS.md](../../../AGENTS.md), the requested Phase 19 prompts/reports including
[Integration Gap Resolution](phase_19b_offline_implementation_and_verification.md#integration-gap-resolution)
and the [24 November reconciliation](phase_19b_post_azure_readiness_offline_validation_evidence_reconciliation.md),
current VM runbook, architecture/plan, security Entra guide, deployment directory, Compose,
Dockerfile/exclusions, actual UI authentication consumers and relevant tests/harness.
The [clean instruction record](../prompts/phase_19b_private_https_origin_configuration_and_integration_verification.md)
preserves the task with formatting/repeated lists consolidated; the supplied instruction
remains authoritative.

Evidence classes used throughout:

- **Historical repository evidence:** existing implementation, prior test/container results,
  reported image audit and Azure foundation records. These were inspected, not rerun as cloud checks.
- **Operator-reported external evidence:** 25 November API registration/role assignment/inventory
  and VM deallocated state. No independent tenant/VM query this task.
- **Fresh offline verification:** actual local Python tests, TLS/HTTP/WebSocket exchanges,
  configuration parsing, compilation and file review recorded below.
- **Proposed procedures:** new runbook commands are reviewed instructions, never executed changes.
- **Unverified live behavior:** real Entra registration acceptance, browser/session/trust,
  tunnel/Windows resolution and production application acceptance.

Tracked source/template/test/document searches covered PHASE19_ORIGIN, polymind.private.example,
polymind.test, oauth2callback, redirect_uri, server_metadata_url, streamlit.toml, 9443,
127.0.0.1 and localhost. The temporary reference inventory retains file/line context.
Classification is contextual, including dated sections within current documents:

| Reference category | Actual consumers/examples and disposition |
|---|---|
| Current Phase 19 deployment | gateway origin/environment, Compose port/mounts, current README and dated runbook/architecture/plan; selected configuration updated |
| Portable configuration example | compose.env.example selects this environment; new OIDC inventory keeps generic tenant/API/browser/credential placeholders; configuration.example.json remains intentionally invalid |
| Historical evidence | docs/codex prior prompts/reports and dated historical sections; untouched, no retroactive verdict changes |
| Synthetic test fixture | tests' phase19.test.invalid/private.example and scripts/phase19_offline_validation.py's polymind.private.example; retained, selected hostname added alongside existing coverage |
| Local development | .env.example, development/document_demo, local launchers, ordinary/Documents Compose, README local instructions; localhost/loopback preserved |
| Unrelated/shared configuration | other phase Helm/Kind/load scripts, generic config defaults and shared gateway logic; no hostname substitution |

The original private-example origin remains in the synthetic container harness intentionally.
The harness overrides gateway input for an isolated test network and is not a production
configuration source. Health probes' loopback IPs are internal service connections, not
browser identities. No indiscriminate replacement was performed.

## 5. Operator-reported Entra verification evidence

On 25 November the operator supplied:

| Item | Reported non-secret configuration |
|---|---|
| API app | estudio-polymind-api-dev |
| Application/client UUID | 5aa70f9d-9f9e-4b5b-972b-698d4d68105e |
| Application ID URI | api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e |
| API service principal object UUID | 046ce5b0-897c-4289-ad86-e403ac6b6e20 |
| Account type / delegated scope | AzureADMyOrg / access_as_user |
| Enabled User app-role | PolyMind.L1Operator |
| Role UUID | e34bc374-42ff-4a6a-87e2-007b8cc788b3 |

Exactly one API app-role assignment was reported. Its principal type was User, principal UUID
matched the signed-in operator's directory object UUID, and role UUID matched the enabled
role. Verdict **OPERATOR_REPORTED_PASS**, configuration only. No token claim, login, consent,
API call or runtime enrollment proof is inferred. The directory object UUID was not supplied
and was not invented. Enrollment remains `[issuer, tenant UUID, API access-token sub]`; neither
`oid`, email/display name nor an ID-token subject supplies it.

Reported inventory contained API and estudio-polymind-cli-dev, but no dedicated
estudio-polymind-streamlit-dev. Browser registration/SP/delegated permission/consent/credentials
are pending. These environment IDs occur only in operational records/procedures, not reusable
application logic or the portable OIDC template.

## 6. Initial readiness assessment

Assessment preceded configuration edits. PASS here refers to the stated existing contract,
not a fresh live test. Later fresh offline verification is distinguished in section 14.

| Area | Initial finding | Class/status | Required change or blocker |
|---|---|---|---|
| Git baseline | Exact expected HEAD, clean worktree/index | Existing state PASS | None |
| Generic origin parsing | HTTPS required; literal localhost/127.0.0.1/::1 and path/query/fragment/userinfo denied | Implementation PASS | No runtime change for polymind.test |
| TLS loading | Private cert/key before listener, minimum 1.2 | Implementation PASS | Operational certs/trust still absent |
| Host/WS boundary | Exact Host and supplied Origin; WS Origin mandatory; forwarded headers sanitized | Implementation PASS | Add selected-name regression |
| Compose | Five services, 127.0.0.1:9443:9443, read-only secret binds, no source auto-create | Implementation PASS | No topology change |
| Origin environment example | Old private.example origin | Configuration GAP | Select requested origin |
| Native OIDC template | No suitable Phase 19 template found | Configuration GAP | Add one inert field inventory |
| Template callback consistency coverage | Native fields described but no concrete Phase 19 pair to compare | Coverage GAP | New parser/consumer regression |
| API role assignment | Exact enabled user role assignment reported | Operator evidence PASS | No claim of authenticated access |
| Browser registration/consent | Dedicated app absent from reported inventory | Operational BLOCKED | Separate authorized registration |
| Windows forwarding | VM loopback requires a loopback-reaching tunnel | Procedure GAP | Windows-native instructions; endpoint pending |
| Operational CA/trust | Name now selected; issuance/lifetimes/custody/trust not supplied | Operational BLOCKED | Reviewed future procedure/decisions |
| Public DNS/new infrastructure | Unneeded for private hosts/tunnel design | NOT_APPLICABLE | Do not introduce |
| Production activation/inference | Unauthorized; independent inputs missing | BLOCKED | Preserve existing gates |

## 7. Selected private HTTPS configuration

| Parameter | Selected value |
|---|---|
| Origin | https://polymind.test:9443 |
| Hostname / scheme / browser port | polymind.test / HTTPS / 9443 |
| Callback / exact Entra Web URI | /oauth2callback / https://polymind.test:9443/oauth2callback |
| HTTP Host / WebSocket Origin | polymind.test:9443 / https://polymind.test:9443 |
| Windows mapping | 127.0.0.1 polymind.test |
| Windows SSH listener / VM target | 127.0.0.1:9443 / 127.0.0.1:9443 |
| VM Docker publication / container TLS | 127.0.0.1:9443:9443 / 9443 |
| Server certificate SAN | DNS:polymind.test |
| Certificate approach / TLS minimum | Dedicated private CA-signed server / TLS 1.2 |
| Public exposure | Prohibited |

This is a `.test` bounded private environment. Another explicitly approved private hostname
remains configurable; there is no hardcoded selected hostname in runtime validation.

## 8. Existing architecture compatibility

`deployment/phase19/gateway.py` parses PHASE19_ORIGIN before TLS setup; it loads the private
certificate/key and calls the shared proxy with upstream `http://ui:8501`, container listener
9443, minimum TLS 1.2, content-free access logging disabled. `ui/tls_gateway.py` compares the
actual Host to the configured authority, rejects mismatched supplied Origin, requires exact
WebSocket Origin and removes untrusted Forwarded/X-Forwarded headers before setting HTTPS.
Cross-site `/auth/` initiation is denied. Callback `/oauth2callback` is proxied to Streamlit.

Docker publishes only gateway `127.0.0.1:9443:9443`; no API/UI/Redis/Chroma ports are published.
The container-interface listener is required for Docker forwarding and does not imply a VM
public listener. TLS/native mounts stay read-only with create_host_path:false. Missing files
fail before useful startup; malformed TLS fails before listener creation. Native secrets need
operator ownership/permission review because Streamlit does not reuse private_path validation.
No new network, service, certificate manager or configuration framework is needed.

The existing API/runner, seven SQLite authorities, Redis/Chroma persistence, explicit initialize
versus serve, mount-aware unit, source/owner/enrollment, independent permission, finance and
provider-neutral inference boundaries are unchanged. Readiness is not execution permission.
Gateway routing has a UI-only upstream, not an API route. New fixture 404 checks verify that
UI-only path in isolation; they do not assert a deployed Streamlit catch-all always returns
404 or constitute production firewall acceptance.

## 9. Configuration and implementation changes

- compose.env.example selects the private origin and labels its limited verification scope;
  every unrelated variable is preserved.
- streamlit.secrets.example.toml is a new minimal inert inventory because no Phase 19 native
  template existed. It lives outside .streamlit, is not auto-loaded/mounted, and has no real IDs
  or secret values. Existing production JSON remains deliberately incomplete/invalid.
- test_phase19_tls.py retains the original synthetic domain and adds polymind.test parameters,
  certificate symlink refusal and combined verified HTTPS/callback/WebSocket security checks.
- test_phase19_oidc_template.py parses real templates and uses installed Streamlit helpers
  against an in-memory mapping, checking default-provider scope/redirect/token exposure and
  the external read-only/missing-source-fatal mount. No login or metadata fetch.
- README, VM runbook, architecture/plan receive dated current-state reconciliation; historical
  reports remain unchanged. This prompt/report are new task records.

No application runtime Python, Compose topology, Dockerfile, dependency, financial policy,
provider adapter or API contract changed. No breaking change was introduced.

## 10. Native Streamlit OIDC configuration contract

Installed and pinned Streamlit is **1.58.0**. Inspected auth_util and Starlette auth routes
support the unnamed default provider used by both st.login() consumers. The new template
contains the requested auth fields and `[auth.client_kwargs]` scope. State/nonce are managed
by the library; its installed route implementation enables S256 when advertised by metadata.
This is a server-side confidential authorization-code flow; implicit/public-client grants
are unnecessary. No additional native auth setting was found necessary for this selection.
See [Streamlit 1.58 login reference](https://docs.streamlit.io/1.58.0/develop/api-reference/user/st.login).

Environment scope is `api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user`, plus openid.
Tenant and browser UUID remain operator supplied. A separate private client secret and strong
cookie secret are custody inputs. No Graph scope is needed. The API audience is the bare API
UUID, not the scope URI/browser client. UI st.user.tokens['access'] is forwarded to the API;
API independently verifies tenant v2 signature/issuer/audience/scope/role/lifetime, enrollment,
revocation and owner/tenant boundaries. Login alone grants no execution.

The template parser proves structural compatibility, not operational authenticity. Streamlit's
key-presence checks do not reject placeholder values. The deployment procedure therefore
requires private-file review, rejecting every placeholder and comparing exactly
`PHASE19_ORIGIN + '/oauth2callback'`, auth.redirect_uri and Entra web.redirectUris before
provisioning/startup. Existing separate UI/gateway mounts have no automatic cross-file validator.
A wrong callback breaks login but does not bypass the gateway or API verifier. No demonstrated
security mismatch required runtime modification; this remaining operational comparison is
explicit rather than claimed as an automated deployment capability.

## 11. Proposed Microsoft Entra browser registration procedure

The [current runbook](../../operations/phase_19_vm.md#proposed-entra-browser-registration--operator-review-only)
contains individually reviewable Bash/Azure CLI steps: verify tenant and duplicate inventory;
discover the enabled API scope UUID; create only the dedicated single-tenant Web confidential
browser app with exact callback and implicit/public flows disabled; read back application
redirect settings; create its SP only if absent; request only the discovered delegated API
scope; assess narrow consent with the administrator; provision credentials privately; verify
read-only application/SP/permissions/grants/credential metadata. Existing API/CLI apps are not
modified. App-role UUID is explicitly distinguished from delegated scope UUID.

[Microsoft code-flow requirements](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
and [redirect restrictions](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url)
show no identified conflict with the selected HTTPS Web callback. The non-localhost port must
match. This is a documentation-based compatibility assessment, not actual tenant acceptance.
Creation/readback of the exact URI remains PENDING; rejection must be reported without silently
substituting another origin. Broad Graph permissions/admin consent are not prescribed.

Credential creation is a later portal/custodian operation transferring the one-time value
directly into approved secure custody and private configuration, with no terminal/history/
logs/chat output. No secret-printing CLI reset is prescribed. Validity/rotation are operator
decisions; metadata verification never retrieves secret values. No registration command was
executed, no tenant login or token acquisition was attempted.

## 12. Windows hostname resolution and SSH forwarding

The [PowerShell procedure](../../operations/phase_19_vm.md#windows-hostname-resolution-and-private-tunnel--future-powershell-procedure)
uses the standard Windows hosts path, verifies Windows resolver output is only 127.0.0.1,
checks local port availability, and starts foreground Windows ssh.exe with -N -T,
ExitOnForwardFailure=yes, StrictHostKeyChecking=yes and explicit loopback forwarding.
It uses the historically identified polymindadmin user/key and host fingerprint, but keeps
the final VM Tailscale endpoint as a placeholder because no authoritative final tail IP/alias
was located. The known Windows tail IP must not be misused as a VM address. Windows and WSL
known_hosts differ; compare the existing host key to the independent record before connecting.

Hosts mapping changes the destination address, preserving URL/SNI/Host/Origin polymind.test.
The tunnel reaches VM loopback; Tailscale routing to a VM interface alone does not. No Windows
hosts entry, network setting, SSH connection or listener was created. Windows-to-WSL localhost
forwarding remains unverified, so the browser procedure uses Windows-native OpenSSH. Controlled
shutdown is foreground Ctrl+C and loopback-listener disappearance after appropriate logout.

## 13. TLS provisioning and browser trust procedure

The [private CA recipe](../../operations/phase_19_vm.md#dedicated-private-ca-and-server-tls--future-reviewed-procedure)
provides an encrypted dedicated CA key, retained issuance/revocation database, separate server
key/CSR, CA-signed leaf with exact DNS SAN, CA:false, serverAuth and appropriate key usage,
public chain/hostname/key-match validation, approved lifetimes and secure transfer. Direct
root-signed leaf needs no intermediate in tls.crt; an approved intermediate hierarchy must
send all required intermediates. The CA private key never enters the VM/image/browser.

Operational TLS files must be regular single-link/no-symlink, UID:GID 10001:10001 and exact
0600 at the established /etc/polymind/secrets paths. Protected root-controlled directories
must allow traversal, container bind mounts remain read-only and UID 10001 must read the
mounted targets. private_path enforces effective UID, regular/single-link, no symlink ancestors
and no group/other mode bits; GID/exact mode are additionally operator-verified requirements.
No unrelated ownership change is required. Native secret mode/owner is an operator preflight.

Windows receives only independently fingerprint-verified public CA material into the approved
user/browser trust scope. Actual browser policy/chain/name/expiry must be verified; no browser
exception or TLS/SSH verification disabling. CA/leaf lifetime, custody, renewal lead time,
revocation/distribution and trust-removal owners are explicitly undecided. CRL generation
alone does not establish effective offline browser revocation: no CRL endpoint/enforcement
is implemented. Compromise handling includes stopping use, withdrawing affected trust as
needed and reviewed replacement/revalidation. Gateway reload requires controlled lifecycle.
No operational certificate or trust/hosts change occurred in this task.

## 14. Exact regression and integration evidence

Validation uses the existing estudio_polymind Python 3.10 environment. The temporary runner
`/tmp/polymind-private-origin-20261125/run_checks.py` constructs a whitelist environment
(PATH/HOME/locale/interpreter libraries), excludes application credentials/provider settings,
sets HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1
and TOKENIZERS_PARALLELISM=false, and puts only the temporary guard directory plus the
repository on PYTHONPATH. Existing tests/conftest.py suppresses implicit application dotenv.
The `-p network_guard` plugin denies non-loopback socket connect/connect_ex and external DNS
in the test process, permitting only local/Unix transport. Provider/Entra tests additionally
use existing mocks/fakes and signed synthetic identity/permission records; no operational
credential or cloud endpoint is used. Subprocess call sites were inspected: launcher/config,
crash-recovery, local schema and Helm checks do not acquire real credentials or dispatch
inference. This is an offline test mechanism, not a new production egress control.

Raw logs, JUnit and temporary pytest state remain outside Git under that evidence directory.
Commands executed by the runner, with those environment controls:

```bash
python -m pytest -q -p network_guard \
 tests/unit/test_phase19_tls.py tests/unit/test_phase19_oidc_template.py \
 tests/unit/test_phase19_deployment.py tests/unit/test_phase19_chat_view.py \
 tests/integration/test_phase19_operator.py tests/integration/test_phase19_execution_bridge.py \
 tests/integration/test_phase19_authority_lifecycle.py tests/unit/test_security_entra.py \
 tests/unit/test_document_oidc_fixture.py tests/unit/test_documents_view.py \
 tests/unit/test_ui_api_client.py tests/unit/test_security_api.py tests/unit/test_security_identity.py \
 --junitxml=/tmp/polymind-private-origin-20261125/focused.xml \
 --basetemp=/tmp/polymind-private-origin-20261125/focused-state \
 -o cache_dir=/tmp/polymind-private-origin-20261125/focused-cache

python -m pytest -q -p network_guard \
 --junitxml=/tmp/polymind-private-origin-20261125/full.xml \
 --basetemp=/tmp/polymind-private-origin-20261125/full-state \
 -o cache_dir=/tmp/polymind-private-origin-20261125/full-cache

docker compose --env-file deployment/phase19/compose.env.example -f docker-compose.phase19.yml config --quiet
PYTHONPYCACHEPREFIX=/tmp/polymind-private-origin-20261125/bytecode python -m compileall -q .
git diff --check
python /tmp/polymind-private-origin-20261125/ca_recipe_check.py
```

Focused final result: **exit 0, 315 passed, 0 failed/errors/skipped, 4 warnings in 76.82 s**
(runner wall time 79.67 s). Counts overlap the full run and must not be summed.

Full-suite result: **exit 0, 3329 passed, 160 warnings in 1068.03s (0:17:48)**; JUnit records **3,329 tests, 0 failures, 0 errors, 0 skipped**.
Runner wall time was 1,071.54 s. The complete run includes all new tests; focused and full
counts overlap, not an additive total. The 160 warnings are 156 existing record_property/
xunit2 JUnit compatibility advisories and four occurrences of the existing aiohttp
NotAppKeyWarning at ui/tls_gateway.py:18 (also the four focused warnings). No warning was
suppressed. These are reporting/string-AppKey advisories, not failed assertions.

Fresh coverage includes selected and alternative private names, real TLS context/hostname
handshakes, TLS minimum, exact Host with required port, callback query traversal, exact WS
Origin and bidirectional echo, wrong/missing WS Origin, wrong Host/HTTP Origin, incoming
Forwarded/X-Forwarded sanitization, missing/invalid cert/key, public file modes, both
certificate/key symlinks, unsafe origin scheme/host/path/query/fragment/userinfo, client
rejection of untrusted certificate and wrong SAN. Selected-domain certs are isolated synthetic
self-signed trust anchors, never operational files. Socket tests bind only loopback ephemeral
ports to avoid operator-port collisions; logical Host/Origin retain the exact configured 9443,
and the entrypoint test separately asserts its production container port is 9443. A test-only
resolver maps each synthetic URL hostname to loopback without changing system DNS/hosts.
Native template regression checks the
actual environment/callback pair and installed Streamlit configuration consumers.

The separate **12-step synthetic OpenSSL recipe check passed**, exit 0 in 0.68 s: it extracted
the documented CA configuration, used an explicitly TEST ONLY encrypted CA and one-day test
leaf, checked issuance/SAN/serverAuth/public-key match, accepted the trusted correct hostname,
rejected wrong hostname/untrusted chain, generated a CRL after revocation and verified explicit
CRL-check rejection. All that synthetic CA material was removed automatically on exit.
One-day durations are test inputs only, not selected operational lifetimes. No OS trust was
changed, and this does not prove browser revocation behavior.

Compose parse passed exit 0 (0.08 s on the recorded static run); external-cache compilation
passed exit 0 (0.76 s); diff whitespace passed exit 0 (0.01 s). TOML is parsed and consumed
in the focused native template test. A final Compose-only repeat passed exit 0 in 0.07 s
with subprocess environment limited to PATH, HOME, LANG and LC_ALL, removing all ambient
PHASE19/Compose overrides; it used the same exact parser arguments listed above.
No configured lint/type/formatter tool exists in the
repository; no tool/dependency was installed. CI's existing pytest/compile checks are covered;
unrelated Helm configuration is unchanged and its existing tests remain in the full suite.

Intermediate failures/corrections are not hidden. The first sandbox attempt could not use
required local sockets and was interrupted (exit 130); it is not a completed test result.
Execution-approved focused rerun then had **314 passed, 1 failed, 4 warnings in 87.72 s**
(exit 1): the new test replaced Streamlit's secret object with a dict lacking its loader
method. This was a fixture error, corrected by injecting the in-memory auth section at its
existing accessor instead of replacing the secret object. The isolated corrective check
passed **1 test in 0.31 s**, then the full focused group passed as recorded above. No production
code or assertion was weakened. Initial patch application failed to match context before
applying anything; the corrected patch applied cleanly.

No five-service container workload or image build was repeated: no executable source,
Compose topology, dependency or runtime behavior changed. The inspected existing harness and
24 November recorded five-service workflow/restart/recovery evidence remain historical,
not new execution. The fresh real TLS + proxy + local UI fixture exercises the changed name's
integration contract with no public port. API/enrollment/execution tests use actual application
assembly over isolated authorities and existing mocked provider transport. API health/admin
paths have no gateway API upstream; fixture 404s and source/Compose checks establish this
bounded contract, not deployed Streamlit status-code behavior or host firewall enforcement.

Not executed: Windows/browser/SSH, Entra registration/token/consent, Azure/production TLS,
production startup/authority initialization, live provider, cloud reboot/DR/capacity/outbound
acceptance. These require missing operational inputs and separate authorization. They are
PENDING/BLOCKED, never PASS by inference from offline results.

## 15. Application image and deployment provenance implications

The historically reviewed Azure application identity remains
`sha256:9f386acf8bddcb5d01bb028151caae24b5df604f8a56c00b7b39c7e0f8298c02`, revision label
`7bf82dc2da4a9f29561a5f493b690502c0090eb0`, linux/amd64, UID:GID 10001:10001. This is
historical reported/audited evidence; no new image inspection/transfer is claimed.

| Change boundary | Outcome |
|---|---|
| Runtime Python / provider / UI / gateway | Unchanged |
| Dockerfile / dependencies / Compose topology | Unchanged |
| External runtime configuration | Selected origin and future native OIDC inputs require reviewed external provisioning |
| Build-context contents | Changed: compose.env.example and new inert TOML inventory are included by COPY . .; tests/docs are excluded |
| Packaged executable behavior | Unchanged; examples are not imported or auto-loaded and mounts select external configuration |
| Existing image provenance | Old image contains neither updated origin example nor new OIDC inventory; do not claim otherwise |
| Image rebuild required for adoption | NO; gateway already accepts selected origin and UI uses external native secrets |
| Exact new source-snapshot image | Would need a new build/provenance if an operator later requires examples packaged; no such rebuild/transfer performed |
| Azure-staged configuration update | YES, later authorization: update /opt/polymind/compose.env.example origin and provision reviewed /etc/polymind/compose.env/native files |

Do not overwrite the Azure-staged pinned Compose with the repository's portable vendor-tag
copy. Preserve the previously reviewed application identity and reported Redis/Chroma pinned
references; no new source change requires replacing them. Review/hash-transfer only the
necessary inert configuration material in the next authorized session, then separately provision
private credentials/certificates. A local image ID is not automatically a registry digest.
The example's selected origin does not supply missing policies/authorities/secrets or make
production configuration valid.

## 16. Engineering self-review

Reviewed runtime consumers and complete scoped changes for callback consistency, TLS name,
secret boundaries, Host/Origin/forwarded checks, SSH loopback, trust/chain, provider neutrality,
backward compatibility and test coverage. Generic validation has no polymind.test literal.
All old synthetic/private alternative domains and local localhost workflows remain.
No caller API, financial semantics, enrollment subject contract, storage schema/path or
execution permission changed. Temporary TLS/socket resources are closed by tests; no keys,
credentials or test state are written to the repository. No new dependency/abstraction.

Review clarified actual enforcement: private_path checks UID/regular/single-link/symlink/
mode exposure, not GID/exact 0600; native Streamlit file permissions need custodian checks;
separate native/gateway configuration needs an operational exact comparison; fixture admin
404s are not deployed response assertions; CA CRL generation is not browser enforcement;
Windows tail IP in historical evidence belongs to the operator device, not VM. These limits
are explicitly documented. The OpenSSL extension-inspection command was corrected to a single
comma-separated -ext list so both SAN and EKU are displayed. Synthetic recipe verification
then passed. The future CA shell recipe uses set -eu so failure to create a new workspace
cannot fall through into overwriting an existing CA database. No operational lifetime/custodian
or missing tenant/browser identity was invented. The Windows port check also stops on query
errors rather than suppressing them as an apparent free port; occupied listeners are reported
without terminating unrelated processes.

## 17. Separate pre-commit review

Separate pre-commit review passed. The checker inspected **10 candidate files** (6 tracked
modifications, 4 new untracked files), new local Markdown links, secret-payload patterns,
new-file/tracked whitespace, exact HEAD/index and historical/runtime byte preservation.
It verified **350 tracked historical records/runtime Python files unchanged**, no unexpected
candidate files, no private key/JWT/credential payload or generated DB/certificate/binary,
and no broken new local link. Manual inspection additionally reviewed complete tracked
diffs and all new template/test/prompt/report contents, placeholders, procedures and readiness
claims. The final generated report had an extra blank line at EOF; the separate new-file
whitespace check caught it, it was removed, and the review was rerun. Pattern scans supplement
that review; they do not certify arbitrary secret absence.
No staging/commit was performed. Exact final Git inventory follows in section 21. Historical prompt/report bytes, runtime files, Compose,
Dockerfile, requirements and existing synthetic harness remain unchanged. Dated operational
addenda retain the full historical runbook/architecture/plan prefixes.

## 18. Remaining blockers and operator decisions

The private origin is selected and locally compatible. Outstanding independent decisions and
actions include tenant UUID and dedicated browser UUID; authorized registration/readback;
API v2 issuance/current scope discovery; browser delegated consent and confidential credential
custody/validity/rotation; CA/leaf validity, custodian, renewal/revocation/trust scope; actual
Windows hosts/tunnel endpoint/key acceptance; operational SAN/chain/permissions/trust; exact
API access-token subject verification/enrollment and real browser/session/token acceptance.

All unrelated Gate A source/privacy/exposure/semantic review/provider capability/tariff/
budget/shared quota/existing obligation/independent execution-custody requirements survive.
Gates B–E still require fresh Azure time/cost/start-stop authorization and state revalidation,
protected production files, explicit new-only initialization, one API/runner activation,
separate browser/workflow/live acceptance and recovery/deallocation evidence. No inference
permission, financial reservation or operational authority was created by this task.

No blocking offline compatibility conflict was found. Configured readiness does not establish
operational readiness. Offline TLS does not establish real browser trust. Role assignment
does not establish authenticated application access or runtime enrollment.

## 19. Final readiness matrix

| Verification area | Final status | Evidence / limit |
|---|---|---|
| Repository baseline | PASS | Exact expected HEAD, clean initial state, unchanged HEAD/index |
| Selected private origin | PASS | https://polymind.test:9443 selected and offline accepted |
| Deployment configuration consistency | PASS | Example origin/callback/Host/WS/SAN/tunnel 9443 agree; populated external files still need review |
| Streamlit OIDC template readiness | PASS | Installed 1.58 helper/parser regression; explicit inert placeholders |
| Entra API role assignment | OPERATOR_REPORTED_PASS | Configuration-level evidence only |
| Dedicated browser registration | PENDING | Absent from operator inventory; no mutation |
| Entra redirect URI acceptance | PENDING | Documentation-compatible; actual tenant readback absent |
| Offline TLS verification | PASS | Verified handshake, SAN/trust rejection, CA recipe and unsafe-input denial |
| Gateway Host/Origin verification | PASS | Executed TLS/HTTP/callback/WS/header allow/deny tests |
| SSH forwarding procedure | PASS | Reviewed Windows-native loopback command; final VM endpoint to reconfirm |
| Actual Windows hostname resolution | PENDING | No hosts edit or Windows/browser test |
| Operational TLS certificate provisioning | PENDING | Synthetic test material only |
| Actual browser certificate trust | PENDING | No trust installation/browser acceptance |
| Real Entra browser authentication | BLOCKED | Registration/consent/credentials/operational acceptance absent |
| Runtime access-token subject enrollment | BLOCKED | Exact verified API token sub not supplied; directory oid not a substitute |
| Production HTTPS verification | BLOCKED | VM operator-reported deallocated; no production activation |
| Regression suite | PASS | Focused 315 and full 3,329 passed, overlapping counts |
| Documentation reconciliation | PASS | Dated current records/procedures, historical evidence retained |
| Pre-commit review | PASS | Separate tracked/new-file review, index empty, no secret payload/artifact findings |

Acceptance gates **1–8 PASS within this task's offline configuration/procedure scope**.
Gate 5 establishes OIDC configuration requirements only; actual registration/authentication
remain independently pending/blocked. No unexecuted live check is classified PASS.

## 20. Recommended next separately authorized live-verification action

After operator review, authorize only dedicated **estudio-polymind-streamlit-dev** browser
registration using **https://polymind.test:9443/oauth2callback**, following the runbook's
inventory, scope-discovery and exact Web readback steps. Actual Entra URI acceptance must be
recorded before promoting it to VERIFIED. Keep consent/credential actions individually reviewed;
no VM activation, TLS issuance/trust installation, token acquisition, runtime initialization,
application startup or inference follows automatically. Stop if the tenant rejects the selected
URI and report the exact compatibility issue without substitution. Phase 19C remains NOT STARTED.

## 21. Git handoff and final validation addendum

The complete offline suite passed as recorded in section 14. Static Compose/TOML/compilation
and separate review also passed; no configured lint/type tool was omitted. The CA recipe
recheck after documentation review also passed (12 OpenSSL steps, 1.31 s); it is overlapping
verification, not a second test total. No application image build/transfer, five-service repeat
or live check is represented as new evidence.

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M deployment/phase19/compose.env.example
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
 M tests/unit/test_phase19_tls.py
?? deployment/phase19/streamlit.secrets.example.toml
?? docs/codex/prompts/phase_19b_private_https_origin_configuration_and_integration_verification.md
?? docs/codex/reports/phase_19b_private_https_origin_configuration_and_integration_verification.md
?? tests/unit/test_phase19_oidc_template.py
```

Final `git diff --stat` (tracked files only, excludes four untracked additions):

```text
 README.md                                          |  19 +-
 deployment/phase19/compose.env.example             |   3 +-
 .../evaluation/phase_19_deployment_architecture.md |  27 ++
 docs/evaluation/phase_19_implementation_plan.md    |  31 ++
 docs/operations/phase_19_vm.md                     | 368 +++++++++++++++++++++
 tests/unit/test_phase19_tls.py                     | 111 ++++++-
 6 files changed, 547 insertions(+), 12 deletions(-)
```

Final `git diff --name-status`:

```text
M	README.md
M	deployment/phase19/compose.env.example
M	docs/evaluation/phase_19_deployment_architecture.md
M	docs/evaluation/phase_19_implementation_plan.md
M	docs/operations/phase_19_vm.md
M	tests/unit/test_phase19_tls.py
```

`git diff --check` passed; `git diff --cached --name-only` was empty. New-file whitespace
checks passed separately. HEAD remains 1b11b3ab766240c162d1970bae438c00752c6c6f.
Candidate checkpoint files, all left unstaged/uncommitted:

- `README.md`
- `deployment/phase19/compose.env.example`
- `docs/evaluation/phase_19_deployment_architecture.md`
- `docs/evaluation/phase_19_implementation_plan.md`
- `docs/operations/phase_19_vm.md`
- `tests/unit/test_phase19_tls.py`
- `deployment/phase19/streamlit.secrets.example.toml`
- `docs/codex/prompts/phase_19b_private_https_origin_configuration_and_integration_verification.md`
- `docs/codex/reports/phase_19b_private_https_origin_configuration_and_integration_verification.md`
- `tests/unit/test_phase19_oidc_template.py`

Proposed commit message for operator review:

```text
chore: configure Phase 19B private HTTPS origin and verify deployment integration
```

No Git staging, commit or push occurred. No cloud session, production runtime or operational
certificate/trust action followed this handoff. Stop for operator review; separately authorize
the dedicated browser registration as described in section 20.

```text
PHASE19B_PRIVATE_ORIGIN_CONFIGURATION: PASS
SELECTED_PRIVATE_ORIGIN: https://polymind.test:9443
SELECTED_OIDC_REDIRECT_URI: https://polymind.test:9443/oauth2callback
CONFIGURATION_CONSISTENCY: PASS
ARCHITECTURE_COMPATIBILITY: PASS
OFFLINE_TLS_VERIFICATION: PASS
GATEWAY_SECURITY_VERIFICATION: PASS
STREAMLIT_OIDC_CONFIGURATION: PASS
ENTRA_API_ROLE_ASSIGNMENT: OPERATOR_REPORTED_PASS
ENTRA_BROWSER_REGISTRATION: PENDING
ENTRA_REDIRECT_URI_ACCEPTANCE: PENDING
SSH_TUNNEL_PROCEDURE: PASS
OPERATIONAL_TLS_PROVISIONING: PENDING
BROWSER_CERTIFICATE_TRUST: PENDING
REAL_ENTRA_AUTHENTICATION: BLOCKED
RUNTIME_SUBJECT_ENROLLMENT: BLOCKED
PRODUCTION_PRIVATE_HTTPS: BLOCKED
APPLICATION_RUNTIME_CODE_CHANGED: NO
APPLICATION_IMAGE_REBUILD_REQUIRED: NO
AZURE_STAGED_CONFIGURATION_UPDATE_REQUIRED: YES
FOCUSED_REGRESSION_VERIFICATION: PASS
FULL_OFFLINE_REGRESSION_VERIFICATION: PASS
DOCUMENTATION_RECONCILIATION: PASS
PRE_COMMIT_REVIEW: PASS
AZURE_VM_ACTIVATED_DURING_TASK: NO
ENTRA_MUTATIONS_DURING_TASK: NO
OPERATIONAL_CERTIFICATES_CREATED: NO
PRODUCTION_AUTHORITIES_MODIFIED: NO
PRODUCTION_SERVICES_ACTIVATED: NO
REAL_INFERENCE_CALLS_DURING_TASK: 0
PUBLIC_EXPOSURE_INTRODUCED: NO
GIT_STAGED: NO
GIT_COMMIT_CREATED: NO
GIT_PUSH_PERFORMED: NO
PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED
NEXT_ACTION_READINESS: READY_FOR_OPERATOR_REVIEW
```
