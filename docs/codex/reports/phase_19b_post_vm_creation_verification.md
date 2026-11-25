# Phase 19B — Private Azure VM post-provisioning verification

24 November 2026. **Assessment executed; infrastructure and application deployment readiness
are NO.** Provisioning, Trusted Launch, private Azure networking, disk attachment, Azure
Run Command recovery and Tailscale installation are verified. Actual first boot failed.
Private SSH, Tailscale enrollment, secure real-key delivery and persistent filesystem
preparation remain incomplete. Phase 19B remains ACTIVE; Phase 19C is not started or complete.

**Evaluation cutoff: 2026-11-24 09:26:38.7760141 UTC.** The VM remained running at the final
control-plane observation around 01:52:46 UTC. At 01:53:44 UTC, 27 minutes 5.6 seconds had
elapsed and 7 hours 32 minutes 54.4 seconds remained. No future monitor or deallocation
job was scheduled. The operator must arrange deallocation by that cutoff and verify it.
This report does not extend or restart the approved eight-hour clock.

## Scope, authorization and evidence provenance

The [current task prompt](../prompts/phase_19b_post_vm_creation_verification.md) supersedes
the earlier unapproved infrastructure proposal for this bounded assessment: the operator
has already provisioned the named Spain Central VM and approved its eight-hour evaluation,
USD 30 incremental target and eventual deallocation. That grants neither real-model
execution nor broader identity, firewall, storage initialization or application-launch
permission. The historical 19A/19B reports and the uncommitted 21 November continuation
remain unchanged. Their older West Europe quota/candidate and undeployed-state findings
are retained as dated evidence, not applied over the operator's later decisions.

All live Azure calls used the existing WSL Azure CLI session. No login, account switch,
explicit credential retrieval/renewal, key inspection, model call, approval signing,
governance database access, AKS mutation, network change or application launch occurred.
The only cloud execution was one marker recovery probe, two read-only guest diagnostic
scripts, and one non-secret protected-parameter managed Run Command. Its temporary child
resource was deleted after recording success; the VM, disks and networks were preserved.
Run Command's necessary guest handler was installed through that supported mechanism;
no Azure CLI extension was installed. No first-boot repair was performed.

The local first-boot YAML, current deployment/configuration/storage/backup/unit files,
existing Phase 19 tests, README, AGENTS.md, architecture, plan, 19A/19B reports and local
continuation prompt/report were inspected. Related production-security and evaluation
governance contracts were consulted. This is an infrastructure assessment; historical
test results were not promoted into new live acceptance evidence.

Selected control-plane JSON and temporary diagnostic scripts are outside Git under
`/tmp/polymind-phase19b-postvm/`. The durable evidence is the sanitized observations and
exact command record in this report. This temporary directory is not a credential store
or durable backup. A tool-server restart occurred after the initial inventory; saved
state was checked before proceeding. No successful mutation was repeated after restart.

## Actual Git baseline

Branch: `master...origin/master`. HEAD:
`7bf82dc2da4a9f29561a5f493b690502c0090eb0`.
The initial `git diff --check` exited 0 and the staged-file list was empty.

```text
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
?? docs/codex/prompts/phase_19b_live_deployment_readiness_continuation.md
?? docs/codex/reports/phase_19b_live_deployment_readiness_continuation.md
```

Initial tracked diff: **4 files changed, 107 insertions(+), 8 deletions(-)**; this excludes
the two pre-existing untracked files. A SHA256 baseline of those six complete working-tree
files was recorded before editing. This task adds the prompt/report and appends only a
dated finding to the VM guide. It does not rewrite those existing changes.

The eight inspected commits were:

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

## Operator-supplied historical baseline versus current observations

The operator supplied successful creation of `vm-epolymind-dev`, private IPv4 `10.50.0.36`,
no public IP/FQDN, Standard_D2s_v4, Ubuntu 24.04 x64/Gen2, two 64-GiB Standard SSD LRS
disks, Trusted Launch intent, Detach disk policies and Delete NIC policy. They also supplied
the pre-existing VNet/subnet/NSG/NAT design, stopped AKS, Windows Tailscale/OpenSSH/key
prerequisites, restricted tailnet policy and local cloud-init syntax checks.

The control-plane findings below independently match that requested VM/network/storage
baseline. The guest disproves successful bootstrap. The reported tailnet policy and its
tests remain operator-supplied evidence: no admin API credential was requested or used.
No claim of live SSH authentication follows from matching public keys.

## Azure identity, VM and security

Azure CLI is **2.93.0**. `az account show` confirmed Enabled **ECI-Development**, subscription
`970e5901-0d2d-44de-ade7-92ce4eb61a73`, tenant `afabeaf8-0fea-42c9-afb4-7e5c07eff3f3`.
Account email and authentication material are omitted. The exact verified VM ID is:

```text
/subscriptions/970e5901-0d2d-44de-ade7-92ce4eb61a73/resourceGroups/rg-epolymind/providers/Microsoft.Compute/virtualMachines/vm-epolymind-dev
```

| Requirement | Actual observation | Decision |
|---|---|---|
| Resource/region/provisioning | Exact VM above; `spaincentral`; provisioning Succeeded; running | PASS |
| Creation timestamp | `2026-11-24T01:26:38.7760141+00:00` from VM `timeCreated` | PASS |
| Hardware | `hardwareProfile.vmSize=Standard_D2s_v4` | PASS |
| Size meaning | 2 vCPU / 8 GiB from current official Dsv4 specification; no guest workload capacity test | PASS for SKU specification only |
| Image | Canonical / `ubuntu-24_04-lts` / `server` / exact version `24.04.202611170` | PASS |
| Architecture/OS | Image x64, V2, Linux; guest `x86_64`, `Ubuntu 24.04.5 LTS` | PASS |
| Security type | `TrustedLaunch` | PASS |
| UEFI | `secureBootEnabled=true`, `vTpmEnabled=true` | PASS |
| Admin/key | `polymindadmin`; Ed25519 public key at `/home/polymindadmin/.ssh/authorized_keys` | PASS for configuration |
| Azure password setting | `disablePasswordAuthentication=true`; VM Agent provisioned | PASS for control-plane setting |
| Effective SSH restrictions | `sshd -T` exits 255 because `/run/sshd` is absent | GAP |
| Boot diagnostics | `diagnosticsProfile=null`; boot diagnostics not established | GAP for Serial Console fallback |

The [official Dsv4 specification](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dsv4-series)
confirms the SKU's CPU/memory allocation and absence of local temporary storage. The bounded
`az vm list-skus` discovery timed out at 60 seconds; its capability result is not claimed.
Provisioned SKU identity is independently present in VM metadata. No capacity, memory-pressure,
IOPS, sustained workload, Docker or reboot acceptance was performed.

The public-key fingerprint matched across Azure configuration, the actual guest authorized
keys and Windows `.pub` file:

```text
SHA256:ALL3MNDydv6j+2P6l2eojS3Gf0pDz1drYeT12N/RdKQ
```

The guest host Ed25519 fingerprint, obtained independently through Run Command, is:

```text
SHA256:tGW/X/urHlViBMqFsJtgeVgrnt2xZxup3Duw/jN6vHg
```

Use that independently verified host identity during a later Windows SSH acceptance.
The Windows private key was checked for existence only. It was never opened, copied,
uploaded, permission-modified or passed to a noninteractive authentication probe.

## Private networking, egress and AKS isolation

| Item | Verified state |
|---|---|
| VM NIC | `vm-epolymind-devVMNic`, attached only to the approved VM; delete option Delete; IP forwarding false |
| NIC IP configurations | One primary IPv4 configuration, dynamic private IP `10.50.0.36`; no public-IP reference, load-balancer backend or inbound-NAT attachment |
| VM IP inventory | `privateIpAddresses=["10.50.0.36"]`, `publicIpAddresses=[]` |
| VNet | `vnet-epolymind-private-dev`, `10.50.0.0/24` |
| VM subnet | `snet-polymind-vm`, `10.50.0.32/27`, `defaultOutboundAccess=false` |
| NSG | `nsg-epolymind-vm-dev` associated with the subnet; no separate NIC NSG |
| NAT | `nat-epolymind-vm-dev`, Standard, Succeeded, attached to this subnet, idle timeout 4 minutes |
| NAT public IP | `pip-epolymind-nat-dev`, Standard/Regional/static, `68.221.228.209`; NAT association only, no NIC IP configuration |
| Other NIC | Historical Redis private-endpoint NIC at `10.50.0.4`; not adopted by the VM application |
| Effective routes | Local `10.50.0.0/24`; peered `10.224.0.0/12`; default Internet route; existing `10.50.0.4/32` InterfaceEndpoint route |
| AKS | `epolymind-aks-dev`, power Stopped, provisioning Succeeded |
| AKS VNet | `aks-vnet-36185111` in `MC_rg-epolymind_epolymind-aks-dev_spaincentral`, `10.224.0.0/12` |
| Reciprocal peering | Both directions Connected; VNet access true; forwarding false; remote gateways false; unchanged |

Actual NIC effective-security rules confirm these four custom rules, before Azure defaults:

| Priority | Direction | Rule | Protocol/destination | Result |
|---:|---|---|---|---|
| 100 | Outbound | DenyAKSOutbound | Any, `10.224.0.0/12`, all ports | Deny |
| 200 | Outbound | AllowOutboundHTTPS | TCP, Internet, 443 | Allow |
| 4096 | Outbound | DenyAllOutbound | Any destination/port | Deny |
| 4096 | Inbound | DenyAllInbound | Any source/destination/port | Deny |

Azure's default AllowVnet/AllowLoadBalancer/AllowInternet rules at priorities 65000/65001
do not override the earlier custom denies. Effective rules also include the platform's
default IPv6 outbound deny. The peered AKS route exists, but the priority-100 deny blocks
VM-initiated traffic into that CIDR; inbound traffic is denied separately. No AKS connection,
port scan or mutation was attempted. This establishes the Azure filtering boundary, not a
claim of guest-tested reachability to every managed endpoint or prevention of access to
all public Azure management endpoints. Internet TCP 443 is broad and includes potential
provider destinations: this NSG is not an application destination allowlist or inference grant.

The resource-group inventory contains the expected new NSG/NAT/PIP/NIC/VM/two disks and
the historical resources. No new load balancer, Bastion, second NAT/PIP/VNet or other
unexpected recent managed service was observed **in `rg-epolymind`**. This is not a
subscription-wide audit or a claim that historical services have no charges.

Guest observations establish working DNS via `168.63.129.16` and HTTPS HEAD responses:
Ubuntu Noble Release **200**, official Tailscale Noble key **200**, and Tailscale control
endpoint **302**, all with normal TLS validation. Tailscale packages were actually installed.
These are prerequisite reachability checks, not tailnet enrollment or DERP session proof.
UDP/direct peer transport was not allowed or claimed. The saved tailnet ACL and actual relay
path remain independent acceptance requirements; [Tailscale firewall documentation](https://tailscale.com/docs/reference/faq/firewall-ports)
explains why HTTPS relay connectivity can matter when direct connections are unavailable.

Azure DNS and Agent communication are platform exceptions that must be distinguished from
ordinary Internet egress. Microsoft's [168.63.129.16 documentation](https://learn.microsoft.com/en-us/azure/virtual-network/what-is-ip-address-168-63-129-16)
describes Agent TCP 80/32526 communication outside ordinary NSG filtering and special DNS
behavior unless AzurePlatformDNS is explicitly targeted. No such DNS deny is present.
The actual Agent/recovery and HTTPS successes supply stronger evidence than assumptions
from those exceptions alone. Guest `NTPSynchronized=yes` was observed; the exact ongoing
time source was not identified. External UDP NTP is not granted by the current NSG.
The [Azure Linux time guidance](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync)
describes host/PTP alternatives; no time configuration was changed.

Guest UFW is inactive. An iptables ruleset was present (25 output lines), but a count does
not establish a complete guest firewall policy. No firewall was relaxed. Review actual
post-enrollment Tailscale/host rules before application acceptance; retain the subnet deny.

## Managed disks and persistence

| Role | Actual disk resource name | Azure state |
|---|---|---|
| OS | `vm-epolymind-dev_OsDisk_1_105778dce92045f1904c44685ebca027` | 64 GiB, StandardSSD_LRS, Attached to approved VM, Linux/V2, caching ReadWrite, delete Detach |
| Data, LUN 0 | `vm-epolymind-dev_disk2_3895d98e43b64d18be61546938b28df5` | 64 GiB, StandardSSD_LRS, Attached to approved VM, create Empty, caching None, delete Detach |

Both managed disks report platform-key encryption at rest and creation time
`2026-11-24T01:26:40.6153746+00:00`. Their distinct full IDs are the VM's disk references
under the same subscription/RG and `Microsoft.Compute/disks/` plus the names above.
The OS disk's guest device was `/dev/sdb`, with ext4 `/` on sdb1, EFI on sdb15 and ext4
`/boot` on sdb16. LUN 0 resolves to `/dev/sda`, **68,719,476,736 bytes**, no partitions,
no detected filesystem and no mount. `wipefs --no-act` returned exit 0 with empty output,
supporting absence of recognized signatures, not a forensic guarantee of zero bytes.
`/srv/polymind` does not exist and is not mounted. No authorities exist under that absent
path; other possible guest locations were not recursively searched for sensitive data.

**Disk attachment PASS; persistent filesystem readiness GAP.** No formatting, partitioning,
fstab edit, directory creation/chown or database initialization occurred. Before deployment,
obtain explicit initialization approval, reidentify this exact managed disk and LUN, confirm
it contains no required state, choose whole-disk ext4 versus an approved partition layout,
record its filesystem UUID and mount it durably at `/srv/polymind`. Verify actual filesystem,
mount failure behavior and numeric directory owners before installing the existing mount-aware
unit. Prepare operator/private/objects, Redis and Chroma directories as documented. Decide
new isolated authority versus approved migration explicitly; never reset historical authority.
Preserve all seven SQLite databases, objects, Redis AOF and Chroma together in future recovery.

Both disks currently report `networkAccessPolicy=AllowAll`, `publicNetworkAccess=Enabled`.
These describe the authenticated import/export/SAS capability, not a VM public IP or
anonymous disk access. No SAS was requested or inspected. The [managed-disk restriction guidance](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-restrict-import-export-overview)
and [disk API property definitions](https://learn.microsoft.com/en-us/rest/api/compute/disks/create-or-update?view=rest-compute-2026-04-01)
support a separate custodian review before storing authorities. Select the required export
policy and recovery process; any disk-policy mutation requires a separate approved action.
No new private endpoint or Disk Access service is proposed automatically.

## Azure VM Agent and independent recovery

Initial Agent instance view: **2.16.0.2**, Ready, `Guest Agent is running`, no extension
handlers or errors. Guest package inventory separately reports
`walinuxagent 2.15.0.1-0ubuntu1~24.04.1`; package and active Agent versions are different
observations, not silently reconciled into one version. Guest walinuxagent is active/enabled.

The single live recovery probe was:

```bash
az vm run-command invoke --resource-group rg-epolymind --name vm-epolymind-dev \
  --command-id RunShellScript --scripts 'printf "AZURE_RUN_COMMAND_RECOVERY_OK\n"' -o json
```

Sanitized exact result: CLI **exit 0**;
`value[0].code=ProvisioningState/succeeded`, `displayStatus=Provisioning succeeded`,
`level=Info`, message:

```text
Enable succeeded:
[stdout]
AZURE_RUN_COMMAND_RECOVERY_OK

[stderr]
```

Action Run Command did not expose a separate numeric guest-exit field in this response.
The marker, empty stderr and successful execution status establish this bounded recovery
probe. A numeric guest `exitCode=0` was separately observed for the managed dummy test below.
The final Agent view still reported Ready and the expected
`Microsoft.CPlat.Core.RunCommandLinux` **1.0.12** handler Ready / Plugin enabled.
No application extension or unrelated extension installation was requested.

**Independent recovery PASS for the live Agent/Run Command path, including while Tailscale
is unenrolled.** It still depends on Azure control-plane availability, current RBAC, Agent
health and guest connectivity; it is not independent of Azure or a disaster-recovery test.
Successful invoke/create/show/delete operations demonstrate permission for those operations
under this identity; no minimal-role/deny-assignment audit or RBAC changes were performed.
Microsoft's [action Run Command guidance](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command)
documents execution permissions and automatic handler installation.

Serial Console is **GAP**: boot diagnostics are not configured, console access was not
exercised, and a usable password-bearing console account was not established. Microsoft's
[Linux Serial Console prerequisites](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/serial-console-linux)
include boot diagnostics and a suitable local account. Do not enable SSH password
authentication as a shortcut. Managed-disk repair remains a separate, untested fallback:
deallocate, preserve exact OS/data identities and evidence, and use an explicitly approved
isolated repair environment. No detach, repair VM, snapshot, repair operation or settings
change was authorized or attempted by this assessment.

## Actual cloud-init and OpenSSH findings

The first diagnostic's JSON exceeded Azure's trailing-output limit. Its retained tail
established package/service/disk facts, but the missing beginning was not accepted as a
complete cloud-init result. A smaller second script retrieved the exact failure without
changing guest state:

```text
cloud-init status --format json: exit 1
status: error
extended_status: error - done
errors: ('scripts_user', RuntimeError('Runparts: 1 failures (runcmd) in 1 attempted commands'))
boot_status_code: enabled-by-generator

/usr/sbin/sshd -t: exit 255
Missing privilege separation directory: /run/sshd

/usr/sbin/sshd -T: exit 255
Missing privilege separation directory: /run/sshd

cloud-init-output.log:
Missing privilege separation directory: /run/sshd
2026-11-24 01:27:52,216 - cc_scripts_user.py[WARNING]: Failed to run module scripts_user (scripts in /var/lib/cloud/instance/scripts)

/run/sshd exists: false
POLYMIND_BOOTSTRAP_COMPLETE occurrences: 0
```

The installed `/usr/local/sbin/polymind-firstboot.sh` SHA256 is
`2f567326350a3da849e36a1782e2cb77cb97bdf755ceaff545f11f98ded1075c`, identical to the
script extracted locally from `/tmp/polymind-tailscale-cloud-init.yaml`.
Review of that exact script explains the stop: `set -euo pipefail` reaches `sshd -t`
before `systemctl enable --now ssh`, then exits on the absent runtime directory. The
enable commands and final marker are therefore not established by executing this script.
The successful installed-package and service observations below remain valid independently.

| Check | Exact observation | Decision |
|---|---|---|
| OpenSSH package | `openssh-server 1:9.6p1-3ubuntu13.20 install ok installed` | PASS |
| Tailscale package | `tailscale 1.104.7 install ok installed` | PASS |
| SSH service | inactive/dead, disabled; systemd Result success / ExecMainStatus 0 | GAP for service activation |
| SSH socket | active/listening, enabled; Result success | PASS for socket activation only |
| TCP listeners | `0.0.0.0:22`, `[::]:22`, local DNS 53; no application listener observed | PASS for observed inventory |
| SSH validator | `sshd -t` and `sshd -T` fail as above | FAIL for current readiness validation |
| Installed drop-in | `99-polymind.conf`: PasswordAuthentication no; KbdInteractiveAuthentication no; PermitRootLogin no; PubkeyAuthentication yes | PASS for file presence/content |
| Other auth drop-ins | `50-cloud-init.conf`, `60-cloudimg-settings.conf`: PasswordAuthentication no | PASS for inspected settings |
| Effective/authentication proof | No successful effective dump or SSH authentication | GAP |
| tailscaled | active and enabled | PASS |
| Bootstrap completion | cloud-init error, no marker | FAIL |

An inactive ssh.service is compatible with Ubuntu socket activation and is **not by itself
proof that SSH connections would fail**. The port is held by the socket; no activation or
authentication attempt was made. `PHASE_19B_OPENSSH_SERVICE: FAIL` below refers to the unmet
requested service/bootstrap readiness and failed validator, not an invented failed SSH
connection. The NSG still denies ordinary inbound traffic, so the all-interface SSH socket
is not a public exposure finding.

The smallest proposed repair, **not executed**, is to review the installed ssh unit's
RuntimeDirectory behavior, then authorize a targeted `systemctl enable --now ssh.service`
through the verified Agent path. Verify unit health, `sshd -t` and selected `sshd -T` fields,
including forwarding required for the later loopback tunnel. This should let systemd prepare
its runtime directory without reinstalling packages or recreating the VM. Confirm rather
than assume that result. Preserve the original cloud-init failure; use a dated repair record
and separate completion evidence instead of forging the original marker or blindly rerunning
cloud-init/apt. Any later bootstrap-source correction needs its own reviewed change.

## Tailscale, protected parameters and Windows handoff

Guest Tailscale reports **NeedsLogin**, no Tailscale IPs and no current tailnet. Windows
peer inventory has no VM. Installation is PASS; enrollment is GAP and was deliberately not
attempted. No real authentication key was generated, supplied, read or consumed.

The intended subsequent enrollment remains: correct personal-email tailnet,
`tag:polymind-vm` owned by `autogroup:admin`, short-lived single-use tagged key, non-ephemeral
server, standard OpenSSH, Tailscale SSH disabled, no advertised subnet/exit routes,
no unnecessary accepted routes, and `--accept-dns=false`. These are reviewed intent,
not verified current VM enrollment preferences. [Tailscale auth-key documentation](https://tailscale.com/docs/features/access-control/auth-keys)
describes key attributes and expiry; the operator must explicitly perform the real security
action only after the handoff and policy are approved.

Current CLI help and installed CLI implementation confirm that `--protected-parameters`
accepts `name=value` entries and constructs parameter objects with `name` and `value`.
The [managed Linux Run Command documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command-managed)
describes Linux named-parameter environment delivery, captured status/output and deletion.
The actual dummy proof used exactly this non-secret command:

```bash
az vm run-command create --resource-group rg-epolymind --vm-name vm-epolymind-dev \
  --name phase19b-protected-dummy-20261124 --location spaincentral \
  --async-execution false --timeout-in-seconds 60 \
  --protected-parameters POLYMIND_HANDOFF_DUMMY=phase19b-dummy-only \
  --script 'if [ "${POLYMIND_HANDOFF_DUMMY:-}" = "phase19b-dummy-only" ]; then printf "PROTECTED_PARAMETER_DUMMY_OK\n"; else printf "PROTECTED_PARAMETER_DUMMY_MISSING\n"; exit 7; fi' \
  --query '{id:id,provisioningState:provisioningState}' -o json

az vm run-command show --resource-group rg-epolymind --vm-name vm-epolymind-dev \
  --name phase19b-protected-dummy-20261124 --expand instanceView \
  --query '{id:id,provisioningState:provisioningState,instanceView:instanceView}' -o json
```

Both CLI commands exited 0. The child ID ends in
`/runCommands/phase19b-protected-dummy-20261124`. Result:

```json
{
  "provisioningState": "Succeeded",
  "instanceView": {
    "startTime": "2026-11-24T01:46:38+00:00",
    "endTime": "2026-11-24T01:46:38+00:00",
    "executionState": "Succeeded",
    "executionMessage": "Execution completed",
    "exitCode": 0,
    "output": "PROTECTED_PARAMETER_DUMMY_OK\n",
    "error": ""
  }
}
```

Only a safe marker was returned. Linux delivery under the expected variable name is PASS.
This command intentionally contains a **dummy value in local process arguments**. It is
not a safe real-key submission template. The installed CLI wrapper does not establish a
protected-value file-input mechanism; invoking shell substitution would still put the
real value in process arguments. CLI/debug/HTTP logging, local history, process inspection,
guest environment access by root and accidental script output remain separate threats.
Protected Azure delivery alone cannot close them. The local CLI source also logs invocation
arguments at debug level; no assertion of comprehensive local log redaction is made.

**PROTECTED_TAILSCALE_HANDOFF: GAP.** No reviewed and dummy-tested end-to-end real-key
handoff was established. Stop before real enrollment. The next concrete review should
cover a masked interactive operator prompt with an in-memory structured request, no
secret-bearing child-process arguments or source/history files, verified logging behavior,
bounded protected delivery, safe guest consumption without a secret-bearing Tailscale argv,
and cleanup on every exit. A protected root-only runtime file or supported in-memory guest
interface requires verification before use. Do not invent CLI `@file` semantics, install
large SDK/Az dependencies, retrieve credentials or create Key Vault to bypass this GAP.

After recording success, the following cleanup exited 0, and the subsequent list returned
`[]` with exit 0:

```bash
az vm run-command delete --resource-group rg-epolymind --vm-name vm-epolymind-dev \
  --name phase19b-protected-dummy-20261124 --yes -o none
az vm run-command list --resource-group rg-epolymind --vm-name vm-epolymind-dev \
  --query '[].{name:name,id:id}' -o json
```

Deleting this child is not proof of erasing all platform/Agent execution artifacts. No real
secret entered them. The required Run Command Agent handler was not removed as cleanup.
The show command emitted a deprecation warning for `--expand`; it is supported by this
installed version and actually returned instanceView. No extension upgrade was attempted.

Windows PowerShell interoperability, after sandbox approval, returned:

| Requirement | Actual observation | Decision |
|---|---|---|
| Operator host | `SUSANTA-HP-PRO` | PASS |
| OpenSSH | Windows System32 OpenSSH, `OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2` | PASS |
| Key files | Dedicated private and public filenames exist; only `.pub` fingerprint read | PASS for presence |
| Tailscale service/backend | Running / Running | PASS |
| Tailnet | CurrentTailnet.Name matches intended personal-email account; DNS suffix `tail456874.ts.net`; email omitted here | PASS for Windows active identity |
| Windows device | Online, `100.108.249.65`, untagged | PASS |
| Android peer | `100.64.92.70`, offline in observed status | PASS for metadata only |
| VM device/tag | No VM peer; guest NeedsLogin | GAP |
| Saved policy/test result | Not independently read from admin API | UNKNOWN |
| Private TCP 22/key login | Not attempted before enrollment/SSH repair | GAP |

The operator-side policy checklist is: inspect the correct tailnet; verify tag owner and
the exact laptop source, destination `tag:polymind-vm`, TCP 22 grant; confirm the phone is
not included by a broader user/autogroup selector; verify no VM-to-personal-device grant
and no unrestricted allow-all entry; run and retain policy tests, including explicit
Android-to-VM deny, laptop-to-VM allow and VM-to-personal-device deny; preserve personal
device access and the existing Tailscale SSH policy. Standard SSH traffic and Tailscale SSH
policy are separate. No policy modification was performed.

After explicit enrollment, require correct tailnet/tag/online metadata, actual relay or
direct transport evidence, Windows `Test-NetConnection <verified-VM-tail-IP> -Port 22`,
and interactive Windows `ssh -o IdentitiesOnly=yes -i "$env:USERPROFILE\.ssh\id_ed25519_polymind_azure" polymindadmin@<verified-VM-tail-IP>`.
Compare the host fingerprint above before trusting it; do not disable host verification.
Enter the passphrase only in the local SSH prompt. Retain sanitized successful key-auth
evidence and effective guest restrictions. Offline Android status does not prove policy denial.

For later application acceptance, the private SSH tunnel must reach VM `127.0.0.1:9443`.
Retain a local loopback bind, fixed reviewed HTTPS hostname, certificate trust, exact origin
and Entra callback. No certificate bypass, gateway rebind, Redis/Chroma/API port publication
or Tailscale SSH shortcut is authorized. Successful SSH alone is not deployed application
or real browser/OIDC acceptance.

## Evaluation window, current retail estimates and residual exposure

The timestamp basis is VM `timeCreated`, not the later provisioning-status timestamp or
the start of Codex. At **2026-11-24 01:53:44.385048 UTC**, elapsed time is **00:27:05.609034**,
remaining **07:32:54.390966**. Cutoff is **09:26:38.7760141 UTC**. The VM remains allocated
and running; early deallocation was not due or requested. No stop/deallocate was issued.

Unauthenticated official retail API GETs completed **01:45:27–01:45:31 UTC on 24 November**.
USD, Consumption, Spain Central, Linux PAYG; exclude Windows/Spot/Low Priority. These are
current retail estimates, not contract rates, invoices, tax/FX or exact accrued costs.
All four result sets had no next-page link. Queries and meter observations are preserved
below. Source interface: [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices).

| Selected meter | USD rate | Meter ID |
|---|---:|---|
| D2s v4, Virtual Machines Dsv4 Series, Spain Central | 0.107/hour | `53b5d786-28cb-5cdf-a644-6dd7e49469d5` |
| E6 LRS Disk, Spain Central, each disk | 4.80/month | `a78a4e9c-48d8-59e1-8d89-8dc39a13aeb8` |
| E6 LRS Disk Operations | 0.002 / 10,000 operations | `18f18f9e-8478-59ba-8de3-b52200807a0b` |
| Standard NAT Gateway, Global applicable meter | 0.045/hour | `ae30040a-67f5-485b-b0f4-a6ef50504d9c` |
| Standard NAT Data Processed, Global | 0.045/GB | `d32b6352-b66b-4c4c-8f21-60e94058e04d` |
| Standard IPv4 Static Public IP, Spain Central | 0.005/hour | `9c150bf9-2bad-430e-a53c-c213804f49ef` |

VM/disk/IP rows have effective start 2024-02-01; selected NAT rows 2020-06-01. These
are rows returned by today's query, not a reused historical quote. The disk response also
contains an **E6 LRS Disk Mount** meter of USD 0.610844/month; applicability was not verified
and is not silently counted as ordinary disk capacity. No shared-disk mount was requested
in the observed deployment. Confirm applicable meters against subscription billing.

Resource inventory creation times establish NAT at **2026-11-23 12:36:38.351872 UTC** and
its public IP at **12:36:35.754777 UTC**, about **12 hours 50 minutes before the VM**.
At the calculation time NAT has existed for **13:17:06**, independently of VM runtime.
The simplified estimate uses NAT creation for both NAT/IP; the IP's roughly 2.6-second
earlier existence is immaterial to the rounded subtotal, not an exact billing calculation.

| Estimate/scenario, excluding variable charges and tax | USD |
|---|---:|
| VM from creation to 01:53:44 at 0.107/hour | 0.0483 |
| NAT + PIP from NAT creation to 01:53:44 at 0.05/hour | 0.6643 |
| Two disk capacities to 01:53:44, illustrative monthly /730-hour proration | 0.0059 |
| Illustrative observed-time fixed subtotal | **0.7185** |
| Full eight-hour VM compute | 0.8560 |
| NAT + PIP from their earlier creation through VM cutoff | 1.0417 |
| Eight hours of two-disk capacity, /730 proration | 0.1052 |
| Illustrative fixed subtotal through cutoff | **2.0029** |
| Two disks retained for 30 days total, 720/730 monthly proration | about 9.47 |
| NAT + PIP left retained after VM deallocation | 1.20/day; 36.50/730 hours |

Capacity proration and continuous allocation are estimate assumptions, not proof of billed
seconds or meter granularity. Add actual disk operations, NAT data, Internet/peering transfer,
any applicable mount/policy/monitoring charges and other billable services. No snapshots
were listed in `rg-epolymind`; no snapshot was created. Historical ACR/Foundry/managed Redis
and AKS-managed resources remain outside this incremental estimate and were not changed.
No Cost Management actual-cost query or invoice reconciliation was performed.

The USD 30 target is not a hard cap. Fixed estimates are below it, but neither that fact
nor the stopped AKS state guarantees the final invoice. **Cost governance GAP** remains
for ongoing cutoff ownership/execution and actual-cost/residual reconciliation. No
autonomous monitoring continues after this turn. The operator must arrange cutoff coverage,
check the actual state at deallocation and reconcile billing after ingestion lag.

## Resource-specific deallocation and teardown plan — not executed

By **09:26:38 UTC today**, use the already approved boundary procedure after verifying
the account and exact VM identity; do not wait for optional application diagnostics:

```bash
az account show --query '{subscription:id,tenant:tenantId,state:state}' -o json
az vm show -g rg-epolymind -n vm-epolymind-dev --query '{id:id,timeCreated:timeCreated}' -o json
az vm deallocate --resource-group rg-epolymind --name vm-epolymind-dev
az vm get-instance-view -g rg-epolymind -n vm-epolymind-dev \
  --query 'instanceView.statuses' -o json
```

Require actual `PowerState/deallocated` / Stopped (deallocated). Guest shutdown, stopping
Compose or `PowerState/stopped` does not meet the billing boundary. [Azure states and billing](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing)
distinguishes those states and continuing disk/network charges. If resumed work finds the
window expired while allocated, record identity/state and prioritize that approved
deallocation before any optional probe. Do not start it again without new authorization.

| Resource | Retention/disposal decision |
|---|---|
| `vm-epolymind-dev` | Deallocate at deadline; do not delete/recreate/resize |
| Its exact OS and LUN-0 disks named above | Retain up to approved 30 days, review by 24 December 2026; no automatic deletion or formatting |
| `vm-epolymind-devVMNic` | Retain with VM; no NIC or public IP replacement |
| `nat-epolymind-vm-dev` | Separate coordinated removal after outbound/recovery use is finished |
| `pip-epolymind-nat-dev` | Separate coordinated removal after NAT deletion releases it |
| VNet, subnet, NSG, reciprocal peerings | Preserve; shared/historical boundaries are not teardown targets |
| AKS and its managed RG; historical private endpoints/DNS/Redis/Foundry/ACR | Preserve untouched; no broad RG deletion |
| Managed Run Command dummy | Already deleted; confirmed empty child list |

The concrete **subsequent coordinated network teardown**, not permission to execute now,
is: recheck the named NAT's subnet list; confirm the sole dependent subnet and no pending
Agent/access requirement; approve the outage; detach NAT only from `snet-polymind-vm`;
delete only that named NAT; then delete only its named PIP after checking references.
Candidate commands for that separately coordinated step are:

```bash
az network nat gateway show -g rg-epolymind -n nat-epolymind-vm-dev -o json
az network vnet subnet update -g rg-epolymind --vnet-name vnet-epolymind-private-dev \
  -n snet-polymind-vm --remove natGateway
az network nat gateway delete -g rg-epolymind -n nat-epolymind-vm-dev
az network public-ip delete -g rg-epolymind -n pip-epolymind-nat-dev
```

Do not execute deletion if new dependents appear or required recovery/access would be
interrupted. Verify deletion and subsequent billable inventory. Disk retention still bills;
retain a named operator review rather than silently deleting at expiry.

## Acceptance matrix and smallest safe closure actions

PASS denotes observed evidence, GAP incomplete configuration/verification, FAIL an observed
failed check, UNKNOWN unavailable evidence. Broad result labels are qualified by scope.

| Requirement | Result | Smallest safe next action and closure evidence |
|---|---|---|
| VM provisioned | PASS | Exact VM/control-plane/image evidence above |
| Trusted Launch / Secure Boot / vTPM | PASS | Actual Azure fields above |
| Overall VM security | GAP | Resolve SSH validation; capture effective auth/forwarding settings; custodian disposition of disk-export and guest-firewall policy |
| No VM public IP / NSG / NAT / AKS CIDR isolation | PASS | NIC/IP inventory, effective denies, reciprocal peering and stopped AKS; tailnet/private authentication remains separate |
| HTTPS/DNS prerequisites | PASS | Actual guest HTTPS codes, resolver and successful Run Command; not every possible endpoint tested |
| Long-term time source | UNKNOWN | Identify active sync source/health read-only; do not assume external NTP works |
| Disk attachment/delete policies | PASS | Two exact attached 64-GiB Standard SSDs, Detach, NIC Delete |
| Durable filesystem/state | GAP | Explicitly approve exact data-disk initialization; verified UUID/local filesystem/mount, owners, mount-failure behavior and deliberate authority decision |
| Azure Agent | PASS | Ready plus actual successful execution |
| Azure Run Command recovery | PASS | Recovery marker/provisioning success; managed dummy numeric exit 0 independently |
| Serial Console fallback | GAP | Review boot diagnostics and secure console-account requirements under separate approval; no password weakening; test only if approved |
| Managed-disk repair fallback | GAP | Review isolated recovery custody/procedure and availability; a separate approved controlled test is needed for tested-repair claims |
| Actual cloud-init completion | FAIL | Authorize bounded SSH runtime/service repair; retain original failure and append repair/revalidation evidence, without rerunning installation blindly |
| OpenSSH readiness | FAIL | Review unit RuntimeDirectory; targeted service activation; `sshd -t` exit 0 and effective restrictions; socket listener alone is insufficient |
| Tailscale installed/service | PASS | Package installed; tailscaled active/enabled |
| Protected dummy delivery | PASS | Expected variable consumed, safe marker, managed exit 0, child cleanup |
| Real-key handoff | GAP | Review and dummy-test a full path excluding secret argv/history/source/logs and safe guest key consumption/cleanup before any real key |
| VM Tailscale enrollment | GAP | Only after explicit operator action and safe handoff: tagged non-ephemeral VM online in correct tailnet, correct DNS/routes/SSH preferences |
| Saved policy and Android deny | UNKNOWN | Operator admin policy/test evidence; offline phone status is insufficient |
| Windows prerequisites/key fingerprint | PASS | Actual service/backend/OpenSSH/existence/public-fingerprint observations |
| Windows private SSH authentication | GAP | After repair/enrollment/policy: actual TCP 22, host-key comparison and interactive dedicated-key login; never collect passphrase |
| Deadline/retail estimate identified | PASS | Actual creation/cutoff and current official prices |
| Full cost governance | GAP | Operator cutoff coverage, actual deallocation evidence, coordinated NAT/PIP disposition, actual-cost reconciliation and disk review |
| Compose offline versus live | GAP for live | Current five-service file is inspected; no VM Compose deployment or acceptance performed |
| Private HTTPS / real browser Entra | GAP | Preserve exact hostname/TLS/origin/callback; separately approved real browser/API acceptance after private transport exists |
| Application readiness | NO | Storage, immutable artifact transfer, reviewed private config/trust/identity, approved lifecycle and recovery/capacity gates still required |
| Paid model inference | NOT AUTHORIZED | Separate A3/A4/A5 review; no inference test or permission was issued |

## Follow-on requirements before application deployment

1. Keep the cutoff covered; stop work and deallocate when due. A later allocated window
   needs explicit authorization rather than silently resetting today's clock.
2. Obtain a narrow SSH service/runtime repair authorization, preserve the cloud-init
   incident and verify effective restrictions and host identity through Run Command.
3. Close the real-key handoff and policy-test GAPs; let the operator explicitly enroll
   the single-use tagged identity. Verify real Windows OpenSSH access over Tailscale,
   retaining Agent recovery and the current NSG. No public route or firewall relaxation.
4. Obtain specific disk initialization/state-provenance authorization; prepare local ext4
   persistence and mount-aware supervision. Review disk export/recovery policy separately.
5. Freeze and verify immutable application/vendor image identities and transfer checksums;
   inspect Docker/Compose host prerequisites without installing or launching automatically.
   This assessment neither installed Docker nor proved it is installed on the VM.
6. Supply reviewed private TLS/origin/Entra inputs, authority custody, source/config bindings
   and controlled egress. Preserve seven current authorities or deliberately approve an
   isolated new set. A broad HTTPS NSG permit is not zero-paid synthetic enforcement.
7. Obtain separate production-lifecycle authorization. Then use only the existing five
   services, gateway host `127.0.0.1:9443`, internal API/cache/vector ports and one API/runner.
   Validate real private browser/OIDC and zero-paid workflows; perform bounded capacity,
   missing-mount/restart, coherent off-disk backup/isolated restore and rollback acceptance.
8. Keep provider/source/capability, pricing/shared quota/financial reconciliation and fresh
   independent live-execution permission gates separate. Infrastructure approval, package
   reachability, login and application readiness grant no model calls or public launch.

## Exact command evidence record

The following generated inventory records preserve the exact successfully executed
read-only CLI argument vectors (rendered with shell quoting). Their selected results are
the sanitized tables above. Initial sandbox failures and timeout limitations are recorded
after the command appendix. No raw Azure credential, full guest log or authority database
is included. The public-key query returned only public configuration and was immediately
reduced locally to the fingerprint shown above.

**account**, 2026-11-24T01:41:26.131546+00:00, exit 0:

```bash
az account show --query '{subscription:id,name:name,state:state,tenant:tenantId}' -o json --only-show-errors
```

**vm**, 2026-11-24T01:41:26.742311+00:00, exit 0:

```bash
az vm show -g rg-epolymind -n vm-epolymind-dev --query '{id:id,name:name,location:location,timeCreated:timeCreated,hardware:hardwareProfile,image:storageProfile.imageReference,security:securityProfile,osDisk:storageProfile.osDisk,dataDisks:storageProfile.dataDisks,nics:networkProfile.networkInterfaces,admin:osProfile.adminUsername,passwordDisabled:osProfile.linuxConfiguration.disablePasswordAuthentication,agentProvisioned:osProfile.linuxConfiguration.provisionVMAgent,diagnostics:diagnosticsProfile}' -o json --only-show-errors
```

**instance**, 2026-11-24T01:41:30.225876+00:00, exit 0:

```bash
az vm get-instance-view -g rg-epolymind -n vm-epolymind-dev --query '{id:id,statuses:instanceView.statuses,agent:instanceView.vmAgent,osName:instanceView.osName,osVersion:instanceView.osVersion,extensions:instanceView.extensions}' -o json --only-show-errors
```

**ips**, 2026-11-24T01:41:30.226368+00:00, exit 0:

```bash
az vm list-ip-addresses -g rg-epolymind -n vm-epolymind-dev -o json --only-show-errors
```

**nics**, 2026-11-24T01:41:27.868742+00:00, exit 0:

```bash
az network nic list -g rg-epolymind --query '[].{id:id,name:name,vm:virtualMachine.id,nsg:networkSecurityGroup.id,ipConfigurations:ipConfigurations,dns:dnsSettings,forwarding:enableIPForwarding}' -o json --only-show-errors
```

**vnet**, 2026-11-24T01:41:30.228571+00:00, exit 0:

```bash
az network vnet show -g rg-epolymind -n vnet-epolymind-private-dev --query '{id:id,addressSpace:addressSpace,dns:dhcpOptions,subnets:subnets,peerings:virtualNetworkPeerings}' -o json --only-show-errors
```

**nsg**, 2026-11-24T01:41:31.625143+00:00, exit 0:

```bash
az network nsg show -g rg-epolymind -n nsg-epolymind-vm-dev --query '{id:id,rules:securityRules,defaults:defaultSecurityRules,subnets:subnets,interfaces:networkInterfaces}' -o json --only-show-errors
```

**effective_nsg**, 2026-11-24T01:41:32.519939+00:00, exit 0:

```bash
az network nic list-effective-nsg -g rg-epolymind -n vm-epolymind-devVMNic -o json --only-show-errors
```

**routes**, 2026-11-24T01:41:33.219672+00:00, exit 0:

```bash
az network nic show-effective-route-table -g rg-epolymind -n vm-epolymind-devVMNic -o json --only-show-errors
```

**nat**, 2026-11-24T01:41:31.629527+00:00, exit 0:

```bash
az network nat gateway show -g rg-epolymind -n nat-epolymind-vm-dev --query '{id:id,sku:sku,publicIps:publicIpAddresses,subnets:subnets,idleTimeout:idleTimeoutInMinutes,provisioning:provisioningState}' -o json --only-show-errors
```

**publicips**, 2026-11-24T01:41:32.023667+00:00, exit 0:

```bash
az network public-ip list -g rg-epolymind --query '[].{id:id,name:name,sku:sku,ip:ipAddress,ipConfiguration:ipConfiguration,natGateway:natGateway,allocation:publicIPAllocationMethod}' -o json --only-show-errors
```

**disks_exact**, 2026-11-24T01:45:22.817160+00:00, exit 0:

```bash
az disk list -g rg-epolymind --query '[].{id:id,size:diskSizeGB,sku:sku.name,state:diskState,timeCreated:timeCreated,managedBy:managedBy,hyperV:hyperVGeneration,encryption:encryption.type,networkAccessPolicy:networkAccessPolicy,publicNetworkAccess:publicNetworkAccess}' -o json --only-show-errors
```

**aks**, 2026-11-24T01:41:33.437414+00:00, exit 0:

```bash
az aks show -g rg-epolymind -n epolymind-aks-dev --query '{id:id,power:powerState,provisioning:provisioningState,nodeResourceGroup:nodeResourceGroup,pools:agentPoolProfiles[].{name:name,subnet:vnetSubnetId},network:networkProfile}' -o json --only-show-errors
```

**aks_vnet**, 2026-11-24T01:45:23.897195+00:00, exit 0:

```bash
az network vnet show -g MC_rg-epolymind_epolymind-aks-dev_spaincentral -n aks-vnet-36185111 --query '{id:id,addressSpace:addressSpace,peerings:virtualNetworkPeerings[].{name:name,state:peeringState,remote:remoteVirtualNetwork.id,allowVnet:allowVirtualNetworkAccess,allowForwarded:allowForwardedTraffic,useRemoteGateways:useRemoteGateways}}' -o json --only-show-errors
```

**inventory**, 2026-11-24T01:41:33.918070+00:00, exit 0:

```bash
az resource list -g rg-epolymind --query '[].{id:id,name:name,type:type,location:location,created:createdTime}' -o json --only-show-errors
```

**snapshots**, 2026-11-24T01:45:22.814285+00:00, exit 0:

```bash
az snapshot list -g rg-epolymind --query '[].{id:id,name:name,created:timeCreated,size:diskSizeGB,sku:sku.name}' -o json --only-show-errors
```

**image**, 2026-11-24T01:45:24.325733+00:00, exit 0:

```bash
az vm image show -l spaincentral --urn Canonical:ubuntu-24_04-lts:server:24.04.202611170 --query '{id:id,architecture:architecture,hyperVGeneration:hyperVGeneration,os:osDiskImage,features:features}' -o json --only-show-errors
```

**azure_key**, 2026-11-24T01:45:24.403045+00:00, exit 0:

```bash
az vm show -g rg-epolymind -n vm-epolymind-dev --query osProfile.linuxConfiguration.ssh.publicKeys -o json --only-show-errors
```

**runcommand_list**, 2026-11-24T01:41:35.560906+00:00, exit 0:

```bash
az vm run-command list -g rg-epolymind --vm-name vm-epolymind-dev --query '[].{id:id,name:name,provisioningState:provisioningState}' -o json --only-show-errors
```

**Public retail vm query**, 2026-11-24T01:45:31.702204+00:00:

[Exact official API request](https://prices.azure.com/api/retail/prices?%24filter=armRegionName+eq+%27spaincentral%27+and+armSkuName+eq+%27Standard_D2s_v4%27+and+serviceName+eq+%27Virtual+Machines%27+and+priceType+eq+%27Consumption%27&currencyCode=%27USD%27)

**Public retail disk query**, 2026-11-24T01:45:27.265199+00:00:

[Exact official API request](https://prices.azure.com/api/retail/prices?%24filter=armRegionName+eq+%27spaincentral%27+and+serviceName+eq+%27Storage%27+and+priceType+eq+%27Consumption%27+and+%28skuName+eq+%27E6+LRS%27+or+meterName+eq+%27E6+LRS+Disk+Operations%27%29&currencyCode=%27USD%27)

**Public retail nat query**, 2026-11-24T01:45:31.693283+00:00:

[Exact official API request](https://prices.azure.com/api/retail/prices?%24filter=productName+eq+%27NAT+Gateway%27+and+priceType+eq+%27Consumption%27&currencyCode=%27USD%27)

**Public retail ip query**, 2026-11-24T01:45:30.433259+00:00:

[Exact official API request](https://prices.azure.com/api/retail/prices?%24filter=armRegionName+eq+%27spaincentral%27+and+productName+eq+%27IP+Addresses%27+and+priceType+eq+%27Consumption%27&currencyCode=%27USD%27)

## Diagnostic commands and observation limits

The two guest invocations were exactly:

```bash
az vm run-command invoke --resource-group rg-epolymind --name vm-epolymind-dev --command-id RunShellScript --scripts @/tmp/polymind-phase19b-postvm/guest.sh -o json
az vm run-command invoke --resource-group rg-epolymind --name vm-epolymind-dev --command-id RunShellScript --scripts @/tmp/polymind-phase19b-postvm/guest_focused.sh -o json
```

Each CLI invocation exited 0 with `ProvisioningState/succeeded` and empty outer stderr.
That is script-transport success, not cloud-init/SSH success: the scripts recorded individual
exit codes without treating a failed subordinate command as a successful readiness check.
The first script queried cloud-init, lsb_release/uname, systemctl active/enabled statuses,
dpkg-query for three packages, selected sshd fields, authorized/host public fingerprints,
`ss -lnt`, `ufw status`, iptables rule count, `lsblk -J -b`, the LUN symlink, findmnt,
bootstrap script hash and marker/error counts, selected non-secret Tailscale status fields,
resolvectl, timedatectl, clocksource and three eight-second HTTPS HEAD requests.
The focused script used `cloud-init status --format json`, `sshd -t`, selected `sshd -T`,
`systemctl show ssh.service ssh.socket`, `lsb_release -ds`, `uname -m`,
`wipefs --no-act /dev/disk/azure/scsi1/lun0`, known failure-line filtering, runtime-directory
existence and only authentication directive lines from SSH drop-ins. Their outputs are
recorded above; no environment dump, Tailscale AuthURL, private key or full log was printed.

The exact Windows command was (the private file is queried only by `Test-Path`):

```bash
powershell.exe -NoProfile -NonInteractive -Command '$ErrorActionPreference="Stop"; $ts=Join-Path $env:ProgramFiles "Tailscale\tailscale.exe"; [pscustomobject]@{Computer=$env:COMPUTERNAME;SSH=(Get-Command ssh.exe).Source;TailscalePresent=(Test-Path $ts);PrivateKeyPresent=(Test-Path (Join-Path $env:USERPROFILE ".ssh\id_ed25519_polymind_azure"));PublicKeyPresent=(Test-Path (Join-Path $env:USERPROFILE ".ssh\id_ed25519_polymind_azure.pub"));TailscaleService=(Get-Service Tailscale).Status.ToString()} | ConvertTo-Json -Compress; ssh.exe -V; ssh-keygen.exe -lf (Join-Path $env:USERPROFILE ".ssh\id_ed25519_polymind_azure.pub"); $s=(& $ts status --json | ConvertFrom-Json); [pscustomobject]@{BackendState=$s.BackendState;TailnetName=$s.CurrentTailnet.Name;MagicDNSSuffix=$s.CurrentTailnet.MagicDNSSuffix;SelfHostName=$s.Self.HostName;SelfOnline=$s.Self.Online;SelfIP=$s.Self.TailscaleIPs;SelfTags=$s.Self.Tags;Peers=@($s.Peer.PSObject.Properties.Value | ForEach-Object {[pscustomobject]@{HostName=$_.HostName;Online=$_.Online;IPs=$_.TailscaleIPs;Tags=$_.Tags}})} | ConvertTo-Json -Depth 5'
```

Actual account email was omitted from this report. No Windows SSH command using the private
key was executed. Tailnet admin policy cannot be reconstructed from client peer status.

Several sandbox Azure invocations failed **before Azure execution** because CLI could not
write `/home/home/.azure/commands/` (read-only filesystem). Windows interoperability initially
failed its WSL socket restriction; public-price GETs initially failed sandbox DNS. These were
rerun through the execution approval mechanism, not by copying credentials or weakening
security. One local timestamp parser rejected Azure's seven fractional digits; it was
corrected to parse microseconds while retaining the original timestamp. The first disk
query used `diskSizeGb` and returned null; the corrected `diskSizeGB` query returned 64
for both disks. These intermediate failures are not counted as successful cloud tests.
The initial `az vm list-skus` attempt has no completed saved result following the tool
restart. The later bounded attempt timed out at 60 seconds and was not retried indefinitely.
One helper exited 1 because that timeout propagated after its other
independent reads had completed; those per-command exit-0 records remain valid.

## Review, verification and final Git inventory

This task changes documentation only. No application implementation, API, provider boundary,
dependency, Compose port, persistent authority, credential or production configuration was
changed. Pytest, application compilation and Docker builds were not rerun: there is no source
or image change requiring them, and this prompt explicitly avoids duplicating the complete
application regression suite. Live infrastructure probes above are the relevant verification.

Implementation self-review distinguished Azure provisioning from guest completion, socket
activation from daemon/authentication, active Agent from a successful recovery probe,
protected dummy delivery from real-key handoff, disk attachment from durable mounts,
effective NSG filtering from tailnet policy, and current retail estimates from actual billing.
It also preserved original cloud-init failure evidence and the temporal boundary with earlier
offline reports. No repair, public access or inference was introduced to obtain a PASS.

Separate pre-commit review checks the new prompt/report and the guide append for private-key,
token/JWT/Tailscale-key payloads, credentials, raw sensitive logs, databases, temporary/generated
artifacts, unrelated changes, broken local links and whitespace. Baseline SHA256 checks
verify preservation of all six existing documentation changes (the VM guide must retain
the complete baseline as its prefix). Final executed check outcomes and Git statistics
are appended after review. Nothing is staged; no commit or push occurred.

Final local verification: `git diff --check` exited **0**; the dedicated documentation
scanner exited **0**, checking **4 local Markdown links**, with **0 broken links** and
**0 secret-payload pattern findings** across this task's prompt, report and VM guide.
All **6 pre-existing changed/untracked files** pass preservation checks: five are
byte-identical to baseline, and the guide retains its complete baseline prefix. Secret
patterns are a bounded check, complemented by manual content/diff review; they are not a
credential-leak certification. An initial custom whitespace assertion incorrectly treated
newlines as trailing whitespace; correcting the checker found no actual whitespace issue.

Final `git status --short --branch`:

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

Final `git diff --stat`: **4 files changed, 135 insertions(+), 8 deletions(-)**.
This includes the preserved earlier tracked changes and **28 added VM-guide lines** from
this task. It excludes all four untracked Markdown files; two of those were already present,
and this task adds only the post-creation prompt/report. `git diff --cached --name-only`
is empty. No source/generated/runtime artifact was added, no history or index was changed,
and **no commit or push occurred**.

## Machine-readable result

```text
PHASE_19B_VM_PROVISIONING: PASS
PHASE_19B_VM_SECURITY: GAP
PHASE_19B_PRIVATE_NETWORK: PASS
PHASE_19B_DISK_ATTACHMENT: PASS
PHASE_19B_CLOUD_INIT: FAIL
PHASE_19B_OPENSSH_SERVICE: FAIL
PHASE_19B_TAILSCALE_INSTALLATION: PASS
PHASE_19B_TAILSCALE_ENROLLMENT: GAP
PHASE_19B_PROTECTED_PARAMETER_HANDOFF: GAP
PHASE_19B_AZURE_RUN_COMMAND_RECOVERY: PASS
PHASE_19B_WINDOWS_PRIVATE_SSH: GAP
PHASE_19B_COST_GOVERNANCE: GAP
PHASE_19B_INFRASTRUCTURE_READY: NO
PHASE_19B_APPLICATION_DEPLOYMENT_READY: NO
PHASE_19B_REAL_MODEL_INFERENCE_AUTHORIZED: NO
PHASE_19B_PUBLIC_EXPOSURE_AUTHORIZED: NO
PHASE_19B_AKS_REQUIRED: NO
```
