# CODEX MASTER PROMPT — PHASE 19B
## Azure Private VM Post-Provisioning Verification and Recovery Readiness

**Project:** Estudio PolyMind
**Repository:** Susanta2025-lab/estudio-polymind-llm-orchestration
**Branch:** master
**Phase:** 19B — Azure VM Deployment and Real-Model Integration
**Stage:** Live infrastructure verification following VM provisioning
**Task:** Independently verify the newly provisioned private Azure VM, networking, storage, bootstrap, SSH readiness, Tailscale prerequisites, independent recovery, and cost controls.
**Execution environment:** Local WSL Ubuntu, Azure CLI, Windows PowerShell interoperability
**Date context:** 24 November 2026
**Mode:** Evidence-first; bounded live infrastructure checks; no paid inference

---

# 1. MISSION

Continue Phase 19B from the actual deployed Azure infrastructure.

The Azure VM has already been created successfully by the operator. Do NOT repeat provisioning.

Your mission is to:

1. Verify the actual Azure VM configuration.
2. Establish the VM creation timestamp and remaining eight-hour evaluation window.
3. Verify the absence of a public VM IP.
4. Verify VM security, Trusted Launch, SSH configuration and managed disks.
5. Verify VNet, subnet, NIC, NAT Gateway, NSG and AKS isolation.
6. Verify Azure VM Agent and independent recovery capability.
7. Inspect actual cloud-init execution and first-boot results.
8. Verify OpenSSH and Tailscale installation and services.
9. Validate the protected-parameter mechanism using non-secret test values.
10. Prepare for real Tailscale enrollment without exposing credentials.
11. Verify Windows SSH prerequisites and prepare private connectivity testing.
12. Produce an evidence-based PASS/GAP/FAIL report.
13. Preserve all existing repository changes and governance constraints.
14. Identify the exact remaining work before application deployment.

The objective is VERIFIED infrastructure readiness, not merely reproducing earlier planned settings.

Do not claim successful cloud bootstrap, Tailscale connectivity, recovery or SSH authentication until supported by actual evidence.

---

# 2. PROJECT AND REPOSITORY CONTEXT

Estudio PolyMind is a provider-neutral, governed multi-LLM orchestration platform.

The current implementation includes:

- FastAPI backend.
- Streamlit interfaces.
- LangGraph-based orchestration.
- Chat/RAG functionality.
- Governed document digestion and intelligence.
- Persistent Chroma vector storage.
- Redis memory/state support.
- Durable SQLite security, governance, admission and workflow authorities.
- Provider-neutral inference abstractions.
- Azure Foundry/OpenAI-compatible integration.
- Authentication, authorization, financial governance and provenance protections.
- Independent execution permissions for potentially billable workflows.

Phase 19 has exactly three formal stages:

- Phase 19A — Readiness verification.
- Phase 19B — Deployment and real-model integration.
- Phase 19C — Validation and documentation.

This task remains WITHIN Phase 19B.

The selected deployment architecture is:

```text
Authorized Windows operator
    |
Windows Tailscale + Windows OpenSSH
    |
Private Tailscale network
    |
Azure Ubuntu VM — no public VM IP
    |
Docker Compose
    |
HTTPS gateway — host 127.0.0.1:9443
    |
Streamlit + FastAPI + one document worker
    |
Persistent Redis, Chroma and SQLite authorities
    |
Separately authorized external inference provider
```

The Phase 19 Compose file is:

`docker-compose.phase19.yml`

Its five services are:

- api
- ui
- gateway
- redis
- chroma

The gateway binds host loopback only:
`127.0.0.1:9443`

Do not publish internal API, Redis, Chroma or worker ports.

Keep private HTTPS hostname, TLS certificate, browser origin and Entra callback requirements intact.

Do not treat localhost-only access as proof of real browser/OIDC acceptance.

AKS is NOT required for Phase 19.

---

# 3. MANDATORY REPOSITORY INVESTIGATION

Before any Azure live probe:

Read:

- AGENTS.md
- README.md
- docs/operations/phase_19_vm.md
- docs/evaluation/phase_19_deployment_architecture.md
- docs/evaluation/phase_19_implementation_plan.md
- docs/codex/reports/phase_19a_readiness_report.md
- docs/codex/reports/phase_19b_offline_implementation_and_verification.md
- docker-compose.phase19.yml
- deployment/phase19/ relevant deployment and configuration files

Also inspect any LOCAL Phase 19B continuation prompts and reports, particularly:

- docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
- docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md

These continuation files may be uncommitted and absent from remote GitHub.

Use the actual local working tree as the primary source.

Read the relevant portions of prior Phase 17/18 governance, identity, authorization, provider and deployment documentation when needed.

Do not use older planning documents to override later operator-approved decisions.

Inspect:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -8
git diff --check
git diff --cached --name-only
```

Record the actual baseline.

Do not assume the working tree is clean.

Never reset, stash, clean, discard, rebase, checkout another branch, commit or push.

---

# 4. OPERATOR-CONFIRMED AZURE BASELINE

The following information was provided by the operator during the live provisioning process.

Treat it as an observed historical baseline requiring independent verification where possible.

## 4.1 Azure subscription

Subscription name:
ECI-Development

Subscription ID:
970e5901-0d2d-44de-ade7-92ce4eb61a73

Subscription state:
Enabled

Resource group:
rg-epolymind

Location:
spaincentral

Azure CLI:
2.93.0

Do not switch subscriptions without operator authorization.

## 4.2 VM creation result

The operator executed the approved VM creation command.

Azure returned:

- VM name: vm-epolymind-dev
- Location: spaincentral
- Resource group: rg-epolymind
- Power state: VM running
- Private IP: 10.50.0.36
- Public IP: empty
- FQDN: empty

The creation operation returned successfully.

This DOES NOT prove that cloud-init, Tailscale, SSH or the Azure VM Agent is healthy.

## 4.3 Intended VM properties

- Size: Standard_D2s_v4
- vCPUs: 2
- RAM: 8 GiB
- Operating system: Ubuntu Server 24.04 LTS
- Architecture: x64
- Hyper-V generation: V2
- Image: Canonical:ubuntu-24_04-lts:server:24.04.202611170
- Admin username: polymindadmin
- Authentication: Ed25519 SSH public key
- OS disk: 64 GiB StandardSSD_LRS
- Data disk: 64 GiB StandardSSD_LRS
- Intended security type: TrustedLaunch
- OS disk delete option: Detach
- Data disk delete option: Detach
- NIC delete option: Delete

Inspect actual Azure state rather than assuming all requested options were applied.

The Azure creation output included an advisory message recommending Trusted Launch. It does not independently establish the actual security configuration.

## 4.4 Private networking

Existing VNet:
vnet-epolymind-private-dev

VNet CIDR:
10.50.0.0/24

VM subnet:
snet-polymind-vm

VM subnet CIDR:
10.50.0.32/27

VM private IP:
10.50.0.36

Subnet defaultOutboundAccess:
false

Attached NSG:
nsg-epolymind-vm-dev

Attached NAT Gateway:
nat-epolymind-vm-dev

NAT public IP resource:
pip-epolymind-nat-dev

The VM itself must have NO public IP.

Do not create an additional public IP, NSG, VNet, subnet, NAT Gateway, Bastion or load balancer.

## 4.5 Verified custom NSG rules before deployment

Priority 100:
DenyAKSOutbound
Outbound / Deny
Destination 10.224.0.0/12
Any protocol/port

Priority 200:
AllowOutboundHTTPS
Outbound / Allow
Destination Internet
TCP 443

Priority 4096:
DenyAllOutbound
Outbound / Deny
Any destination/port

Priority 4096:
DenyAllInbound
Inbound / Deny
Any source/port

The NSG is associated with the VM subnet.

Inspect effective rules and default Azure platform behavior before drawing conclusions.

TCP 443 is expected to support HTTPS package repositories, Tailscale control/relay connectivity and relevant Azure services.

Do not assume direct UDP Tailscale transport is available.

Azure DNS, time synchronization and VM Agent prerequisites must be assessed separately.

## 4.6 Existing AKS infrastructure

An existing AKS cluster belongs to the broader Azure environment.

Earlier checks established:

- AKS power state: Stopped
- AKS virtual network address space: 10.224.0.0/12
- Existing reciprocal VNet peerings: Connected
- Existing peering configurations must remain untouched

Do not start, stop, modify or redeploy AKS.

Do not alter the existing peering relationships.

Verify that the private VM does not acquire unintended access to AKS or its managed resources.

---

# 5. WINDOWS AND TAILSCALE BASELINE

## 5.1 Windows machine

Operator device:
susanta-hp-pro

Operating system:
Windows 11

Windows Tailscale:
Previously authenticated and online

Windows OpenSSH:
Installed

Observed OpenSSH version:
OpenSSH_for_Windows_9.5p2

The Linux project working environment is WSL Ubuntu with zsh.

When issuing shell scripts, do not alter persistent zsh options such as `set -u`.

Use explicit Bash subshells where strict shell behavior is needed.

## 5.2 SSH key

A dedicated Ed25519 key pair was generated using Windows PowerShell.

Private key:
Windows user profile `.ssh/id_ed25519_polymind_azure`

Public key:
Windows user profile `.ssh/id_ed25519_polymind_azure.pub`

The public key was verified as accessible from WSL.

The private key has a passphrase.

Do not read, print, copy, upload, alter permissions of or expose the private key.

Do not request its passphrase in a Codex chat or report.

Verify Azure VM authorized-key configuration using non-secret metadata and fingerprints where possible.

The key must remain outside Git.

## 5.3 Tailscale identity and policy

The operator initially configured a tag in an unused GitHub-associated Tailscale account.

That was corrected.

The intended active tailnet is the operator's existing personal-email-associated tailnet containing:

Windows laptop:
susanta-hp-pro
Previously observed Tailscale IP: 100.108.249.65

Android phone:
susantas-a27
Previously observed Tailscale IP: 100.64.92.70

These IP addresses are historical observations and must be rechecked before use.

A dedicated tag was created:

tag:polymind-vm

Tag assignment:
autogroup:admin

The operator reported saving a restricted policy that:

- Preserves access among personal user-owned devices.
- Permits the Windows laptop to access the tagged PolyMind VM over TCP 22.
- Does not grant the Android phone access to the tagged VM.
- Does not grant the tagged VM access to personal devices.
- Removes the unrestricted allow-all network grant.
- Includes policy tests.
- Retains the prior Tailscale SSH policy.

Do not assume the live policy or its tests were independently verified by Codex.

If Tailscale admin API credentials are unavailable, prepare an operator-side verification checklist.

Do not change the tailnet policy without explicit authorization.

PolyMind uses standard OpenSSH, not Tailscale SSH.

---

# 6. CLOUD-INIT BASELINE

The operator created:

/tmp/polymind-tailscale-cloud-init.yaml

Local verification completed:

```text
CLOUD_INIT_YAML_VALID
SSH_PASSWORD_AUTH_DISABLED: True
ROOT_LOGIN_DISABLED: True
WRITE_FILES_ENTRIES: 1
BOOTSTRAP_BASH_SYNTAX_PASS
```

The first-boot script is intended to:

1. Verify Ubuntu 24.04.
2. Configure HTTPS Ubuntu package sources.
3. Install required packages.
4. Install Tailscale using the official Ubuntu Noble package repository.
5. Install/enable OpenSSH.
6. Disable SSH password authentication.
7. Disable SSH root login.
8. Enable tailscaled.
9. Leave Tailscale registration pending.

Expected guest script:
/usr/local/sbin/polymind-firstboot.sh

Expected completion marker:
POLYMIND_BOOTSTRAP_COMPLETE

These were local syntax/configuration checks only.

They are NOT evidence that cloud-init finished successfully on the Azure VM.

Verify actual VM bootstrap results, logs, installed packages and services.

Do not regenerate cloud-init or recreate the VM automatically if a failure is found.

---

# 7. SPENDING, EXECUTION AND SECURITY BOUNDARIES

The operator approved:

- Maximum eight-hour VM evaluation.
- USD 30 incremental spending TARGET.
- VM deallocation at the end of the evaluation.
- NAT Gateway/public IP removal after access is no longer required.
- Up to 30 days of disk retention, subject to review.

The USD 30 target is NOT an Azure-enforced hard spending cap.

The NAT Gateway and its public IP were already created before the VM and may incur independent charges.

FIRST PRIORITY:

Query the VM's actual timeCreated, current state and current UTC time.

Determine:

- Elapsed time since provisioning.
- Estimated remaining evaluation time.
- Whether the VM remains allocated.
- Estimated incremental cost, clearly labeled if unverified.
- Ongoing NAT/public IP and disk exposure.
- Expected cutoff for deallocation.

Do not reset the eight-hour clock because Codex started later.

If a reliable time/cost assessment is impossible, mark a governance GAP.

If the approved evaluation window has already expired and the VM remains allocated, use the operator-approved deallocation procedure after recording evidence. Never delete the VM or attached disks automatically.

Prioritize preventing unapproved continued VM compute spending over completing optional diagnostics.

No autonomous monitoring or future scheduled action is implied by this prompt. Report if ongoing monitoring is unavailable.

STRICTLY FORBIDDEN:

- New Azure VM, IP, network, gateway or managed service creation.
- Recreating or resizing the VM.
- AKS changes.
- Foundry model/deployment changes.
- Paid inference or provider smoke calls.
- Credential renewal/retrieval or API-key inspection.
- Real Entra user registration or consent changes.
- Execution approval signing.
- Financial/governance database modifications.
- Public SSH or application exposure.
- Production service launch without separate approval.
- Destructive storage formatting, filesystem repair or deletion.
- Unapproved firewall-policy relaxation.
- Git commits, pushes, resets or cleanup.
- Installing extra Azure extensions unnecessarily.
- Tailscale credential exposure.

Existing Phase 17/18 financial, security, identity and execution-governance invariants remain binding.

---

# 8. WORK PACKAGE A — AZURE CONTROL-PLANE VERIFICATION

Use Azure CLI in the operator's authenticated WSL session.

Begin with read-only commands.

Verify:

1. Actual subscription and tenant.
2. VM existence, exact name, region and resource ID.
3. VM power/provisioning status.
4. Creation time.
5. Hardware SKU.
6. Image publisher, offer, SKU and version.
7. Linux architecture/OS.
8. SecurityProfile.securityType.
9. Secure Boot status.
10. vTPM status.
11. OS disk properties.
12. Data disk count and properties.
13. Disk delete options.
14. NIC identities and attachment.
15. All NIC IP configurations.
16. Actual private IP.
17. No public IP references.
18. Absence of accidental new networking resources.

Start with commands such as:

```bash
az account show

az vm show \
  -g rg-epolymind \
  -n vm-epolymind-dev \
  -o json

az vm get-instance-view \
  -g rg-epolymind \
  -n vm-epolymind-dev \
  -o json

az vm list-ip-addresses \
  -g rg-epolymind \
  -n vm-epolymind-dev \
  -o json

az network nic list \
  -g rg-epolymind \
  -o json

az disk list \
  -g rg-epolymind \
  -o json
```

Use targeted queries to limit sensitive or irrelevant output in the report.

Check command availability in Azure CLI 2.93.0.

Distinguish verified actual state from intended configuration.

Do not accept the creation response alone as full evidence.

---

# 9. WORK PACKAGE B — NETWORK SECURITY VERIFICATION

Independently inspect:

- VNet and subnet IDs/CIDRs.
- VM NIC subnet membership.
- NSG attachment and effective NSG rules.
- NAT Gateway attachment.
- NAT public IP association.
- Default outbound access setting.
- Existing AKS peerings.
- Existing AKS address-range deny.
- Inbound SSH/HTTP/HTTPS exposure.
- Unexpected public endpoints or load balancer attachments.

Do not modify any NSG rule at this stage.

Evaluate:

- Whether normal Azure inbound traffic is denied.
- Whether the VM has a direct public IP.
- Whether the NAT is configured for expected outbound traffic.
- Whether Tailscale can reach its coordination/relay infrastructure over HTTPS.
- Whether package installation requires any currently denied egress.
- Whether Azure platform DNS and VM Agent communication remain available.
- Whether guest firewalls and Tailscale policy need additional verification.

NSG configuration alone cannot prove reachability.

Distinguish control-plane checks from guest-level tests.

Do not test internet exposure by temporarily opening SSH.

---

# 10. WORK PACKAGE C — VM AGENT AND RECOVERY

Inspect:

- VM Agent status and version.
- Provisioning/extension statuses.
- Agent-related errors.
- Azure Run Command support.
- Availability of a management path independent of Tailscale.

Use the established Azure VM Agent communication mechanism.

Perform one bounded, non-secret, non-destructive Run Command recovery probe if:

1. The VM remains within the approved evaluation window.
2. Azure CLI identity and target VM are verified.
3. There is no cost or governance blocker.

Suggested probe:

```bash
az vm run-command invoke \
  --resource-group rg-epolymind \
  --name vm-epolymind-dev \
  --command-id RunShellScript \
  --scripts 'printf "AZURE_RUN_COMMAND_RECOVERY_OK\n"'
```

Record the exact execution result, status, exit code and completion marker.

Do not use Run Command for wide-ranging guest changes.

If the probe fails:

- Capture sanitized diagnostic evidence.
- Determine whether the cause is Agent, provisioning, network, RBAC or command availability.
- Report a blocker.
- Do not repeatedly invoke it without understanding the failure.

Also assess fallback recovery:

- Managed disk repair via controlled detachment.
- Azure Serial Console availability.
- Boot diagnostics requirements.
- Limitations imposed by disabled password authentication.

Do not enable SSH password authentication merely to make serial login easier.

Do not detach disks, enable boot settings or perform a disk repair without separate approval.

---

# 11. WORK PACKAGE D — CLOUD-INIT AND BOOTSTRAP

After establishing the VM Agent recovery path, use a bounded, read-only guest diagnostic script to check:

- cloud-init status.
- cloud-init completion/error records.
- Guest OS version.
- Installation of openssh-server.
- Installation of tailscale.
- SSH service status.
- tailscaled service status.
- OpenSSH effective authentication configuration.
- Relevant listening sockets.
- Guest firewall status.
- HTTPS package repository reachability if necessary.
- Presence of the expected bootstrap completion marker.

Relevant inspection commands may include:

```bash
cloud-init status --long
systemctl is-active ssh
systemctl is-active tailscaled
ss -lnt
sshd -T
dpkg-query
journalctl
```

Avoid printing complete configuration files or logs if they may contain credentials.

Use targeted and sanitized log extracts.

Treat failed installation or missing marker as a GAP/FAIL, not an automatic repair authorization.

Do not rerun first-boot package installation blindly.

Do not introduce public SSH access.

---

# 12. WORK PACKAGE E — PROTECTED PARAMETER VALIDATION

The Azure CLI was verified to support:

```text
az vm run-command create
--protected-parameters
```

Managed Run Command is the proposed mechanism for Tailscale enrollment.

Verify the CURRENT Azure CLI and Microsoft documentation for:

- Protected parameter representation.
- Linux environment-variable delivery.
- Run Command execution permissions.
- Command status/result retrieval.
- Resource cleanup.
- Logging and output behavior.
- Secret exposure risks on the LOCAL workstation.
- Azure CLI argument/process-list exposure.

Critical distinction:

Azure protected parameters do not automatically make a raw secret safe if it appears in the shell command line or local process arguments.

First validate behavior using a DUMMY, NON-SECRET value only.

If possible, prove:

- The parameter reaches the script under the expected name.
- The script can consume it without printing it.
- The command returns only a safe marker.
- The real value would not need to be embedded in source files, chat, command history or process arguments.

Do not generate or consume a real Tailscale authentication key at this stage.

If a secure handoff cannot be established, report:

`PROTECTED_TAILSCALE_HANDOFF: GAP`

Do not improvise with insecure CLI arguments.

Do not create a Key Vault or other managed service without separate approval.

---

# 13. WORK PACKAGE F — TAILSCALE ENROLLMENT READINESS

Confirm the expected enrollment design:

- Correct existing personal-email tailnet.
- VM tag: tag:polymind-vm
- Single-use authentication key.
- Short key-validity period.
- Non-ephemeral server identity.
- Standard OpenSSH.
- Tailscale SSH disabled.
- No subnet routes advertised.
- No exit-node advertisement.
- No acceptance of unnecessary routes.
- Preserve Azure DNS settings, using --accept-dns=false as planned.

The VM is NOT yet proven to be enrolled.

Do not infer successful enrollment because tailscaled is installed.

Generate no authentication key automatically.

For an operator-authorized subsequent enrollment, use:

- A reviewed secret-safe delivery mechanism.
- A short-lived single-use tagged key.
- No secret output.
- An auditable completion marker.
- Explicit verification of the correct tailnet and device tag.

If the key-delivery mechanism is not verified, stop before enrollment.

Treat real enrollment as an explicit operator-controlled security action.

---

# 14. WORK PACKAGE G — WINDOWS SSH AND PRIVATE CONNECTIVITY

Reverify Windows-side prerequisites where possible using PowerShell interoperability.

Check without revealing credentials:

- Windows Tailscale backend running.
- Correct active tailnet.
- Windows OpenSSH availability.
- Dedicated Ed25519 key present.
- Public-key fingerprint.
- Approved Windows Tailscale device identity and IP.

Once the VM is deliberately enrolled, verify:

1. VM appears online in the correct tailnet.
2. VM has tag:polymind-vm.
3. Windows-to-VM TCP 22 is permitted by the saved policy.
4. Standard SSH accepts the dedicated key.
5. Password/root login protections remain effective.
6. Android-to-VM SSH is not granted by policy.
7. Direct public-IP SSH is impossible because the VM has no public IP.

Actual SSH may require interactive passphrase entry on the operator's Windows machine.

Never collect or log that passphrase.

Do not claim SSH PASS if only Azure Run Command succeeds.

Do not enable Tailscale SSH as a shortcut.

After application deployment, the intended HTTPS access is via SSH local port forwarding to the VM's loopback-bound gateway.

Preserve the approved private HTTPS hostname, TLS identity, origin and Entra redirect.

Do not introduce certificate validation bypasses.

The application is not deployed merely because the VM is reachable.

---

# 15. WORK PACKAGE H — DISK AND PERSISTENCE READINESS

Verify from Azure:

- 64-GiB Standard SSD OS disk.
- 64-GiB Standard SSD data disk.
- Disk attachment states.
- Intended disk delete options.
- Appropriate independent storage identities.

From the guest, when recovery access is available, inspect:

- Block devices.
- Filesystems.
- Current mounts.
- Availability of the intended data disk.
- Whether the disk is blank or already formatted.
- Whether /srv/polymind exists.
- Whether any unexpected authorities or application data exist.

READ-ONLY ONLY.

Do NOT:

- Run mkfs.
- Partition a disk.
- Rewrite fstab.
- Change disk ownership.
- Create or initialize governance databases.
- Start the production Compose stack.

The repository requires durable local storage on an appropriate filesystem such as ext4.

Do not place SQLite authorities on ephemeral storage or network shares.

Report the exact subsequent disk-initialization requirements separately.

The eventual persistent storage must preserve security, governance, admission, jobs, publication, object store, Redis and Chroma state.

No automatic initialization or historical authority replacement is authorized.

---

# 16. WORK PACKAGE I — COST AND TEARDOWN GOVERNANCE

Verify and report:

- VM creation timestamp UTC.
- Current UTC timestamp.
- Elapsed time.
- Remaining approved evaluation window.
- VM allocation/power state.
- Current SKU and expected compute meter.
- NAT Gateway and public IP retention.
- Managed disk retention charges.
- Possible snapshots or unexpected new resource charges.
- Whether pricing evidence is current and source-backed.

Approved limits:

VM evaluation: eight hours maximum.
Incremental target: USD 30.
No automatic billing hard cap exists.

Do not claim exact accrued charges from estimates.

Do not perform expensive or prolonged benchmarks.

When the authorized runtime ends, deallocate the VM using the approved procedure:

```bash
az vm deallocate \
  --resource-group rg-epolymind \
  --name vm-epolymind-dev
```

Use this only when deallocation is due under the operator-approved evaluation boundary or explicitly requested.

Afterward, verify actual deallocated status.

Do not automatically delete:

- VM
- OS disk
- Data disk
- NAT Gateway
- NAT public IP
- VNet
- NSG
- Existing AKS resources

Prepare a resource-specific teardown inventory and command plan.

NAT removal must be separately coordinated so that required outbound access is not unexpectedly interrupted.

If the current VM runtime has already exceeded the approved window, do not run more optional VM probes before addressing deallocation.

---

# 17. TEST CLASSIFICATION AND ACCEPTANCE GATES

Classify every requirement as:

PASS:
Verified against actual evidence.

GAP:
Incomplete configuration, unexecuted verification or unresolved requirement.

FAIL:
Observed incompatible, unsafe or failed behavior.

UNKNOWN:
Insufficient evidence or inaccessible environment.

Do not equate:

- Azure VM creation with bootstrap completion.
- NSG associations with working network connectivity.
- SSH public-key presence with successful SSH authentication.
- Tailscale installation with successful enrollment.
- Azure Agent running with independent recovery PASS.
- Dummy protected parameters with real secret-safe operator handoff.
- Cloud-init syntax validation with live execution.
- Guest disk attachment with persistent filesystem readiness.
- Docker Compose offline PASS with live deployment PASS.
- VM readiness with real Entra acceptance.
- Application readiness with authorization for paid model inference.

Provide an evidence matrix covering all these distinctions.

---

# 18. REPORT AND DOCUMENTATION OUTPUTS

Create or update, without overwriting previous evidence:

docs/codex/prompts/phase_19b_post_vm_creation_verification.md

docs/codex/reports/phase_19b_post_vm_creation_verification.md

Save this task's prompt as the first file.

The report must contain:

1. Executive assessment.
2. Actual Git baseline.
3. Operator-supplied historical Azure baseline.
4. Actual Azure control-plane observations.
5. Timestamp and spending analysis.
6. VM security and Trusted Launch.
7. NIC/subnet/NSG/NAT/AKS isolation.
8. OS/data disk findings.
9. VM Agent and Run Command recovery result.
10. Cloud-init and bootstrap results.
11. Tailscale installation/enrollment readiness.
12. Protected-parameter verification.
13. Windows/SSH connectivity readiness.
14. Evidence table with exact commands and sanitized outputs.
15. PASS/GAP/FAIL/UNKNOWN decisions.
16. Blockers, security risks and required operator actions.
17. Follow-on tasks required before Docker Compose application deployment.
18. Safe deallocation and network teardown plan.
19. Git status and changed-file inventory.

If appropriate, append a narrowly scoped, dated operational finding to:

docs/operations/phase_19_vm.md

Do not rewrite historical Phase 19A or 19B reports.

Do not falsely update older documents from "Azure not activated" into a claim that live inference has been authorized.

Preserve the temporal distinction between historical offline evidence and new Azure activation.

---

# 19. VERIFICATION AND GIT SAFETY

After report creation:

- Inspect the diff.
- Run git diff --check.
- Inspect changed/untracked files.
- Verify no credentials, authorization headers, private keys, authentication tokens, sensitive database contents or raw sensitive logs entered source control.
- Preserve every existing modification.
- Do not commit, push, stage broadly, reset, stash, clean or discard any file.
- Do not invent test counts.
- Do not rerun the complete application regression suite unless a source change creates a justified dependency.

This is primarily infrastructure verification, not an application-code implementation task.

Avoid unrelated refactoring.

---

# 20. FINAL MACHINE-READABLE VERDICT

Finish with an explicit result block:

```text
PHASE_19B_VM_PROVISIONING: PASS/GAP/FAIL
PHASE_19B_VM_SECURITY: PASS/GAP/FAIL
PHASE_19B_PRIVATE_NETWORK: PASS/GAP/FAIL
PHASE_19B_DISK_ATTACHMENT: PASS/GAP/FAIL
PHASE_19B_CLOUD_INIT: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_OPENSSH_SERVICE: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_TAILSCALE_INSTALLATION: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_TAILSCALE_ENROLLMENT: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_PROTECTED_PARAMETER_HANDOFF: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_AZURE_RUN_COMMAND_RECOVERY: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_WINDOWS_PRIVATE_SSH: PASS/GAP/FAIL/UNKNOWN
PHASE_19B_COST_GOVERNANCE: PASS/GAP/FAIL
PHASE_19B_INFRASTRUCTURE_READY: YES/WITH_CONDITIONS/NO
PHASE_19B_APPLICATION_DEPLOYMENT_READY: YES/WITH_CONDITIONS/NO
PHASE_19B_REAL_MODEL_INFERENCE_AUTHORIZED: NO
PHASE_19B_PUBLIC_EXPOSURE_AUTHORIZED: NO
PHASE_19B_AKS_REQUIRED: NO
```

For every GAP, FAIL or UNKNOWN, provide the smallest safe next action and the evidence required to close it.

Do not claim Phase 19B or Phase 19C complete merely because infrastructure checks pass.

---

# 21. STOP CONDITIONS

Stop live operations immediately if:

- The wrong Azure subscription is active.
- The Azure VM identity does not match the approved target.
- The VM has an unexpected public IP.
- The approved evaluation window has expired.
- An action requires new Azure resource spending without approval.
- VM Agent/Run Command appears unsafe or unreliable.
- Tailscale credential handling would expose a secret.
- A request would initiate real inference or modify financial authority.
- Existing repository changes would be lost.
- Any proposed repair requires broadening public access.
- Existing critical controls would be weakened.

Report the blocker and preserve evidence.

The desired final outcome is a trustworthy post-provisioning assessment, a controlled private-access handoff and a precise list of remaining requirements.

Do not automatically proceed to production application deployment.
