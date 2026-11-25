# Phase 19B — OpenSSH bootstrap repair and revalidation

24 November 2026. **POST-BOOT REPAIR: current SSH readiness PASS; broader bootstrap repair
WITH_CONDITIONS.** One authorized service activation restored the systemd-managed runtime
directory and a healthy enabled daemon. Actual syntax, effective authentication controls,
SSH identities and Azure Agent recovery pass. The original first boot remains FAIL;
reboot and corrected first-boot execution remain untested. Full infrastructure and
application deployment readiness remain NO. Phase 19B is ACTIVE; 19C was not started.

**Fixed cutoff: 2026-11-24T09:26:38.7760141+00:00.** Last live power observation:
`PowerState/running` at 07:41:42.570731 UTC. At the 07:42:02.549891 UTC calculation,
elapsed evaluation time was 06:15:23.773877; remaining time 01:44:36.226123. Deallocation
was not yet due and was not performed. No background monitor or scheduled deallocation
was created. The operator must cover the cutoff and verify actual deallocation.

## Scope and exact Git baseline

The [full task instruction](../prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md)
authorizes read-only inspection, one justified SSH activation, independent revalidation,
a local future cloud-init candidate and documentation. It grants no restart/rebuild,
network alteration, enrollment, storage initialization, application launch or inference.
No explicit credential generation, retrieval, renewal or delivery was performed.

Read AGENTS.md and all eight required baseline documents completely, including their
Integration Gap Resolution and continuation sections. The primary prior live evidence is
the [post-creation report](phase_19b_post_vm_creation_verification.md). Inspected the exact
original YAML and guest SSH units/configuration; searched deployment/scripts/tests for
SSH/bootstrap consumers. No repository application/test interface needed modification.

Initial `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
?? docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/prompts/phase_19b_post_vm_creation_verification.md
?? docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/reports/phase_19b_post_vm_creation_verification.md
```

HEAD was verified as `7bf82dc2da4a9f29561a5f493b690502c0090eb0`. Initial
`git diff --check` exited 0; `git diff --cached --name-only` was empty. Initial tracked
diff: four files, 135 insertions and eight deletions. All eight existing changed/untracked
files were copied and SHA256-recorded before editing under
`/tmp/polymind-phase19b-ssh-repair-20261124/baseline/` and `baseline.json`.

The eight inspected commits:

```text
7bf82dc feat: complete Phase 19B offline Azure deployment foundation
b48dde4 feat: improve local app launchers and document frontend reliability
d7d2ec2 fix(ui): resolve Streamlit document module collision and preserve legacy chat
6aedae3 docs: finalize Phase 18 local engineering closure and deployment handoff
f7d091a feat(documents): implement authenticated local document frontend and verification
f0e420b docs: assess Phase 18 frontend integration and Azure deployment readiness
faaddc2 docs: finalize Phase 17I engineering closure with external verification deferred
ed7dbd5 feat(pilot): implement bounded supervised Phase 17I verification workflow
```

## Azure identity, evaluation gate and infrastructure

First actions read UTC, the active account and exact VM instance view. At 06:50:18 UTC,
05:23:39.223986 had elapsed and 02:36:20.776014 remained. The first VM read encountered
Azure CLI's read-only local session-file restriction; its execution-approved retry
verified the running VM before optional guest work. Active subscription: ECI-Development,
Enabled, `970e5901-0d2d-44de-ade7-92ce4eb61a73`. No account switch occurred. Fresh account,
identity/power, Agent and NIC checks preceded each guest call; repair/final gates queried
the active account without a subscription override. Execution-system approvals did not
expand the user's narrow authorization.

Exact target ID:

```text
/subscriptions/970e5901-0d2d-44de-ade7-92ce4eb61a73/resourceGroups/rg-epolymind/providers/Microsoft.Compute/virtualMachines/vm-epolymind-dev
```

| Property | Independently observed state |
| --- | --- |
| Creation time | `2026-11-24T01:26:38.7760141+00:00`; original eight-hour clock retained |
| Location / SKU | spaincentral / Standard_D2s_v4 |
| Image | Canonical `ubuntu-24_04-lts:server:24.04.202611170` |
| Security | TrustedLaunch; Secure Boot and vTPM true |
| Administrator | polymindadmin; Azure password authentication disabled |
| NIC | vm-epolymind-devVMNic; private 10.50.0.36; no public-IP, load-balancer backend or inbound-NAT reference; IP forwarding false |
| Subnet | snet-polymind-vm, 10.50.0.32/27, defaultOutboundAccess false |
| Associations | nsg-epolymind-vm-dev and nat-epolymind-vm-dev on that subnet; NAT retains pip-epolymind-nat-dev |
| Disks | Two exact 64-GiB StandardSSD_LRS disks Attached to this VM, delete options Detach |
| AKS | epolymind-aks-dev remains Stopped, provisioning Succeeded; only read-only show used |
| RG inventory | Same 19 resource IDs as the prior assessment and before/after this repair |

Disk identities remain:

```text
OS:   vm-epolymind-dev_OsDisk_1_105778dce92045f1904c44685ebca027
LUN0: vm-epolymind-dev_disk2_3895d98e43b64d18be61546938b28df5
```

All seven before/after selected JSON projections are identical: NIC, VNet/subnets/peering,
NSG, NAT, inventory, disks and AKS. NSG/NAT also match retained prior assessment results.
The prior VNet query additionally projected `dns=null`; after accounting for that query
difference, its address space/subnets/peering match. No subscription-wide audit or new
reverse-peering probe is claimed.

The four custom NSG rules remain: priority 100 outbound deny to 10.224.0.0/12; priority
200 outbound Internet TCP 443 allow; priority 4096 all-outbound and all-inbound denies.
No network or AKS mutation occurred. The previous effective-NSG/route probes were not
repeated; associations and rule definitions stayed identical. Broad HTTPS egress remains
separate from an application destination allowlist or inference grant.

## Independent pre-repair findings

Guest diagnostic time: 06:56:12 UTC. Ubuntu `24.04.5 LTS`, kernel `7.0.0-1020-azure`.
Package query exited 0: openssh-server `1:9.6p1-3ubuntu13.20` and tailscale `1.104.7`,
both `install ok installed`.

| Probe | Before repair | Individual exit/result |
| --- | --- | --- |
| cloud-init status --long | error; extended error - done; scripts_user; Runparts: 1 failures (runcmd) in 1 attempted commands | 1 |
| /usr/sbin/sshd -t | Missing privilege separation directory: /run/sshd | 255 |
| stat /run/sshd | Absent | 1 |
| SSH service | inactive/dead, disabled, Result success | properties query 0 |
| SSH socket | active/listening, enabled, Result success | properties query 0 |
| ss -lntpH | TCP 22 IPv4/IPv6 held by systemd PID 1; two loopback DNS listeners | 0 |
| Original completion marker | Zero occurrences | grep 1, expected no match |
| Original failure line | Still present in cloud-init-output.log | grep 0 |
| Failed units | Only cloud-final.service | query 0 |
| Tailscale | tailscaled active/running/enabled; NeedsLogin, no tail IPs/current tailnet | queries 0 |
| LUN0 | /dev/sda, 64G, no filesystem/mount; wipefs --no-act empty | both probes 0 |

Deployed `/usr/local/sbin/polymind-firstboot.sh` SHA256 still equals
`2f567326350a3da849e36a1782e2cb77cb97bdf755ceaff545f11f98ded1075c`, matching the Bash
extracted from the original local YAML. The failure was reproduced independently.
An inactive socket-activated service alone does not establish failed SSH connectivity;
the observed failure is validation and interrupted first boot. No authentication attempt
was made to invent additional failure evidence.

## Installed service/socket and root-cause assessment

All unit queries exited 0. Actual service file: `/usr/lib/systemd/system/ssh.service`,
no service drop-ins. Relevant installed lines/properties:

```text
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755
RuntimeDirectoryPreserve=no
Restart=on-failure
RestartPreventExitStatus=255
WantedBy=multi-user.target
Alias=sshd.service
Requires includes ssh.socket
TriggeredBy=ssh.socket
After includes ssh.socket, network.target, auditd.service
```

The installed socket has Accept=no, FreeBind=yes, separate IPv4/IPv6 port-22 streams,
BindIPv6Only=ipv6-only, Before=ssh.service, Triggers=ssh.service and Install
RequiredBy=ssh.service. Its enabled state establishes the service requirement. Normal
service activation and the existing socket are compatible; disabling the socket is
unnecessary. `/etc/ssh/sshd_not_to_be_run` is absent. Optional `/etc/default/ssh` was
checked without printing variables: `SSHD_OPTIONS_NO_OVERRIDE: PASS`.

All four drop-ins were inspected, including `50-cloudimg-settings.conf`, which the first
specific-file query had omitted. The only active Include is the standard drop-in glob;
no active Match/nested Include appeared. Password denial appears in 50-cloud-init,
60-cloudimg-settings and 99-polymind; the latter also denies keyboard-interactive/root
login and enables public keys. Configuration and unit hashes were recorded before repair.

**ROOT_CAUSE_CONFIRMED: YES.** The identical first-boot script uses `set -euo pipefail`
and runs standalone `sshd -t` before service activation. Missing `/run/sshd` causes
exit 255, terminating the script before enablement and its marker. The verified service
creates its runtime directory before its own ExecStartPre check. Success of both that
precheck and the later independent validator after this single change confirms the cause.
No manual directory, unit override, package reinstall or authentication change was needed.

## Exact bounded live repair

One authorized mutation ran through Action Run Command at 07:37:06–07:37:07 UTC:

```bash
timeout 60s systemctl enable --now ssh.service
```

The timeout bounds the approved `systemctl enable --now ssh.service`. Read-only guards
checked UTC before the 30-minute optional-work boundary, expected inactive/disabled
service and active socket, RuntimeDirectory/mode, absent directory/blocker, both required
Ed25519 fingerprints, original bootstrap hash and seven SSH/unit-file hashes. An exclusive
local attempt record prevented accidental retry after uncertainty. No second repair ran.

Returned evidence:

```text
SSH_REPAIR_PRECONDITIONS_OK
2026-11-24T07:37:06Z
SSH_SERVICE_ACTIVATION_EXIT=0
2026-11-24T07:37:07Z
```

CLI exit 0; Azure ProvisioningState/succeeded. Guest stderr recorded normal SysV
synchronization and creation of `/etc/systemd/system/sshd.service` and
`/etc/systemd/system/multi-user.target.wants/ssh.service` links to the installed unit.
No socket disable, key replacement, authorized-key edit, cloud-init/package rerun, firewall
change or reboot occurred.

## Independent post-repair acceptance

Separate read-only verification guest time: 07:41:15 UTC.

| Probe | After repair | Individual exit/result |
| --- | --- | --- |
| Runtime directory | /run/sshd root:root 0755 directory | stat 0 |
| ssh.service | active/running, enabled, Result success; PID 5122; ExecMainStatus 0; NRestarts 0 | show/is-active/is-enabled all 0 |
| ExecStartPre | /usr/sbin/sshd -t completed 07:37:07, status 0 | observed unit result |
| ssh.socket | active/running, enabled, Result success; still triggers ssh.service | show/is-active/is-enabled all 0 |
| /usr/sbin/sshd -t | No errors | 0 |
| /usr/sbin/sshd -T | Successful global effective dump | 0 |
| Context effective dumps | Administrator and root contexts below | each 0 |
| Failed units | Only original cloud-final.service | query 0; no new failure |
| Tailscale | tailscaled active/running/enabled; NeedsLogin, no IP/tailnet | queries 0 |
| Data / app mount | Same blank unmounted LUN0; /srv/polymind still absent | probes 0 |

Effective settings, identical globally and in both contexts:

```text
passwordauthentication no
kbdinteractiveauthentication no
permitrootlogin no
pubkeyauthentication yes
allowtcpforwarding yes
permitopen any
authenticationmethods any
gatewayports no
disableforwarding no
```

PubkeyAcceptedAlgorithms includes ssh-ed25519; authorized-key paths remain
`.ssh/authorized_keys .ssh/authorized_keys2`. Tested `sshd -T -C` contexts:

```text
user=polymindadmin,host=susanta-hp-pro,addr=100.108.249.65,laddr=10.50.0.36,lport=22
user=root,host=susanta-hp-pro,addr=100.108.249.65,laddr=10.50.0.36,lport=22
```

These are configuration-parser contexts using the previously recorded laptop address,
not real connections/enrollment evidence. No Match differences appeared. AuthenticationMethods
any does not re-enable explicitly disabled password/keyboard-interactive methods.
Forwarding remains compatible with a future authenticated local tunnel to 127.0.0.1:9443;
PermitOpen any is general forwarding permission, not a destination restriction to 9443.
No forwarding policy was broadened or tunnel started. Later client acceptance must bind
local forwarding to loopback and retain TLS/host verification.

`ss -lntpH` still shows exactly four TCP listeners: loopback DNS 127.0.0.53:53 and
127.0.0.54:53; SSH 0.0.0.0:22 and [::]:22. SSH sockets are now shared by sshd PID 5122
and systemd PID 1, consistent with inherited socket activation. No gateway 9443, fixture
9444, HTTP/HTTPS, API/UI, Redis or Chroma listener appeared. An all-interface private
guest listener is not proof of Tailscale-only connectivity; no VM public IP exists and
Azure ingress remains restrictive.

Boot enablement PASS is supported by links and is-enabled. **Reboot persistence UNKNOWN:**
no approved reboot occurred, so boot-time directory recreation/startup has not been tested.

## SSH identities preserved

All public fingerprint commands exited 0 before and after repair:

| Identity | Identical fingerprint |
| --- | --- |
| Guest Ed25519 host | `SHA256:tGW/X/urHlViBMqFsJtgeVgrnt2xZxup3Duw/jN6vHg` |
| Deployed operator Ed25519 key | `SHA256:ALL3MNDydv6j+2P6l2eojS3Gf0pDz1drYeT12N/RdKQ` |
| Guest ECDSA host | `SHA256:bShUvibED3FZetjFWiOa2ZFvl406WCgmegpUjjG+JMY` |
| Guest RSA host | `SHA256:p2LFRMhm6HU5xBIOllFsODmkxFRAfwdQkfckDC49mus` |

The two required Ed25519 identities match the previous report. Windows public-key
preservation PASS means the deployed key still matches the independently recorded Windows
.pub fingerprint; this task did not reread the Windows key file or attempt Windows SSH.
No private key was read/displayed or host/authorized key replaced.

## Original first-boot failure preserved

```text
ORIGINAL_FIRST_BOOT_CLOUD_INIT: FAIL
CURRENT_POST_REPAIR_SSH_READINESS: PASS
```

After repair, cloud-init status still exits 1 with the same scripts_user error; marker
count remains zero and cloud-final.service remains failed. The live bootstrap script and
original local YAML remain unchanged. All ten pre/post hashes match: SSH main config,
four drop-ins, two installed units, and the three incident records below.

| Incident record | Unchanged SHA256 |
| --- | --- |
| /var/lib/cloud/data/status.json | `35bbd07fb9da2759e1eddaa3c0a234ebeb97d9a7f0cf7abc6be9bd6e966890c2` |
| /var/lib/cloud/data/result.json | `8c2d95ced48431b87e48fa705592c35a48fe7cc0b1617d28bc6623527e0fd84b` |
| /var/log/cloud-init-output.log | `c710420acc937b252661602b937d581165164c3f4356696322a9bc8e941c5bd9` |

No clean, state reset, all-module rerun, apt rerun, marker fabrication or historical
customData edit occurred. The previous verification report remains byte-identical to its
working-tree baseline. Current repair evidence is separate from historical bootstrap failure.

## Corrected future cloud-init candidate

Preserved `/tmp/polymind-tailscale-cloud-init.yaml`; created separately
`/tmp/polymind-tailscale-cloud-init.corrected.yaml`. Selected approach B: let the verified
service manage runtime creation and its mandatory ExecStartPre validation, then retain
standalone validation. Approach A would duplicate directory preparation outside the unit
lifecycle and was unnecessary. Complete reviewed change:

```diff
--- /tmp/polymind-tailscale-cloud-init.yaml
+++ /tmp/polymind-tailscale-cloud-init.corrected.yaml
@@ -49,8 +49,9 @@
       PubkeyAuthentication yes
       EOF

-      sshd -t
-      systemctl enable --now ssh
+      # systemd creates /run/sshd before its own ExecStartPre syntax check.
+      systemctl enable --now ssh.service
+      /usr/sbin/sshd -t
       systemctl enable --now tailscaled

       echo "POLYMIND_BOOTSTRAP_COMPLETE"
```

| Artifact | SHA256 |
| --- | --- |
| Original YAML | `4bef517b0a47d04935ce601a448fe127c0c96cd0daa733e3bca6df58f7b973df` |
| Corrected YAML | `d93b84f442d3cf3e2a9516810f13da0b7c22b7a05753b2532b8102086a0fa125` |
| Corrected embedded Bash | `7bb561fb422daea0f8d7898347dc6418971c0c479fc33216990f4fc65561ccb5` |

Executed checks passed: existing PyYAML safe_load; cloud-config header; exact required
top-level structure/runcmd; single root:root mode-0700 script; ssh_pwauth false and
disable_root true; embedded bash -n exit 0; service-before-standalone-test ordering;
exact equality outside the intended edit; zero secret-payload pattern findings. No
dependency was installed. Ubuntu version verification, official HTTPS repositories,
OpenSSH/Tailscale installation, auth restrictions and unenrolled behavior are preserved.
No credential, app port or inference was added.

Candidate PASS means local syntax/structure/order and observed unit-contract review.
It is not live bootstrap acceptance. The corrected YAML was not uploaded or executed on
the VM. A future approved provisioning event must reverify its image/unit and record
actual first-boot completion independently. These artifacts are in /tmp; archive the
reviewed non-secret candidate and digest before temporary-file cleanup.

## Azure Agent and recovery continuity

The independent post-repair verification returned `AZURE_RUN_COMMAND_RECOVERY_OK`,
Azure ProvisioningState/succeeded, CLI exit 0, and empty outer/guest stderr. This combines
recovery and read-only acceptance in one invocation; no extra marker-only call was needed.
Individual subordinate exits, including the preserved cloud-init failure, were recorded.
Action Run Command did not return a separate numeric guest exit field; the repair wrapper
explicitly printed its activation exit code.

Final instance view: provisioning Succeeded; Agent 2.16.0.2 Ready, Guest Agent is running;
existing Microsoft.CPlat.Core.RunCommandLinux 1.0.12 handler Ready / Plugin enabled;
extensions empty, no unexpected extension failure. No handler install/removal/upgrade was
requested. Recovery remains independent of Tailscale enrollment but depends on Azure
permissions/control plane, Agent and connectivity. Serial Console/disk repair remain
separately deferred, and complete disaster recovery is not established.

## Cost, deallocation and remaining actions

No deallocation, restart or window extension occurred. Repair and revalidation completed
well before the optional-work boundary. The USD 30 target is not a billing cap. No resource
or paid inference was added. Actual accrued billing, NAT data/disk operations, billing lag
and residual reconciliation remain GAP; no Cost Management query or price refresh was
performed. The previous report's retail estimates remain dated estimates. Retained disks
and NAT/PIP can continue billing after compute deallocation.

Operator cutoff action after active-account/exact-VM verification:

```bash
az account show --query '{id:id,name:name}' -o json
az vm show --subscription 970e5901-0d2d-44de-ade7-92ce4eb61a73 \
  -g rg-epolymind -n vm-epolymind-dev --query '{id:id,timeCreated:timeCreated}' -o json
az vm deallocate --subscription 970e5901-0d2d-44de-ade7-92ce4eb61a73 \
  --resource-group rg-epolymind --name vm-epolymind-dev
az vm get-instance-view --subscription 970e5901-0d2d-44de-ade7-92ce4eb61a73 \
  -g rg-epolymind -n vm-epolymind-dev --query 'instanceView.statuses' -o json
```

Require actual PowerState/deallocated by **09:26:38.7760141 UTC today**, not guest shutdown
or PowerState/stopped. No scheduler or monitoring survives this execution. A later
allocation window needs new authorization. Coordinate exact NAT/PIP teardown after required
access/recovery ends, using the prior plan; this task changed neither resource. Retain both
disks pending review, with the existing up-to-30-day review by 24 December 2026; no automatic
disk deletion is implied.

| Unresolved item | Next safe action and closure evidence |
| --- | --- |
| Original cloud-init FAIL | Preserve this incident; future corrected first-boot success must be recorded as a new event, never retroactively change this verdict. |
| Reboot persistence UNKNOWN | Separately authorize reboot/evaluation time; require boot-ID change, runtime/service/socket startup, syntax/security/identity continuity and Agent recovery. Do not restart a deallocated VM without new authorization. |
| Corrected candidate execution untested | Archive digest/source; recheck future image/unit; require actual new cloud-init completion/error/marker evidence under separate provisioning authorization. |
| Real-key handoff GAP | Review and dummy-test full protected delivery, safe consumption and cleanup with no real secret in argv/history/source/logs/output before generating any credential. Prior dummy delivery alone is insufficient. |
| Tailscale enrollment GAP | After explicit approval and safe handoff, use operator-owned tailnet, tag:polymind-vm, short-lived single-use tagged key, non-ephemeral VM, standard OpenSSH, Tailscale SSH disabled, no subnet/exit routes, accept-routes false and accept-dns false; verify actual identity/tag/online/preferences. |
| Tailnet policy / Windows SSH GAP | Retain operator policy tests for laptop allow, phone deny and VM-to-personal deny; after enrollment prove TCP 22 and interactive dedicated-key login with the recorded host fingerprint. Keep passphrase local and host verification enabled. |
| Data filesystem GAP | Obtain exact-disk/provenance authorization; reidentify LUN0/no required state; separately prepare and verify local filesystem UUID, durable mount, owners, mount-failure refusal and deliberate authority initialization/migration. |
| Infrastructure/application readiness NO | Resolve private access, prior disk-export/guest-firewall review, storage, immutable transfer identities, private TLS/origin/Entra/config/trust, egress, approved lifecycle, capacity and recovery. Separately authorize the existing five-service deployment and validate real private browser/API identity and zero-paid workflows. |
| Serial Console / disk repair deferred | Separately review secure console prerequisites and isolated disk-recovery custody; obtain authorization before settings, snapshots, detach or repair environments. No SSH authentication weakening. |
| Cost governance GAP | Cover cutoff, retain actual deallocated-state evidence, coordinate NAT/PIP disposition, review disks and reconcile billing after ingestion lag. |
| Inference/public exposure unauthorized | Preserve separate A3/A4/A5 provider/source/finance/fresh signed execution gates and later public-exposure authority; SSH or infrastructure readiness grants neither. |

No Tailscale credential/enrollment/policy change, data disk write/mount, application deployment,
governance-authority access, Entra administration or provider request occurred. Read-only
signature probes do not prove forensic absence of all data; no data disk writer was authorized.

## Evidence record and targeted validation

Exact argv arrays, timestamps, CLI JSON, scripts and decoded guest outputs remain under
`/tmp/polymind-phase19b-ssh-repair-20261124/`. This report contains durable sanitized
findings; the temporary directory is not a backup or credential store. Read-only scripts
gzip/base64-encoded selected non-secret output to avoid Run Command truncation; complete
delimiters decoded successfully. No full journal, environment dump, private key, AuthURL,
credential or governance database was captured. Each probe prints its individual exit;
outer transport success was not substituted for subordinate success.

The five guest calls used this exact shape, substituting the listed script:

```bash
az vm run-command invoke -g rg-epolymind -n vm-epolymind-dev \
  --command-id RunShellScript \
  --scripts @/tmp/polymind-phase19b-ssh-repair-20261124/diagnose.sh \
  --subscription 970e5901-0d2d-44de-ade7-92ce4eb61a73 -o json --only-show-errors
```

| Script | CLI start–completion UTC | CLI exit |
| --- | --- | --- |
| diagnose.sh | 06:56:08.273212–06:56:41.069587 | 0 |
| units.sh | 07:00:45.370387–07:01:18.601267 | 0 |
| prerequisites.sh | 07:21:38.600612–07:22:11.900038 | 0 |
| repair.sh | 07:37:00.975712–07:37:34.224612 | 0 |
| verify.sh | 07:41:07.976014–07:41:40.695410 | 0 |

Three read-only pre-repair calls, one repair, one independent post-repair call containing
the recovery marker; no managed Run Command child was created. Read-only control-plane
commands were account show, vm show/get-instance-view, network nic/vnet/nsg/nat gateway
show, resource list, disk list and aks show, scoped above. Timeouts were 60 seconds for
control reads, 240 seconds for guest transports and 60 seconds for activation. No repair
retry occurred. The initial CLI sandbox failure was resolved through execution approval;
no credential copying, login or security relaxation was used.

Executed local acceptance assertions exited 0: three effective contexts/settings,
16 successful post-repair probe sections, four preserved public fingerprints, ten
preserved guest hashes, seven identical control-plane projections, original error/absent
marker and no new failed unit. YAML/Bash/order/diff/secret-pattern candidate checks also
exited 0. No application/dependency/image/Compose change exists, so pytest, compileall and
Docker builds were not rerun for this targeted infrastructure repair.

## Self-review and separate pre-commit review

Self-review inspected the source-candidate diff, installed lifecycle/socket inheritance,
runtime ownership, effective auth/forwarding, timeout/error paths, identities, incident
preservation, recovery and deadline ownership. It added the fourth-drop-in/service-options
inspection before repair, resolved the VNet query projection difference and separated boot
enablement from untested reboot acceptance. No architecture/API/provider boundary changed.

Separate pre-commit review covers the prompt/report and guide append for private keys,
auth-key/token/header payloads, generated authorities/artifacts, temporary/debug material,
unrelated dependencies/changes, whitespace and local links. Public resource IDs,
fingerprints/hashes and requested /tmp paths are intentional evidence; no machine-specific
path entered application code. No old report was rewritten. Nothing was staged, committed
or pushed. Final executed local-check results and Git inventory are appended below.

## Final local review and Git inventory

Executed documentation/preservation review exited 0: three files scanned, six local
Markdown links checked, zero broken links, zero secret-payload pattern findings and no
trailing whitespace. All eight pre-existing changed/untracked files are preserved: seven
byte-identical and the VM guide retaining its complete baseline as an unchanged prefix.
Original cloud-init YAML and HEAD are unchanged; the index is empty. These bounded pattern
checks complement manual review and are not a comprehensive credential-leak certification.
`git diff --check` exited 0. Local review clock observation was 07:51:00 UTC, still before
the fixed cutoff; the last actual Azure power observation remains the one stated above.

Final `git status --short --branch`:

```text
## master...origin/master
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
?? docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/prompts/phase_19b_post_vm_creation_verification.md
?? docs/codex/prompts/phase_19b_ssh_bootstrap_repair_and_revalidation.md
?? docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/reports/phase_19b_post_vm_creation_verification.md
?? docs/codex/reports/phase_19b_ssh_bootstrap_repair_and_revalidation.md
```

`git diff --stat`: four tracked files changed, **158 insertions(+), eight deletions(-)**.
This includes all prior tracked changes and this task's **23 appended VM-guide lines**;
it excludes untracked files. This task creates only the full repair prompt and this report
in Git's working tree, plus the guide append. Scripts, candidate and selected evidence
remain outside Git in /tmp. `git diff --cached --name-only` is empty. No application,
dependency, governance authority, Git history or Git remote-state change occurred.
**No commit or push occurred.**

## Machine-readable acceptance matrix

```text
PHASE_19B_SSH_REPAIR_AUTHORITY: WITHIN_SCOPE
PHASE_19B_ORIGINAL_CLOUD_INIT: FAIL
PHASE_19B_ROOT_CAUSE_CONFIRMED: YES
PHASE_19B_SSH_RUNTIME_DIRECTORY: PASS
PHASE_19B_SSH_SERVICE_ACTIVATION: PASS
PHASE_19B_SSHD_SYNTAX: PASS
PHASE_19B_SSH_EFFECTIVE_AUTH_SECURITY: PASS
PHASE_19B_SSH_HOST_KEY_PRESERVED: PASS
PHASE_19B_WINDOWS_PUBLIC_KEY_PRESERVED: PASS
PHASE_19B_SSH_REBOOT_PERSISTENCE: UNKNOWN
PHASE_19B_CORRECTED_CLOUD_INIT_SOURCE: PASS
PHASE_19B_AZURE_AGENT_RECOVERY: PASS
PHASE_19B_VM_PRIVATE_NETWORK: PASS
PHASE_19B_TAILSCALE_INSTALLATION: PASS
PHASE_19B_TAILSCALE_ENROLLMENT: GAP
PHASE_19B_REAL_KEY_HANDOFF: GAP
PHASE_19B_WINDOWS_PRIVATE_SSH: GAP
PHASE_19B_DATA_FILESYSTEM: GAP
PHASE_19B_COST_GOVERNANCE: GAP
PHASE_19B_SSH_BOOTSTRAP_REPAIR: WITH_CONDITIONS
PHASE_19B_FULL_INFRASTRUCTURE_READY: NO
PHASE_19B_APPLICATION_DEPLOYMENT_READY: NO
PHASE_19B_LIVE_MODEL_INFERENCE_AUTHORIZED: NO
PHASE_19B_PUBLIC_EXPOSURE_AUTHORIZED: NO
PHASE_19B_AKS_REQUIRED: NO
```

WITH_CONDITIONS refers to broader bootstrap acceptance: current post-boot SSH passes,
original first boot remains failed and future/reboot acceptance is untested. Corrected
source PASS is local candidate validation only. Stop here; enrollment, storage preparation,
application launch and subsequent phases were not begun.
