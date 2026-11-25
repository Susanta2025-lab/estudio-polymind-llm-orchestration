# CODEX MASTER PROMPT — PHASE 19B
## Targeted OpenSSH / Cloud-init Repair and Live Revalidation

**Project:** Estudio PolyMind
**Repository:** Susanta2025-lab/estudio-polymind-llm-orchestration
**Branch:** master
**Phase:** 19B — Azure VM Deployment and Real-Model Integration
**Stage:** Controlled Post-Provisioning Repair and Revalidation
**Task:** Repair the verified OpenSSH runtime/bootstrap failure, restore secure SSH service readiness and verify the resulting VM state.
**Date:** 24 November 2026
**Execution:** WSL Ubuntu + existing authenticated Azure CLI
**Mode:** Evidence-first, minimal live mutation, strict time and cost gates

---

# 1. MISSION

Continue Phase 19B from the completed post-VM-creation verification report.

The Azure VM was successfully provisioned, but its first-boot cloud-init script failed during OpenSSH validation.

The failure is specific and already investigated.

Your mission is to:

1. Verify the current Azure VM and remaining evaluation window.
2. Independently confirm the recorded OpenSSH failure.
3. Inspect the actual SSH systemd service/socket configuration.
4. Identify the smallest safe repair.
5. Apply only the explicitly authorized SSH service/runtime repair, if its prerequisites pass.
6. Revalidate SSH daemon syntax, effective security controls and service health.
7. Preserve the original cloud-init failure evidence.
8. Prepare a corrected first-boot source configuration for future deployments.
9. Verify Azure Run Command recovery remains operational.
10. Document executed results and remaining infrastructure blockers.
11. Stop without attempting Tailscale enrollment, data-disk initialization or application deployment.

Do not rebuild the VM.

Do not redesign Phase 19.

Do not introduce additional Azure infrastructure.

This is a targeted repair, not a general cloud-hardening or deployment task.

---

# 2. MANDATORY REPOSITORY BASELINE

Read AGENTS.md and inspect the current working tree before making changes.

Read the following sources completely where available:

- docs/operations/phase_19_vm.md
- docs/evaluation/phase_19_deployment_architecture.md
- docs/evaluation/phase_19_implementation_plan.md
- docs/codex/reports/phase_19b_offline_implementation_and_verification.md
- docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
- docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
- docs/codex/prompts/phase_19b_post_vm_creation_verification.md
- docs/codex/reports/phase_19b_post_vm_creation_verification.md

The latest post-creation report is the PRIMARY source of actual live-state evidence.

Inspect these commands:

git status --short --branch
git log --oneline -8
git rev-parse HEAD
git diff --check
git diff --cached --name-only

The earlier observed HEAD was:

7bf82dc2da4a9f29561a5f493b690502c0090eb0

Do not assume HEAD is unchanged.

Existing tracked/untracked Phase 19B documentation is valuable and must be preserved.

Do not:

- Reset or clean the working tree.
- Stash or discard files.
- Create a Git branch.
- Commit or push.
- Rewrite prior verification reports.
- Overwrite historical deployment evidence.
- Modify unrelated application source.

Work directly on the existing master working tree.

---

# 3. VERIFIED AZURE BASELINE

Subscription:
ECI-Development

Subscription ID:
970e5901-0d2d-44de-ade7-92ce4eb61a73

Resource group:
rg-epolymind

Azure region:
spaincentral

VM:
vm-epolymind-dev

Private IPv4:
10.50.0.36

VM public IP:
None

VM size:
Standard_D2s_v4

Operating system:
Ubuntu Server 24.04 LTS

Security:
TrustedLaunch

Secure Boot:
Enabled

vTPM:
Enabled

OS disk:
64 GiB StandardSSD_LRS

Data disk:
64 GiB StandardSSD_LRS

Azure VM Agent:
Ready

Previously observed Agent version:
2.16.0.2

Independent Azure Run Command recovery:
PASS

The successful recovery marker was:

AZURE_RUN_COMMAND_RECOVERY_OK

No Tailscale enrollment has occurred.

No production Compose application has been deployed.

The data disk remains unformatted and unmounted.

---

# 4. STRICT EVALUATION DEADLINE

The VM creation timestamp was:

2026-11-24T01:26:38.7760141+00:00

The operator approved:

- Maximum eight-hour VM evaluation.
- USD 30 incremental infrastructure spending target.
- Deallocation at the evaluation cutoff.
- Retention of managed disks pending separate review.
- Coordinated NAT/public-IP teardown after their use ends.

The exact deadline is:

2026-11-24T09:26:38.7760141+00:00

This deadline is an absolute UTC timestamp.

It must NOT be recalculated from Codex start time.

FIRST ACTION:

Read current UTC time and actual Azure VM power state.

Verify:

- Correct subscription.
- Correct VM resource ID.
- Actual current UTC time.
- Elapsed evaluation time.
- Remaining time.
- Whether the VM is allocated.

If fewer than 30 minutes remain, do not initiate an optional repair sequence that could overrun the cutoff.

Prioritize safe deallocation and reporting.

If the cutoff has already passed and the VM remains allocated, execute the previously approved bounded deallocation procedure after verifying exact identity.

Verify actual PowerState/deallocated.

Do not automatically restart a deallocated VM.

No further VM spending authorization is implied.

The operator remains responsible for cutoff coverage if this Codex execution ends before the deadline.

Never claim that a future deallocation is scheduled unless an actual supported scheduler has been configured and verified.

---

# 5. VERIFIED BOOTSTRAP FAILURE

The previous independent diagnostic established:

cloud-init status:
error

extended_status:
error - done

Failure:
scripts_user

Recorded error:
Runparts: 1 failures (runcmd) in 1 attempted commands

OpenSSH validation:

/usr/sbin/sshd -t

Exit code:
255

Error:

Missing privilege separation directory: /run/sshd

Additional evidence:

- /run/sshd did not exist.
- The cloud-init first-boot completion marker was absent.
- openssh-server was installed.
- tailscale was installed.
- tailscaled was active and enabled.
- ssh.socket was active and listening.
- ssh.service was inactive and disabled.
- Password-authentication-denial drop-ins existed.
- No real Windows SSH authentication was attempted.

The deployed bootstrap script was:

/usr/local/sbin/polymind-firstboot.sh

Its observed SHA256:

2f567326350a3da849e36a1782e2cb77cb97bdf755ceaff545f11f98ded1075c

The local cloud-init source was:

/tmp/polymind-tailscale-cloud-init.yaml

The earlier comparison established identical embedded script content.

The root-cause hypothesis is:

The first-boot script uses `set -euo pipefail`.

It executes `sshd -t` before the SSH service is enabled or started.

Because `/run/sshd` is missing, validation exits 255.

The script terminates before its systemctl enable commands and completion marker.

This is the investigated hypothesis to verify against actual guest state.

Do not assume that merely creating `/run/sshd` establishes persistent boot correctness.

---

# 6. SECURITY AND MUTATION BOUNDARIES

AUTHORIZED FOR THIS TASK:

- Read-only Azure and guest inspection.
- One narrowly justified SSH runtime/service activation repair.
- Read-only post-repair SSH and systemd verification.
- Bounded independent Run Command revalidation.
- Local cloud-init candidate correction and syntax checks.
- Documentation/report updates.
- Read-only local Windows/SSH prerequisites, if relevant.

NOT AUTHORIZED:

- Recreate or resize the VM.
- Modify public IP or NIC exposure.
- Change the VNet, subnet, NSG, NAT or AKS.
- Open port 22 to the Internet.
- Enable password-based SSH.
- Enable SSH root login.
- Disable SSH public-key authentication.
- Disable host-key verification.
- Enable Tailscale SSH.
- Generate or consume a real Tailscale auth key.
- Enroll the VM in Tailscale.
- Modify tailnet policies.
- Install Docker or launch Compose.
- Format, mount or initialize the data disk.
- Modify financial/governance authorities.
- Perform Entra login or consent changes.
- Invoke a real AI model.
- Retrieve, print or renew secrets.
- Trigger an unapproved reboot.
- Install unrelated packages or Azure services.
- Create snapshots or repair VMs without approval.

Preserve the current private-access architecture.

The VM has no public IP.

The subnet NSG must remain restrictive.

Existing AKS resources and peerings must remain untouched.

---

# 7. WORK PACKAGE A — READ-ONLY PRE-REPAIR DIAGNOSTICS

After the deadline check, inspect the actual guest using Azure Run Command.

Do not assume that SSH must be contacted directly.

Inspect:

1. Current cloud-init status and error.
2. Ubuntu distribution and kernel.
3. openssh-server package state.
4. ssh.service status and enabled state.
5. ssh.socket status and enabled state.
6. Unit dependencies.
7. Unit RuntimeDirectory settings.
8. Relevant service ExecStartPre and ExecStart.
9. Current /run/sshd existence and permissions.
10. Actual SSH listeners.
11. SSH security configuration drop-ins.
12. Current SSH host-key fingerprints.
13. tailscaled state, without enrollment or secret inspection.

Useful guest commands include:

cloud-init status --long
systemctl status ssh.service --no-pager
systemctl status ssh.socket --no-pager
systemctl cat ssh.service
systemctl cat ssh.socket
systemctl show ssh.service -p RuntimeDirectory -p RuntimeDirectoryMode -p ExecStartPre -p ExecStart
systemctl is-enabled ssh.service
systemctl is-enabled ssh.socket
systemctl is-active ssh.service
systemctl is-active ssh.socket
ss -lnt
stat /run/sshd
/usr/sbin/sshd -t

Capture individual exit codes.

Avoid using full journal dumps.

Do not print private keys, passwords, environment variables, authentication tokens or unrelated configuration.

The pre-repair record must show whether the previously observed failure is still present.

If the current state differs from the earlier report, investigate and do not blindly apply the proposed repair.

---

# 8. WORK PACKAGE B — ROOT CAUSE AND REPAIR DECISION

Inspect the actual Ubuntu OpenSSH systemd unit.

Determine:

- Whether ssh.service manages /run/sshd through RuntimeDirectory.
- Whether service activation will prepare the directory correctly.
- Whether socket activation interacts safely with service activation.
- Whether the installed OpenSSH configuration validates after normal runtime-directory creation.
- Whether a persistent service state can be established without weakening authentication.

Preferred repair candidate:

systemctl enable --now ssh.service

However, do NOT execute this merely because it appears in the prompt.

First verify that the actual installed unit and current service/socket configuration support it.

If the expected RuntimeDirectory behavior exists and no conflicting condition is found, perform this single approved service activation using Azure Run Command.

The repair must:

- Leave SSH password authentication disabled.
- Leave keyboard-interactive authentication disabled.
- Keep root SSH login disabled.
- Retain Ed25519 public-key authentication.
- Preserve the existing SSH host keys.
- Avoid broadening Azure ingress.
- Preserve the functioning ssh.socket unless unit behavior requires a separately reviewed change.

Do not run `systemctl disable ssh.socket` as a blind workaround.

Do not replace or regenerate SSH host keys.

Do not modify authorized_keys.

Do not reinstall openssh-server unless a separate technical justification and authorization exists.

If the unit does not manage /run/sshd as expected, STOP before improvising a manual directory or systemd override repair.

Report the exact alternative and its security consequences.

No speculative sequence of repeated repairs is authorized.

---

# 9. WORK PACKAGE C — POST-REPAIR SSH VALIDATION

After the bounded repair, independently verify:

## C1. Runtime integrity

- /run/sshd exists.
- It has expected root ownership and safe permissions.
- SSH unit state is healthy.
- Required socket/service relationship is understood.
- No unexpected failed units were introduced.

## C2. Daemon configuration

Run:

/usr/sbin/sshd -t

Require exit code 0.

Then inspect effective settings using:

/usr/sbin/sshd -T

Where appropriate, use connection-context testing through sshd -T -C to account for Match directives.

Verify the effective values of:

passwordauthentication
kbdinteractiveauthentication
permitrootlogin
pubkeyauthentication
allowtcpforwarding
permitopen
authenticationmethods

Expected security baseline:

passwordauthentication no
kbdinteractiveauthentication no
permitrootlogin no
pubkeyauthentication yes

Local TCP forwarding must remain compatible with the later private PolyMind HTTPS tunnel, without exposing an unrestricted public service.

Do not weaken security merely to obtain a passing daemon test.

If Match directives change effective settings, report those differences explicitly.

## C3. Listeners and exposure

Inspect:

ss -lnt

Determine:

- Whether TCP 22 is listening.
- Whether ssh.service or ssh.socket owns the listener.
- Whether extra listeners appeared.
- Whether application gateway ports remain absent.
- Whether the NIC still has no public IP.

Listening on 0.0.0.0:22 inside the private guest is not automatically public exposure, but it is not by itself proof of secure Tailscale-only connectivity.

Do not change the Azure NSG.

## C4. Identity preservation

Verify non-secret fingerprints of:

- The deployed SSH authorized public key.
- The existing guest SSH host public key.

Compare with the previous report.

The previously recorded guest Ed25519 host-key fingerprint was:

SHA256:tGW/X/urHlViBMqFsJtgeVgrnt2xZxup3Duw/jN6vHg

The operator public-key fingerprint was:

SHA256:ALL3MNDydv6j+2P6l2eojS3Gf0pDz1drYeT12N/RdKQ

Preserve both identities.

Never read or display private key material.

## C5. Persistence

Verify whether ssh.service is enabled appropriately for subsequent boots.

Do not reboot the VM merely to claim persistence.

If persistence has not been tested by an actual approved reboot, report reboot acceptance as GAP/UNKNOWN rather than PASS.

---

# 10. WORK PACKAGE D — CLOUD-INIT FAILURE PRESERVATION

Important distinction:

Restoring SSH service health does not retroactively turn the failed first-boot cloud-init execution into a successful historical run.

Do not:

- Delete cloud-init error evidence.
- Clear cloud-init state.
- Run cloud-init clean.
- Rerun all cloud-init modules.
- Rerun apt installation blindly.
- Append the original completion marker as if first boot succeeded.
- Rewrite the old failure report.

Record two separate facts:

1. ORIGINAL_FIRST_BOOT_CLOUD_INIT: FAIL
2. CURRENT_POST_REPAIR_SSH_READINESS: PASS/GAP/FAIL

If SSH recovery succeeds, document it as an explicitly dated POST-BOOT REPAIR.

The original incident must remain visible for audit and future image/bootstrap improvements.

Do not attempt to change the Azure VM's historical customData to fabricate success.

---

# 11. WORK PACKAGE E — CORRECT FUTURE CLOUD-INIT SOURCE

The original bootstrap source resides outside Git:

/tmp/polymind-tailscale-cloud-init.yaml

Do not overwrite the original automatically.

Prepare a corrected candidate:

/tmp/polymind-tailscale-cloud-init.corrected.yaml

First inspect the exact original contents.

Then propose the smallest safe change that prevents `sshd -t` from running without its required runtime directory.

Possible approaches to evaluate:

A. Explicitly prepare the correct root-owned runtime directory with safe permissions before validation.

B. Use the verified service/unit startup sequence when it reliably prepares the runtime directory.

Select the approach supported by the observed Ubuntu 24.04 systemd/OpenSSH configuration.

Preserve all existing bootstrap protections:

- Ubuntu version verification.
- Official package repositories.
- OpenSSH installation.
- Tailscale installation.
- Password authentication disabled.
- Root login disabled.
- No Tailscale auth key in customData.
- No public application ports.
- No automatic real-model execution.

Do not introduce credentials into cloud-init.

Validate the corrected candidate with:

- YAML parsing.
- Required cloud-init structure.
- Embedded Bash syntax.
- Explicit check of the runtime-directory ordering.
- A reviewed diff against the original.
- Secret scanning.

Record the exact SHA256 of the candidate.

Do not claim live bootstrap PASS from candidate syntax alone.

The original failed first boot remains an observed FAIL.

The corrected candidate is intended for a future explicitly approved provisioning or reprovisioning event, not automatic replacement of the running VM.

Do not execute the corrected cloud-init file on the live VM.

---

# 12. WORK PACKAGE F — RECOVERY PATH REVALIDATION

Azure Run Command previously succeeded before Tailscale enrollment.

After any permitted SSH service repair, verify that the Azure VM Agent remains healthy.

Check:

- Agent Ready state.
- VM provisioning status.
- Run Command handler state.
- No unexpected extension failures.

Perform at most one additional minimal marker-based Run Command test if needed to establish post-repair recovery continuity.

The marker must contain no secrets.

Do not repeatedly install, remove or upgrade Agent extensions.

If recovery regresses after the repair, classify as FAIL and stop further repair operations.

Preserve diagnostic evidence.

Azure Run Command is independent of Tailscale enrollment but still depends on Azure control-plane permissions, VM Agent health and required connectivity.

Do not claim it is a complete disaster-recovery mechanism.

Serial Console and disk repair remain separately deferred.

---

# 13. WORK PACKAGE G — TAILSCALE BOUNDARY

Tailscale package and daemon installation already passed.

Previous guest result:

NeedsLogin

This is expected before deliberate enrollment.

Do not generate a real authentication key.

Do not run `tailscale up` with any real credential.

Do not turn on Tailscale SSH.

Do not modify tailnet ACLs.

Do not advertise routes or exit-node functionality.

Do not change guest DNS policy.

The correct subsequent enrollment design remains:

- Existing operator-owned tailnet.
- tag:polymind-vm.
- Single-use short-lived tagged authentication key.
- Non-ephemeral VM.
- Standard OpenSSH.
- Tailscale SSH disabled.
- No advertised subnet/exit routes.
- --accept-routes=false.
- --accept-dns=false.

A protected-parameter dummy test has passed, but the end-to-end secure REAL credential handoff remains GAP.

Do not mark this GAP closed through a successful SSH daemon repair.

Actual Windows-to-VM SSH cannot be accepted before controlled Tailscale enrollment.

---

# 14. WORK PACKAGE H — COST AND DEPLOYMENT GOVERNANCE

Reconfirm:

- VM remains in the approved subscription.
- No VM public IP was introduced.
- No extra Azure resources were created.
- Both managed disks remain attached.
- No unexpected disk content was modified.
- NAT Gateway and NSG associations are unchanged.
- AKS remains untouched.
- No Tailscale credential was generated.
- No inference provider request occurred.

Do not make storage, application, identity or network changes.

No paid inference is authorized.

The approved USD 30 target is not a hard Azure billing limit.

The VM must be deallocated by the previously stated cutoff.

Never extend the evaluation window automatically.

Document actual power state and whether deallocation occurred.

If the task is interrupted, report that no scheduled background enforcement has been created.

---

# 15. REQUIRED DELIVERABLES

Create:

docs/codex/prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md

docs/codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md

Save this full task prompt in the prompt file.

The report must include:

1. Executive summary.
2. Exact Git baseline.
3. Current Azure VM identity and evaluation time.
4. Prior cloud-init failure evidence.
5. Actual SSH unit/socket/runtime findings.
6. Root-cause assessment.
7. The proposed repair and authorization boundary.
8. Exact live mutation executed, if any.
9. Before-and-after guest observations.
10. SSH service and socket status.
11. sshd -t result.
12. Effective SSH security settings.
13. Authorized-key and host-key fingerprint preservation.
14. Azure VM Agent recovery result.
15. Corrected future cloud-init candidate and diff.
16. Original cloud-init failure preservation.
17. Remaining Tailscale, disk and application deployment GAPs.
18. Cost/deallocation verification.
19. Final PASS/GAP/FAIL acceptance matrix.
20. Git status and changed-file summary.

If useful, append a dated, factual repair addendum to:

docs/operations/phase_19_vm.md

Do not alter historical findings elsewhere merely to obtain a passing status.

---

# 16. VERIFICATION AND PRE-COMMIT REVIEW

Run:

git diff --check
git status --short --branch
git diff --stat
git diff --cached --name-only

Inspect every newly created or changed file.

Verify:

- No credentials or private keys.
- No auth-key payload.
- No raw authorization headers.
- No governance database content.
- No unapproved Azure resource creation.
- No network exposure change.
- No Git history mutation.
- No unrelated application changes.
- No invented test results.
- No overwritten historical verification record.

Application source was not expected to change.

Do not rerun the entire pytest regression suite solely for this SSH repair.

Use targeted configuration checks and actual Azure evidence.

Leave all documentation uncommitted for operator review.

---

# 17. FINAL ACCEPTANCE MATRIX

Use the following machine-readable output:

PHASE_19B_SSH_REPAIR_AUTHORITY: WITHIN_SCOPE/BLOCKED
PHASE_19B_ORIGINAL_CLOUD_INIT: FAIL
PHASE_19B_ROOT_CAUSE_CONFIRMED: YES/NO/WITH_CONDITIONS
PHASE_19B_SSH_RUNTIME_DIRECTORY: PASS/GAP/FAIL
PHASE_19B_SSH_SERVICE_ACTIVATION: PASS/GAP/FAIL/NOT_ATTEMPTED
PHASE_19B_SSHD_SYNTAX: PASS/GAP/FAIL
PHASE_19B_SSH_EFFECTIVE_AUTH_SECURITY: PASS/GAP/FAIL
PHASE_19B_SSH_HOST_KEY_PRESERVED: PASS/GAP/FAIL
PHASE_19B_WINDOWS_PUBLIC_KEY_PRESERVED: PASS/GAP/FAIL
PHASE_19B_SSH_REBOOT_PERSISTENCE: PASS/GAP/UNKNOWN
PHASE_19B_CORRECTED_CLOUD_INIT_SOURCE: PASS/GAP/FAIL
PHASE_19B_AZURE_AGENT_RECOVERY: PASS/GAP/FAIL
PHASE_19B_VM_PRIVATE_NETWORK: PASS/GAP/FAIL
PHASE_19B_TAILSCALE_INSTALLATION: PASS/GAP/FAIL
PHASE_19B_TAILSCALE_ENROLLMENT: GAP
PHASE_19B_REAL_KEY_HANDOFF: GAP
PHASE_19B_WINDOWS_PRIVATE_SSH: GAP
PHASE_19B_DATA_FILESYSTEM: GAP
PHASE_19B_COST_GOVERNANCE: PASS/GAP/FAIL
PHASE_19B_SSH_BOOTSTRAP_REPAIR: PASS/WITH_CONDITIONS/FAIL
PHASE_19B_FULL_INFRASTRUCTURE_READY: NO/WITH_CONDITIONS
PHASE_19B_APPLICATION_DEPLOYMENT_READY: NO
PHASE_19B_LIVE_MODEL_INFERENCE_AUTHORIZED: NO
PHASE_19B_PUBLIC_EXPOSURE_AUTHORIZED: NO
PHASE_19B_AKS_REQUIRED: NO

Adjust any fixed GAP if newer actual evidence proves a different state, but never claim a PASS from intention alone.

For each unresolved item, provide the exact next safe action and evidence required.

---

# 18. STOP CONDITIONS

Immediately stop optional live operations if:

- The VM evaluation deadline is reached.
- The wrong Azure subscription is active.
- The target VM identity differs.
- The VM is deallocated.
- A public IP appears unexpectedly.
- The proposed repair requires weakening SSH authentication.
- The expected systemd runtime behavior is absent.
- The repair requires additional unapproved service changes.
- Azure Run Command recovery becomes unreliable.
- Any operation would modify an existing financial authority.
- A real credential would be exposed.
- The data disk would be modified.
- A change could interrupt existing AKS resources.
- The local working tree would be damaged.

If the evaluation cutoff has been reached while the approved VM remains allocated, prioritize the previously authorized deallocation after exact identity verification.

Document what was completed and what remains.

Do not continue into Tailscale enrollment, Docker Compose deployment, Phase 19C or real-model inference.

---

# 19. EXPECTED FINAL OUTCOME

A successful task establishes:

- The actual OpenSSH root cause.
- A minimal and safe corrective action.
- A healthy SSH runtime/service.
- Successful sshd syntax validation.
- Verified password/root-login restrictions.
- Preserved SSH identity.
- Continued Azure Run Command recovery.
- A corrected future cloud-init candidate.
- An accurate, retained historical bootstrap failure.
- No broadened network exposure.
- No unauthorized additional Azure spending or inference.
- An actionable handoff to the separately governed Tailscale enrollment stage.

A current SSH PASS does not establish full infrastructure or application deployment readiness.

Stop at the bounded repair and revalidation boundary.
