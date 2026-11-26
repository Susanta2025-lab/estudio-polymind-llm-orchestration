# Phase 19B — Streamlit OIDC configuration preparation

26 November 2026, Europe/Lisbon. Repository: `Susanta2025-lab/estudio-polymind-llm-orchestration`.
This report covers offline preparation and procedure verification only. Phase 19A is COMPLETE,
19B remains ACTIVE, and 19C is NOT STARTED.

## 1. Executive summary

The supplied Entra registration evidence is internally consistent with the existing native
Streamlit and API contracts. Exact non-secret configuration is prepared below. The portable
template remains unchanged. No application runtime code, dependency, Compose topology, API
contract, authority or executable image input changed; no application image rebuild is required.

The operator-only preparation procedure privately prompts for the existing client-secret
**value**, independently generates a cookie secret, serializes TOML, creates a private file
without overwrite, and validates it without displaying credentials. Its exact report text is
tested using synthetic values and isolated temporary directories. This establishes procedure
readiness, not actual secret possession, encryption, validity, Azure installation or login.

The expected next step is operator review, then independent preparation outside this Codex
session. Actual API access-token `sub`, runtime enrollment, operational TLS/trust and real
authentication remain blocked. No credential, VM or Entra action was performed.

## 2. Git baseline and CI evidence

Before editing, read the complete root [AGENTS.md](../../../AGENTS.md) and ran:

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline -5
git diff --stat
git diff --check
git diff --cached --name-only
```

All exited 0. Status was only `## master...origin/master`; diff/stat/check and staged names
were empty. No pre-existing operator changes existed. Exact HEAD:
`e0ad729e96934167e616bb63e37efe195f75a43f`.

```text
e0ad729 chore: configure Phase 19B private HTTPS origin and verify deployment integration
1b11b3a docs: reconcile Phase 19B Azure evidence and verify offline readiness
7bf82dc feat: complete Phase 19B offline Azure deployment foundation
b48dde4 feat: improve local app launchers and document frontend reliability
d7d2ec2 fix(ui): resolve Streamlit document module collision and preserve legacy chat
```

Read-only GitHub connector confirmed run `45778620125`, build job `139768317805`, completed
successfully (all reported steps successful). Combined commit statuses returned an empty
list, which alone does not establish an Actions result. The connector's job projection
did not expose head SHA. A read-only `gh api` fallback reconciled the run precisely:

```bash
gh api repos/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45778620125 \
  --jq '{head_sha,head_branch,event,status,conclusion,run_started_at,updated_at,name,html_url}'
```

First sandbox attempt exited 1 because network access was unavailable; execution-approved
retry exited 0. [Estudio PolyMind CI run](https://github.com/Susanta2025-lab/estudio-polymind-llm-orchestration/actions/runs/45778620125)
reports the exact HEAD above, `master`, `push`, `completed`, `success`, start
`2026-11-26T07:52:52Z`, update `2026-11-26T08:00:24Z` (7m32s elapsed). This CI linkage is
independently read back. Entra/VM evidence below remains operator-reported.

## 3. Authorization and evidence boundaries

Authorized work was local source inspection, non-secret documentation, and synthetic offline
verification. No real `.env`, private runtime secrets, personal credential storage or encrypted
personal files were read. No operational secret was generated, retrieved, rotated, printed,
copied or installed. Codex did not run the operator procedures with operational destinations.

No Azure/Graph/Entra command, remote SSH, VM activation, browser login, token acquisition,
provider request, production Compose startup, runtime-authority initialization, execution
permission or financial mutation occurred. External access was restricted to read-only GitHub
CI reconciliation. Real inference count: **0**. No staging, commit, push or history changes.

Inspected every requested template, deployment entrypoint, Compose file, operation/security
guide, architecture/plan, prior HTTPS report and named test. Also inspected actual
`ui/chat_view.py`, `ui/documents_view.py`, API clients, `security/identity.py`,
`security/authority.py`, `security/chat.py`, `deployment/phase19/runtime.py`, settings isolation,
Docker exclusions and installed Streamlit helpers. Historical reports retain their original
findings and test counts. The prior 315-focused/3,329-full results are historical, not reruns.

## 4. Reconciled Entra registration evidence

Every external observation in this section is **OPERATOR_REPORTED_PASS**, dated
25–26 November 2026. No tenant query was made in this task.

| Identity or setting | Reported value / distinction |
|---|---|
| Tenant | `afabeaf8-0fea-42c9-afb4-7e5c07eff3f3`; Azure account Enabled; AzureADMyOrg |
| API application | `estudio-polymind-api-dev` |
| API client ID / token audience | `5aa70f9d-9f9e-4b5b-972b-698d4d68105e` |
| API Application ID URI | `api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e`; scope prefix, not token audience |
| API service principal object ID | `046ce5b0-897c-4289-ad86-e403ac6b6e20` |
| API token version | Requested access-token version `2` |
| Delegated scope | `access_as_user`; enabled; Admin consent requirement |
| Scope UUID | `276cbb61-4f0d-4f08-9ce2-f62c5140813e` |
| API role | `PolyMind.L1Operator`; enabled; allowed member type User |
| Role UUID | `e34bc374-42ff-4a6a-87e2-007b8cc788b3`; distinct from scope UUID |
| Operator role assignment | Directory principal and role UUID matched by operator |
| Browser application | `estudio-polymind-streamlit-dev`; AzureADMyOrg; Web |
| Browser client ID | `a43f5479-4cbd-45a0-86e0-9c658e77d133`; Streamlit client, not API audience |
| Browser application object ID | `11fb33b1-2149-4e74-a6ac-5f7295147607`; directory management object |
| Browser service principal object ID | `6a15b03a-f544-43eb-b486-d29a52ddfa8b`; type Application; enabled |
| Browser flow flags | Implicit access tokens false; implicit ID tokens false; fallback public client false |
| Registered and accepted Web redirect | `https://polymind.test:9443/oauth2callback` |
| Required resource permission | API client ID above; scope UUID above; type Scope; exactly required API permission |
| Persisted delegated grant | Client SP `6a15b03a-f544-43eb-b486-d29a52ddfa8b` → resource SP `046ce5b0-897c-4289-ad86-e403ac6b6e20` |
| Consent | Principal; `access_as_user`; independently read back by operator; tenant-wide consent NOT GRANTED |
| Consent principal / operator directory object ID | `3c1c6ec4-ac53-485d-af7c-ff015f8fbe57`; **not** API access-token subject |
| API access-token `sub` | UNKNOWN; no operational enrollment tuple can yet be completed |

The confidential credential's description is `polymind-streamlit-phase19b-dev`, key ID
`7319515e-0342-4c8e-aacb-b5c663c8cda9`, count 1, start `2026-11-26T08:24:50.834Z`,
expiration `2027-05-25T07:24:50.834Z`. Metadata verification is operator-reported PASS.
The key ID is an identifier, **never the secret value**. The value was not supplied to Codex.
Its reported location is operator-controlled personal storage outside Git; intended custodian
is the project operator. Possession, encryption, access restrictions and operational validity
were not independently verified. Preserve the existing principal-only consent; no additional
Graph scopes, tenant-wide consent or credential changes are needed for this preparation.

## 5. Exact non-operational native Streamlit reference

This is a non-secret reference with deliberately non-operational credential placeholders.
Never mount this block or the portable template as runtime credentials.

```toml
[auth]
redirect_uri = "https://polymind.test:9443/oauth2callback"
server_metadata_url = "https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/v2.0/.well-known/openid-configuration"
client_id = "a43f5479-4cbd-45a0-86e0-9c658e77d133"
client_secret = "<OPERATOR_SUPPLIED_SECRET>"
cookie_secret = "<INDEPENDENT_RANDOM_SECRET>"
expose_tokens = ["access"]

[auth.client_kwargs]
scope = "openid api://5aa70f9d-9f9e-4b5b-972b-698d4d68105e/access_as_user"
```

Installed interpreter is `/home/home/.pyenv/versions/estudio_polymind/bin/python`, Python 3.10,
with Streamlit **1.58.0**. Inspected `streamlit/auth_util.py`:
`generate_default_provider_section` forwards client ID/secret, discovery URL, kwargs and
token exposure; `get_redirect_uri` accepts the exact callback; `validate_auth_credentials`
accepts these default-provider fields; `get_expose_tokens_config` accepts `["access"]`;
`get_signing_secret` reads `auth.cookie_secret`. Verification injects in-memory synthetic
secrets, never the ambient Streamlit secrets singleton's files.

Both Chat and Documents call unnamed `st.login()`, so the unnamed default provider is
appropriate. The installed Starlette auth-route factory preserves an explicitly supplied scope instead of adding its default email/profile scopes. Both require `st.user.is_logged_in` and `st.user.tokens.get('access')`, then
forward Bearer credentials to the API. Missing tokens prevent useful application access.
Reauthentication/logout remains native. No replacement authentication framework is introduced.
The portable [template](../../../deployment/phase19/streamlit.secrets.example.toml) retains
tenant/browser/API placeholders; environment-specific values have a single reference here.

## 6. API identity, authorization and consistency

The API configuration remains a separate reviewed object, not native browser secrets:

```json
{
  "token_profile": "entra_v2",
  "tenant_id": "afabeaf8-0fea-42c9-afb4-7e5c07eff3f3",
  "issuer": "https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/v2.0",
  "jwks_url": "https://login.microsoftonline.com/afabeaf8-0fea-42c9-afb4-7e5c07eff3f3/discovery/v2.0/keys",
  "audience": "5aa70f9d-9f9e-4b5b-972b-698d4d68105e"
}
```

`OIDCSettings` validates this exact mapping offline. `OIDCVerifier` fixes the delegated
`access_as_user` scope and exact `PolyMind.L1Operator` role set, verifies RS256, issuer, scalar
audience, matching tenant, version 2.0, user identity and integer lifetime claims. The role
maps to publication management, not tenant administration or model execution authority.
Neither browser client ID nor `api://...` is a valid substitute for the configured API audience.
Application/service-principal object IDs are management/consent identifiers, not this audience.

Runtime manifest enrollment and both workflows bind **`[issuer, tenant UUID, API access-token sub]`**.
Security authority owner IDs derive from that verified tuple. The operator's directory `oid`,
ID-token `sub`, email, display name and service-principal UUID cannot supply the missing
API token subject. No operational manifest, placeholder subject or production enrollment
was created. Login, enrollment, independent execution approval and financial authorization
remain separate requirements. Seven SQLite authorities, Redis/Chroma, provider neutrality,
Chat/RAG, Documents and the SSE → provider tokens → NDJSON boundary are unchanged.

Before provisioning, operator compares the actual private gateway configuration's
`PHASE19_ORIGIN` to `https://polymind.test:9443`, then native redirect and the reported Entra
Web URI to that origin plus `/oauth2callback`. Also compare API configuration to the mapping
above and role/scope requirements. Do not print environment dumps, TOML mappings or secrets.
The procedure below checks native fields exactly; **automatic deployed cross-file validation
does not exist**. Actual gateway/API files and certificate SAN remain an operator preflight.
Keep `DNS:polymind.test`, Windows `127.0.0.1 polymind.test`, Windows and remote loopback 9443,
and VM `127.0.0.1:9443:9443`; public exposure is prohibited.

## 7. Complete operator-executable local preparation procedure

**Run independently after review, outside the Codex session.** Keep the existing client secret
in its protected personal storage until the private prompt requires it. No persistent
intermediate plaintext credential file is needed. Use an interactive WSL Linux terminal,
outside the repository, with recording/debug tracing disabled. Do not use `/mnt/c`, a
synchronized directory, notebook, chat, command argument or environment variable for secrets.

Save the following non-secret Python block as `prepare_streamlit.py` in an operator-selected
directory outside Git. Activate the existing `estudio_polymind` environment. Python 3.11+
uses standard-library `tomllib`; the installed Python 3.10 uses the **already installed**
`toml` parser. No installation or application utility is required. If no parser exists, stop.
The fixed destination is `~/.config/polymind/phase19/streamlit.toml`; another location requires
an independently reviewed adaptation retaining all checks. The script refuses unsafe existing
directories rather than changing unrelated permissions. It may create only the missing
`.config/polymind/phase19` chain beneath an existing safe Linux home.

```python
"""Operator-only local preparation; no network, dotenv, or runtime startup."""
import getpass
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import warnings

try:
    import tomllib as toml_reader
except ImportError:  # Existing estudio_polymind Python 3.10 dependency; no install.
    try:
        import toml as toml_reader
    except ImportError:
        raise SystemExit("FAIL: approved TOML parser unavailable; nothing prepared.") from None

ORIGIN = "https://polymind.test:9443"
TENANT = "afabeaf8-0fea-42c9-afb4-7e5c07eff3f3"
API = "5aa70f9d-9f9e-4b5b-972b-698d4d68105e"
BROWSER = "a43f5479-4cbd-45a0-86e0-9c658e77d133"
KEY_ID = "7319515e-0342-4c8e-aacb-b5c663c8cda9"
NAME = "streamlit.toml"
EXPECTED = {
    "redirect_uri": ORIGIN + "/oauth2callback",
    "server_metadata_url": f"https://login.microsoftonline.com/{TENANT}/v2.0/.well-known/openid-configuration",
    "client_id": BROWSER,
    "expose_tokens": ["access"],
    "client_kwargs": {"scope": f"openid api://{API}/access_as_user"},
}


def require(condition):
    if not condition:
        raise ValueError("Preflight rejected")


def valid_secret(value):
    require(type(value) is str and 1 <= len(value) <= 16384 and bool(value.strip()))
    require(not any(marker in value.upper() for marker in (
        "<", ">", "REPLACE", "OPERATOR_SUPPLIED", "INDEPENDENT_RANDOM",
        "SUPPLIED_PRIVATELY", "PLACEHOLDER")))
    require(value != KEY_ID)
    value.encode("utf-8", errors="strict")


def quote(value):
    # JSON basic-string escapes are TOML-compatible; escape DEL explicitly.
    # Literal Unicode avoids JSON surrogate-pair escapes, forbidden by TOML.
    return json.dumps(value, ensure_ascii=False).replace(chr(127), "\\u007f")


def validate(text):
    data = toml_reader.loads(text)
    require(set(data) == {"auth"})
    auth = data["auth"]
    require(set(auth) == set(EXPECTED) | {"client_secret", "cookie_secret"})
    require(all(auth[key] == value for key, value in EXPECTED.items()))
    valid_secret(auth["client_secret"])
    valid_secret(auth["cookie_secret"])
    require(re.fullmatch(r"[A-Za-z0-9_-]{64}", auth["cookie_secret"]) is not None)
    require(auth["client_secret"] != auth["cookie_secret"])
    return data


def render(client):
    valid_secret(client)
    cookie = secrets.token_urlsafe(48)  # Independent 384-bit CSPRNG input.
    require(cookie != client)
    values = {**EXPECTED, "client_secret": client, "cookie_secret": cookie}
    text = "[auth]\n" + "\n".join(
        f"{key} = {json.dumps(value) if isinstance(value, list) else quote(value)}"
        for key, value in values.items() if key != "client_kwargs"
    ) + "\n\n[auth.client_kwargs]\nscope = " + quote(EXPECTED["client_kwargs"]["scope"]) + "\n"
    validate(text)
    return text


def private_directory(create):
    home = Path.home()
    require(home.is_absolute() and ".." not in home.parts)
    require(home != Path("/") and not home.is_relative_to("/mnt"))
    destination = home / ".config" / "polymind" / "phase19"
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for index, part in enumerate(destination.parts[1:], 1):
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except FileNotFoundError:
                require(create and index >= len(home.parts))
                os.mkdir(part, mode=0o700, dir_fd=fd)
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
            info = os.fstat(fd)
            require(info.st_uid in {0, os.getuid()} and stat.S_IMODE(info.st_mode) & 0o022 == 0)
            # Refuse a destination inside any Git worktree (including .git files).
            try:
                os.stat(".git", dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise ValueError("Repository destination rejected")
        info = os.fstat(fd)
        require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700)
        return fd
    except BaseException:
        os.close(fd)
        raise


def private_prompt():
    # Explicit controlling terminal plus warning-as-error prevents getpass fallback.
    with open("/dev/tty", "w") as tty, warnings.catch_warnings():
        require(tty.isatty())
        warnings.simplefilter("error", getpass.GetPassWarning)
        return getpass.getpass("Existing Entra client secret (hidden): ", stream=tty)


def metadata(fd):
    info = os.fstat(fd)
    require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid())
    require(stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1)
    require(0 < info.st_size <= 65536)
    return info


def verify_fd(fd):
    info = metadata(fd)
    os.lseek(fd, 0, os.SEEK_SET)
    with os.fdopen(os.dup(fd), "r", encoding="utf-8") as stream:
        text = stream.read(65537)
    require(len(text.encode("utf-8")) == info.st_size)
    validate(text)
    return info


def run(verify=False):
    os.umask(0o077)
    directory = private_directory(create=not verify)
    fd = None
    created = None
    completed = False
    try:
        if verify:
            fd = os.open(NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        else:
            # Existing files, directories and dangling links all fail before prompting.
            try:
                os.stat(NAME, dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise FileExistsError("Destination exists")
            text = render(private_prompt())
            fd = os.open(NAME, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=directory)
            created = os.fstat(fd)
            require(stat.S_IMODE(created.st_mode) == 0o600)
            with os.fdopen(os.dup(fd), "w", encoding="utf-8") as stream:
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
        info = verify_fd(fd)
        os.fsync(directory)
        completed = True
        print(f"PASS: configuration verified; uid={info.st_uid} gid={info.st_gid} "
              f"mode=0600 regular=yes links=1 bytes={info.st_size}")
    finally:
        # Remove only our newly created inode after a failed write/verification.
        try:
            if created is not None and not completed:
                current = os.stat(NAME, dir_fd=directory, follow_symlinks=False)
                if (current.st_dev, current.st_ino) == (created.st_dev, created.st_ino):
                    os.unlink(NAME, dir_fd=directory)
        finally:
            if fd is not None:
                os.close(fd)
            os.close(directory)


if __name__ == "__main__":
    try:
        require(sys.argv[1:] in ([], ["--verify"]))
        run(verify=sys.argv[1:] == ["--verify"])
    except (Exception, KeyboardInterrupt):
        print("FAIL: private configuration preflight failed; no credential details displayed.", file=sys.stderr)
        sys.exit(1)
```

From the directory containing that non-secret script:

```bash
python prepare_streamlit.py
python prepare_streamlit.py --verify
```

Supply the actual existing client-secret **value** only to the hidden terminal prompt. A
missing controlling terminal or getpass echo fallback causes failure. A failure prints a
fixed sanitized category; do not enable traceback/debug output around credentials. Existing
destinations, including dangling links, refuse before prompting. `O_EXCL|O_NOFOLLOW`, mode
0600 at initial creation, directory descriptors, non-writable trusted ancestry, exact 0700
destination directory, owner/regular/single-link checks and post-write parsing protect the
local path. Successful verification prints only outcome and file metadata. Do not print or
copy the TOML to inspect it. The validation checks exact non-secret identifiers/scope,
access-token exposure and unresolved credential placeholders; it cannot prove Entra validity.

## 8. Cookie-secret independence and lifetime

The preparation procedure calls `secrets.token_urlsafe(48)` once per new file, independently
of the supplied client secret and all other credentials. This is 48 random bytes (384 bits),
encoded as 64 URL-safe characters. It is neither derived from identifiers nor reused from
Foundry, TLS, execution signing or development credentials. The script additionally refuses
equality with the client secret. Only synthetic instances were generated in this task.

Preserve the prepared cookie secret across ordinary restarts. `--verify` never regenerates
it. Changing it can invalidate existing browser authentication cookies; coordinate deliberate
rotation and reauthentication. Do not regenerate a whole file merely because the application
restarts. Client-secret renewal is a separately reviewed operation, not part of this procedure.

## 9. Plaintext, optional encrypted staging and custody

A populated `streamlit.toml` contains **two plaintext secrets**, even with mode 0600. Linux
permissions restrict ordinary users; they do not encrypt disk/backup content or exclude host
administrators. Actual custody/encryption is unverified. The existing Entra secret may remain
in the operator's encrypted personal storage until needed; this report does not inspect it.
Use protected encrypted staging when preparation precedes deployment. GPG is already present
at `/usr/bin/gpg`; no encryption software was installed or personal GPG files inspected.

Optional operator-only Bash sequence, after successful preparation and from the script's
directory; run individual steps and stop on failure. Keep the passphrase in existing protected
custody, independently of this file. GPG prompts through its normal pinentry, never an argument
or environment variable. Restrictive umask and shell noclobber apply to output from creation:

```bash
umask 077
set -o noclobber
phase19_private="$HOME/.config/polymind/phase19/streamlit.toml"
gpg --symmetric --cipher-algo AES256 --output - "$phase19_private" > "$phase19_private.gpg"
# Check decryptability AND equality without displaying either plaintext stream:
set -o pipefail
gpg --decrypt --output - "$phase19_private.gpg" | cmp -s "$phase19_private" -
```

Only after both commands succeed and protected passphrase/backup custody is confirmed, remove
the exact redundant plaintext path if it is not actively needed. A failed encryption may leave
an incomplete new encrypted file: retain the valid plaintext and remove only that known failed
artifact after inspection of metadata. Do not overwrite a previous encrypted file or delete
unknown artifacts. Ordinary deletion does **not** guarantee secure erasure on SSDs, journals,
snapshots or backups; avoid creating extra plaintext copies in the first place.

To restore later in the same verified 0700 directory (check ancestry with the Python procedure's
directory checks first), require the plaintext path to be absent; keep noclobber and umask 077:

```bash
gpg --decrypt --output - "$phase19_private.gpg" > "$phase19_private"
python prepare_streamlit.py --verify
```

If decryption or verification fails, do not transfer/start anything; remove only this newly
created failed plaintext file after confirming its identity. Never overwrite an existing valid
runtime configuration. Avoid editors' swap/backup files, clipboard history, shell tracing,
screen recording and broad temporary directories. The direct SSH stream below needs no
remote plaintext staging copy. These GPG steps are proposed, not operationally executed or
proof that the operator's existing storage is encrypted.

## 10. Future Azure VM provisioning — prepared, not executed

Requires a separately authorized Azure maintenance session with UI/gateway stopped, verified
VM state/identity, approved Tailscale
OpenSSH route and host key, and reviewed maintenance privileges. No target or fingerprint is
invented here. Use the operator's independently verified SSH config alias/user-host; do not
reuse a historical operator-device IP as the VM address. Enforce `StrictHostKeyChecking=yes`.
No connection, transfer, decryption or host mutation occurred during this task.

Actual Compose contract inspected:

| Property | Required value |
|---|---|
| Host source variable | `PHASE19_STREAMLIT_SECRET` |
| Example/required final host path | `/etc/polymind/secrets/streamlit.toml` |
| Container destination | `/tmp/.streamlit/secrets.toml` |
| Bind flags | `read_only: true`, `bind.create_host_path: false` |
| UI working directory / identity | `/tmp`; `10001:10001` |
| Final host file | regular, no symlink, single link, UID:GID `10001:10001`, exact 0600 |
| Host traversal policy for this procedure | `/etc/polymind` and `secrets`: root:10001, 0710 |

Host traversal must permit UID 10001 to reach the file for host-side checks; container loading
uses the read-only bind under `/tmp`. Streamlit does not enforce the repository private_path
policy, so operator checks remain mandatory. Missing bind sources still fail instead of
being created. Preserve the reviewed Azure-pinned Compose and image identities, five services,
loopback gateway, data disk, seven authorities and provider/execution mounts.

Future operator transfer procedure: first run local `--verify`, compare actual origin/API
metadata to section 6 and accepted redirect, verify host key/alias independently, then use the
following non-secret Python driver beside `prepare_streamlit.py`. It streams the one private
file through SSH stdin, with no secret in arguments/environment or remote temporary path.
It requires already approved **noninteractive `sudo -n`** for the reviewed receiver. If that
maintenance path is unavailable, stop and use a separately reviewed operator maintenance
channel; do not weaken sudo policy or disable host-key checks. The remote Python must already
provide `tomllib` or `toml`; failure does not justify installing dependencies automatically.

```python
import os
from pathlib import Path
import re
import shlex
import subprocess
import prepare_streamlit as p

receiver = r'''
d = None
f = None
created = None
done = False
try:
    require(os.geteuid() == 0)
    os.umask(0o077)
    payload = sys.stdin.buffer.read(65537)
    require(0 < len(payload) <= 65536)
    validate(payload.decode("utf-8"))
    d = os.open("/etc", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    info = os.fstat(d)
    require(info.st_uid == 0 and stat.S_IMODE(info.st_mode) & 0o022 == 0)
    for part in ("polymind", "secrets"):
        fresh = False
        try:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=d)
        except FileNotFoundError:
            os.mkdir(part, 0o700, dir_fd=d)
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=d)
            fresh = True
        os.close(d)
        d = child
        if fresh:
            os.fchown(d, 0, 10001)
            os.fchmod(d, 0o710)
        info = os.fstat(d)
        require(info.st_uid == 0 and info.st_gid == 10001 and stat.S_IMODE(info.st_mode) == 0o710)
    f = os.open(NAME, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=d)
    created = os.fstat(f)
    require(created.st_uid == 0 and stat.S_IMODE(created.st_mode) == 0o600)
    with os.fdopen(os.dup(f), "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    verify_fd(f)  # Parses back the root-owned new file before ownership handoff.
    os.fchown(f, 10001, 10001)
    info = os.fstat(f)
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1)
    require(info.st_uid == info.st_gid == 10001 and stat.S_IMODE(info.st_mode) == 0o600)
    os.fsync(f)
    os.fsync(d)
    done = True
    print("PASS: uid=10001 gid=10001 mode=0600 regular=yes links=1 configuration=verified")
except (Exception, KeyboardInterrupt):
    print("FAIL: installation preflight failed; no credential details displayed.", file=sys.stderr)
finally:
    try:
        if created is not None and not done:
            current = os.stat(NAME, dir_fd=d, follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (created.st_dev, created.st_ino):
                os.unlink(NAME, dir_fd=d)
    finally:
        if f is not None: os.close(f)
        if d is not None: os.close(d)
if not done:
    sys.exit(1)
'''

directory = None
source = None
try:
    target = input("Independently verified SSH alias/user-host: ")
    p.require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.@-]*", target) is not None)
    directory = p.private_directory(create=False)
    source = os.open(p.NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    p.verify_fd(source)
    os.lseek(source, 0, os.SEEK_SET)
    # Send reviewed non-secret code as the remote command; secret bytes only on stdin.
    code = Path("prepare_streamlit.py").read_text().split('if __name__ == "__main__":')[0] + receiver
    result = subprocess.run([
        "ssh", "-T", "-o", "StrictHostKeyChecking=yes", "-o", "BatchMode=yes",
        target, "sudo -n python3 -c " + shlex.quote(code)
    ], stdin=source, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    expected = b"PASS: uid=10001 gid=10001 mode=0600 regular=yes links=1 configuration=verified\n"
    p.require(result.returncode == 0 and result.stdout == expected)
    print(expected.decode(), end="")
except (Exception, KeyboardInterrupt):
    print("FAIL: transfer unavailable or unverified; reconcile remote metadata before retrying.")
    raise SystemExit(1) from None
finally:
    if source is not None: os.close(source)
    if directory is not None: os.close(directory)
```

The receiver refuses existing files and unsafe existing directories; it does not replace a
previous runtime configuration. Newly created parent directories remain after failure; inspect
metadata and reconcile them deliberately. A lost connection can leave an installed file even
when the client reports failure: verify metadata/contents via the same protected, sanitized
validator before any retry, never overwrite blindly. Do not grant blanket sudo solely to run
this example. Review the exact code/maintenance authorization before future execution.

After transfer, operator verifies metadata without content (`sudo stat -c '%F %u:%g %a %h'
/etc/polymind/secrets/streamlit.toml`), checks every ancestor without following symlinks and
confirms UID 10001 traversal/readability through the approved maintenance channel. Validate
the installed file again under UID 10001 using the same `validate` mapping and read-only
descriptor checks; print only PASS/FAIL and metadata. Compare actual external Compose source,
origin and API identity settings without dumping their content. This is a future preflight,
not claimed runtime enforcement or executed Azure acceptance. Keep the encrypted recovery
copy and stable cookie secret; remove redundant local plaintext only when no longer needed.
No service startup, authority initialization or inference is part of this transfer procedure.

## 11. Offline verification

Final executed focused command (through the temporary whitelist runner):

```bash
python /tmp/polymind-oidc-preparation-20261126/run_checks.py \
  tests/unit/test_phase19_oidc_template.py tests/unit/test_phase19_tls.py \
  tests/unit/test_security_entra.py tests/unit/test_phase19_chat_view.py \
  tests/unit/test_documents_view.py tests/unit/test_ui_api_client.py \
  tests/unit/test_phase19_deployment.py tests/integration/test_phase19_operator.py \
  /tmp/polymind-oidc-preparation-20261126/test_procedure.py
```

The runner invokes `python -m pytest -q -p network_guard` with those exact paths and:

```text
--junitxml=/tmp/polymind-oidc-preparation-20261126/focused.xml
--basetemp=/tmp/polymind-oidc-preparation-20261126/focused-state
-o cache_dir=/tmp/polymind-oidc-preparation-20261126/focused-cache
```

It supplies only PATH/HOME/LANG/LC_ALL from the caller, PYTHONPATH pointing to the temporary
helper directory and repository, HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1,
PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1 and TOKENIZERS_PARALLELISM=false. Application
configuration and provider credential environment variables are excluded. Existing
`tests/conftest.py` disables implicit dotenv before collection. The temporary pytest plugin
denies non-loopback socket connect/connect_ex and external DNS, permitting loopback/Unix
transport only. API tests also inject fake JWKS/providers and synthetic tokens. The PTY child
only exercises getpass; it does not import application settings or perform network work.
This is test isolation, not a newly implemented production firewall.

Final result: **exit 0; 225 passed, 4 warnings, 18.78s**. JUnit: **225 tests, 0 failures,
0 errors, 0 skipped**. This consists of **192 existing repository tests and 33 synthetic
procedure checks**. The four existing `NotAppKeyWarning` occurrences come from
`ui/tls_gateway.py:18` in the two parameterized selected-origin TLS tests and the two
existing gateway deployment tests. No warning was suppressed.

Synthetic checks include exact report-script byte equality; native reference equality and
installed default-provider credentials/redirect/exposure/cookie helpers; parser round trip
with quotes, backslashes, newline, tab, DEL and Unicode; invalid/placeholder/key-ID/surrogate
rejection; independent token_urlsafe(48) generation; creation mode checked before any write;
existing-file refusal before prompting; symlink/dangling link/directory/FIFO/public mode/
hard-link refusal; parent symlink/public directory/writable ancestor/repository/Windows-path
rejection; metadata-only output; failure cleanup; and exact API settings validation.
The real pseudoterminal check confirms terminal ECHO is disabled before sending **synthetic**
input and that input never appears in captured output. Missing terminal and getpass fallback
are also tested. No test creates an operational cookie or operational destination.

The fake HOME lives only under pytest temporary state. A narrowly scoped test adapter models
`/tmp`'s root-owned sticky ancestor as a trusted ancestor so the real directory-walking code
can run there; the operator script itself has no such exception and rejects writable
ancestors. No actual home configuration or personal secret is read or written. Temporary test
helpers are not a new application module or a second deployed configuration source.

Intermediate outcomes are retained explicitly: first socket-dependent sandbox attempt was
interrupted, **exit 130**, without a completed test result; execution-approved run then passed
**223 tests, 4 warnings in 18.79s**, exit 0. Adding exact-report and real-terminal checks exposed
one real procedure bug: `open('/dev/tty', 'r+')` raises `io.UnsupportedOperation` because the
terminal is not seekable. That run had **224 passed, 1 failed, 4 warnings in 28.34s**, exit 1.
A synthetic-only PTY diagnostic exited 0 and identified that exception. The report procedure
was corrected to use a write-only terminal stream for getpass, preserving warning-as-error
fallback refusal; the final 225-test run above passed. No security assertion was weakened.
The failure log/XML are retained separately beside final focused.log/XML in the temporary
evidence directory. Initial missing-file search paths were corrected by inspecting actual
`deployment/phase19/runtime.py`; they were not assumed to exist.

Additional checks:

```bash
PYTHONPYCACHEPREFIX=/tmp/polymind-oidc-preparation-20261126/bytecode python -m compileall -q .
git diff --check
python /tmp/polymind-oidc-preparation-20261126/precommit_review.py
```

Compilation and whitespace checks exited 0. Separate pre-commit checker outcome is recorded
in section 13; it also compiles the embedded Python blocks without running them and checks
new-file whitespace/local links. No configured lint/formatter was found, and none was installed.

Full regression is **NOT_REQUIRED**: changes are documentation/operator procedures only;
no application runtime, dependency, shared API contract, Compose or executable image behavior
changed. The prior **3,329-test full pass** remains historical evidence; it was not repeated.
No Docker build, Compose startup/config rerun, five-service container workload, GPG operational
round trip, Azure transfer, TLS issuance/trust installation, real discovery/JWKS/token request,
browser authentication, live inference, runtime enrollment or authority initialization ran.
Unchanged Compose is covered by source inspection and existing focused contracts, without
reading real environment files. GPG/remote procedures are reviewed future instructions,
not executed operational checks or new acceptance evidence.

## 12. Engineering self-review

Reviewed identity distinctions, native helper behavior, both UI consumers, API scope/role
enforcement and exact enrollment tuple. No runtime change is required. The configuration uses
only `openid` and the API scope; operator-specific consent stays intact. No Graph/refresh-token
scope is introduced. No automatic cross-file or operational-validity check is claimed.

Reviewed prompt failure, TOML quote/control/Unicode escaping, independent randomness, descriptor
closure, restricted ancestry, no-follow/exclusive initial creation, ownership/modes, bounded
readback and safe failed-file removal. The script never echoes errors containing input. It
uses existing TOML parsing on Python 3.10 and no new dependency. Validation is local and does
not establish credential validity. Plaintext/encrypted copy lifetime and cookie continuity are
explicit. Future transfer requires privileged maintenance and refuses ambiguous inputs; its
unexecuted host/network aspects remain pending. No reusable application utility was added.

## 13. Separate pre-commit review

Separate review inspects all **seven candidates**: five existing documentation changes and
this new prompt/report. Complete tracked diffs and both new records were reviewed separately.
The temporary checker validates exact candidate names, unchanged HEAD/empty index, new-file
whitespace, embedded Python compilation, shell syntax without execution, local link targets/
anchors and byte equality of all existing tracked historical prompts/reports. No runtime,
Compose, dependency, portable-template, Dockerfile or authority file changed.

Reviewed for real credential payloads, private keys/JWTs, real env files, machine-specific
operational targets, debug statements, temporary/generated artifacts, stale TODOs, unrelated
changes, broken documentation and API drift. Only supplied non-secret directory identifiers,
explicit credential placeholders and synthetic test values occur. Pattern checks supplement
manual review; they do not establish actual operator credential custody. No accidental
credential staging or generated operational file was found. No staging or commit occurred.

The first checker invocation stopped on intentionally unfilled report assembly markers before
final report completion (exit 1); the markers were populated and the checker was rerun. This
was an unfinished-document check, not a security bypass. Final checker exited 0: **7 scoped documentation files, 9 local links, 2 embedded Python
blocks compiled, 213 historical records byte-identical, HEAD/index preserved; no payload or
artifact findings**. Final Git commands are part of the handoff evidence. The review also clarified README is a non-executable
Docker build-context input; changed prose does not require replacing the existing image.

## 14. Remaining operational blockers

Actual client-secret possession, encryption/access restriction and operational validity are
not independently verified. Neither operational cookie secret nor populated TOML exists as
a result of this task. Azure configuration has not been provisioned. The VM is
operator-reported deallocated; activation, remote connection and runtime initialization were
not authorized. Actual CA/leaf provisioning, validity/custody/revocation decisions, Windows
resolution/trust and private SSH/browser acceptance remain outstanding from the HTTPS task.

Real authentication/token claim validation, especially API access-token `sub`, is separately
blocked. Runtime enrollment cannot be inferred from directory IDs. Session/logout/expiry,
JWKS egress, deployed TLS/configuration and identity acceptance require an authorized live step.
Source/privacy/semantic review, provider capability/endpoint, finance/shared quota/obligations,
fresh independent signed execution permission, capacity/recovery/cost and deallocation gates
remain unchanged. This task grants no resource expenditure or model execution authority.

## 15. Final readiness matrix and acceptance gates

| Area | Status | Evidence / limit |
|---|---|---|
| Entra API settings and role assignment | OPERATOR_REPORTED_PASS | Matching supplied UUIDs, v2, scope and enabled User role |
| Browser registration / Web redirect acceptance | OPERATOR_REPORTED_PASS | Exact tenant/client/accepted callback supplied |
| Browser service principal | OPERATOR_REPORTED_PASS | Enabled Application SP supplied |
| Delegated permission | OPERATOR_REPORTED_PASS | API resource / scope UUID / Scope type match |
| Operator-specific persisted consent | OPERATOR_REPORTED_PASS | Principal grant for supplied operator, no tenant-wide consent |
| Confidential credential metadata | OPERATOR_REPORTED_PASS | One key, description/start/expiry supplied; value unseen |
| Native Streamlit exact configuration | PASS | Installed 1.58.0 helpers + synthetic readback |
| API identity configuration compatibility | PASS | Existing settings/verifier and regression; operational file unprovisioned |
| Secure provisioning / cookie generation design | PASS | Exact local report procedure exercised synthetically |
| Actual credential custody / encryption | GAP | Location operator-reported; no independent inspection |
| Azure installation / operational TLS | PENDING | Future procedure only; no VM access |
| Runtime subject enrollment | BLOCKED | Actual API access-token sub unknown |
| Actual browser authentication | BLOCKED | Not authorized or executed |

Acceptance gates 1–8 are PASS **within offline preparation/procedure scope**: baseline preserved;
Entra evidence reconciled without upgrading its provenance; exact OIDC/native contract matched;
procedure tested synthetically; secret-custody design passed with actual custody separately GAP;
applicable offline checks passed; reproducible documentation/current addenda completed; security
and Git boundaries preserved. This is not a PASS for an unexecuted operational check.

## 16. Recommended next operator action

Review this report and the embedded procedure, then independently prepare and verify the private
configuration outside Codex using the existing client-secret value. If not immediately required,
retain protected encrypted staging without redundant plaintext. Do not paste credentials back
into chat. No new Entra registration/consent or credential creation is needed on supplied evidence.
Later Azure provisioning and actual authentication require their separate authorization and
outstanding TLS/identity/runtime inputs. Stop here; Phase 19C has not begun.

## 17. Git handoff and application image

All final Git commands below exited 0. HEAD remains the baseline SHA and the index is empty.
`git diff --stat` / `--name-status` describe tracked files only; new records are listed separately.

```text
$ git status --short --branch
## master...origin/master
 M README.md
 M docs/evaluation/phase_19_deployment_architecture.md
 M docs/evaluation/phase_19_implementation_plan.md
 M docs/operations/phase_19_vm.md
 M docs/security/entra_v2.md
?? docs/codex/prompts/phase_19b_streamlit_oidc_configuration_preparation.md
?? docs/codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md
exit 0
```

```text
$ git diff --stat
 README.md                                          | 21 +++++++-
 .../evaluation/phase_19_deployment_architecture.md | 19 +++++++
 docs/evaluation/phase_19_implementation_plan.md    | 22 ++++++++
 docs/operations/phase_19_vm.md                     | 61 ++++++++++++++++++++++
 docs/security/entra_v2.md                          | 19 +++++++
 5 files changed, 141 insertions(+), 1 deletion(-)
exit 0
```

```text
$ git diff --name-status
M	README.md
M	docs/evaluation/phase_19_deployment_architecture.md
M	docs/evaluation/phase_19_implementation_plan.md
M	docs/operations/phase_19_vm.md
M	docs/security/entra_v2.md
exit 0
```

```text
$ git diff --check
(no output)
exit 0
```

```text
$ git diff --cached --name-only
(no output)
exit 0
```

- `docs/codex/prompts/phase_19b_streamlit_oidc_configuration_preparation.md` (new, untracked; inspected separately).
- `docs/codex/reports/phase_19b_streamlit_oidc_configuration_preparation.md` (new, untracked; inspected separately).

Proposed operator checkpoint message:

```text
docs: prepare Phase 19B Streamlit OIDC configuration and secure credential provisioning
```

No application runtime or executable image payload changed. README is in the Docker build context, so a new build would package updated prose; the existing image retains its prior README. This does not require an application rebuild. Existing external native secrets mount supplies
the new values; **application image rebuild required: NO**. Preserve previously reviewed image
and Azure-pinned Compose provenance. No commit or push occurred; operator review is next.

## 18. Final status contract

```text
PHASE19B_STREAMLIT_OIDC_PREPARATION: PASS

ENTRA_API_CONFIGURATION: OPERATOR_REPORTED_PASS
ENTRA_API_ROLE_ASSIGNMENT: OPERATOR_REPORTED_PASS
ENTRA_BROWSER_REGISTRATION: OPERATOR_REPORTED_PASS
ENTRA_REDIRECT_URI_ACCEPTANCE: OPERATOR_REPORTED_PASS
ENTRA_BROWSER_SERVICE_PRINCIPAL: OPERATOR_REPORTED_PASS
ENTRA_DELEGATED_PERMISSION: OPERATOR_REPORTED_PASS
ENTRA_OPERATOR_SPECIFIC_CONSENT: OPERATOR_REPORTED_PASS
ENTRA_CLIENT_CREDENTIAL_METADATA: OPERATOR_REPORTED_PASS

EXACT_STREAMLIT_OIDC_CONFIGURATION: PASS
API_IDENTITY_CONFIGURATION_COMPATIBILITY: PASS
SECURE_PROVISIONING_PROCEDURE: PASS
COOKIE_SECRET_GENERATION_PROCEDURE: PASS
SYNTHETIC_PROVISIONING_VERIFICATION: PASS
ACTUAL_CLIENT_SECRET_ACCESSED_BY_CODEX: NO
ACTUAL_CREDENTIAL_ENCRYPTION_VERIFIED: NO
OPERATIONAL_COOKIE_SECRET_CREATED: NO
OPERATIONAL_STREAMLIT_TOML_CREATED: NO
AZURE_STREAMLIT_CONFIGURATION_PROVISIONED: NO
REAL_ENTRA_AUTHENTICATION: BLOCKED
RUNTIME_SUBJECT_ENROLLMENT: BLOCKED

APPLICATION_RUNTIME_CODE_CHANGED: NO
APPLICATION_IMAGE_REBUILD_REQUIRED: NO
FOCUSED_REGRESSION_VERIFICATION: PASS
FULL_REGRESSION_VERIFICATION: NOT_REQUIRED
DOCUMENTATION_RECONCILIATION: PASS
PRE_COMMIT_REVIEW: PASS

AZURE_VM_ACTIVATED: NO
ENTRA_MUTATIONS: NO
REAL_INFERENCE_CALLS: 0
PUBLIC_EXPOSURE_INTRODUCED: NO
GIT_STAGED: NO
GIT_COMMITTED: NO
GIT_PUSHED: NO

PHASE19A_STATUS: COMPLETE
PHASE19B_STATUS: ACTIVE
PHASE19C_STATUS: NOT_STARTED

NEXT_ACTION_READINESS: READY_FOR_OPERATOR_REVIEW
```
