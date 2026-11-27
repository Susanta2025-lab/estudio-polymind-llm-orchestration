# Phase 19B local identity bootstrap — operator runbook

27 November 2026. **Future operator procedure; actual Entra authentication is NOT_AUTHORIZED
by the implementation task.** Phase 19A COMPLETE; 19B ACTIVE; 19C NOT_STARTED.
Review the [engineering report](../codex/reports/phase_19b_local_identity_bootstrap_utility.md)
and obtain separate authorization before operational provisioning or `serve`.

This maintenance utility acquires native Streamlit browser authentication and independently
verifies only the API access token. It exports sensitive enrollment-candidate evidence, never
enrollment, source approval, execution permission or an executable manifest. Production startup,
Compose, ordinary Chat/Documents and existing development launchers do not invoke it.

## 1. Prerequisites and local acceptance

Use the reviewed working tree based on `b5f16926100ca1712f85c39f5fc579fbad88829d` (or the later
operator-reviewed checkpoint) and the existing Python 3.10 `estudio_polymind` environment with
pinned Streamlit 1.58.0/Authlib and installed project dependencies. Check the report's final
regression evidence. No installation, image build, Azure, SSH, provider or production state is
needed. Do not run the utility from an unreviewed or writable-by-others checkout.

Confirm both Windows and WSL ports 9443 and WSL port 8503 are free. In WSL, use
`ss -ltn '( sport = :9443 or sport = :8503 )'`; in PowerShell use
`Get-NetTCPConnection -State Listen -LocalPort 9443 -ErrorAction SilentlyContinue`.
A listener must be understood/stopped by its owner before continuing. Do not launch the Azure
SSH tunnel while bootstrap runs. The launcher reserves WSL 127.0.0.1:9443 without reuse-port
before child startup; conflicts fail closed. Windows and WSL can have distinct listener
namespaces: the Windows check is also mandatory. Never use forwarding to a public address.

The current host reports WSL NAT mode; a synthetic Windows TCP client reached a temporary WSL
127.0.0.1 listener during offline verification. This observation does not guarantee future
WSL/Windows configurations or browser TLS acceptance. Confirm Windows still resolves
`polymind.test` to 127.0.0.1, with the already approved mapping, and the correct dedicated public
CA remains trusted by the current Windows user. Make no hosts/firewall/trust changes as part
of login troubleshooting. Failure means stop and review networking, not bind to 0.0.0.0.

The leaf certificate must have SAN DNS:polymind.test, serverAuth EKU, valid dates, matching
private key, and a chain to the approved public CA. Review with offline OpenSSL hostname/chain
and current CRL checks using **public certificates only**. The launcher checks leaf date/SAN/EKU
and key matching; it does not prove Windows root trust, chain revocation or CRL freshness.
Minimum TLS is 1.2. Retain the existing renewal deadlines and obtain explicit acceptance of
manual revocation limitations; issuing a CRL does not ensure browser enforcement. Never move
or read the CA private key/complete CA archive. Do not replace certificates to force a pass.

Approve a new empty evidence directory on protected WSL Linux storage outside Git, /mnt,
shared temporary storage and production paths. Session/evidence directories must be separate,
0700 and operator-owned; files 0600, single-link, regular and operator-owned. Ancestors must
be root/operator-owned, without group/other write or symlinks. The utility rejects /tmp and
Windows-mounted paths. Same-UID code/root remains trusted: native execution is not an OS
filesystem sandbox. Use a dedicated local account/session if stronger separation is required;
keep unrelated programs and browser extensions out of the trusted session.

## 2. Prepare private session inputs — operator only

The operator, outside Codex, supplies existing encrypted OIDC configuration and the designated
server leaf certificate/key exports. Do not access CA workspaces, SSH keys, provider credentials,
production storage or real `.env` files. Preserve original encrypted custody and the independently
generated **production cookie secret unchanged**.

Use a new ephemeral cookie secret for this bootstrap. The same origin and native cookie names
(`_streamlit_user`, `_streamlit_user_tokens`, chunk variants and OAuth session cookie) can otherwise
carry bootstrap authentication into production. A different signing secret invalidates cookie
reuse between the applications but does not remove old cookies. Use a dedicated private browser
window with every other private window closed, clear polymind.test site data before starting,
and do not open a production tab or another bootstrap tab during the session.

The following commands and script are prepared for the **future operator session only**. Paths
are entered privately; none of the values is a credential passed on a command line. The script
reads decrypted TOML through stdin, replaces only its in-memory cookie value, and creates only
the temporary native TOML and designated leaf/key copies. It never writes the restored
production TOML. Its plaintext copies are justified solely for Streamlit/OpenSSL consumption
in this bounded session; remove them after shutdown. No secure-erasure guarantee follows.

From the reviewed repository, in the approved environment:

```bash
umask 077
BOOTSTRAP_SESSION="$(mktemp -d "$HOME/.polymind-bootstrap.XXXXXXXX")"
BOOTSTRAP_EVIDENCE="$(mktemp -d "$HOME/.polymind-identity-evidence.XXXXXXXX")"
mkdir -m 700 -- "$BOOTSTRAP_SESSION/.streamlit"
read -r -p 'Encrypted native OIDC file (absolute path): ' ENCRYPTED_CONFIG
read -r -p 'Designated server certificate export (absolute path): ' LEAF_CERT
read -r -p 'Designated server key export (absolute path): ' LEAF_KEY
```

Save this reviewed code as `prepare_session.py` inside a **separate private 0700 preparation
directory**, mode 0600, outside the repository. Set `PREPARE_SCRIPT` to that absolute path.
The session itself must contain exactly `.streamlit`, `tls.crt`, `tls.key`; do not save the
script there. Do not alter or decrypt the original encrypted artifact into the repository.

```python
# Operator-only preparation, never executed with operational inputs by Codex.
import os
import secrets
import sys
from pathlib import Path
import toml
from deployment.phase19.identity_bootstrap.core import validate_auth
from deployment.phase19.identity_bootstrap.files import directory, read_private, regular

os.umask(0o077)
created = []
try:
    root = Path(sys.argv[1])
    with directory(root), directory(root / '.streamlit'):
        if {p.name for p in root.iterdir()} != {'.streamlit'}:
            raise ValueError()
        if any((root / '.streamlit').iterdir()):
            raise ValueError()
    restored = sys.stdin.buffer.read(65537)
    if len(restored) > 65536:
        raise ValueError()
    values = toml.loads(restored.decode('utf-8'))
    production_cookie = values['auth']['cookie_secret']
    values['auth']['cookie_secret'] = secrets.token_urlsafe(48)
    if values['auth']['cookie_secret'] == production_cookie:
        raise ValueError()
    validate_auth(values)
    inputs = [(root / '.streamlit/secrets.toml', toml.dumps(values).encode()),
              (root / 'tls.crt', read_private(Path(sys.argv[2]))),
              (root / 'tls.key', read_private(Path(sys.argv[3])))]
    for path, data in inputs:
        with directory(path.parent) as parent:
            fd = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=parent)
            try:
                info = os.fstat(fd)
                created.append((path, info.st_dev, info.st_ino))
                regular(fd)
                with os.fdopen(os.dup(fd), 'wb') as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.fsync(parent)
            finally:
                os.close(fd)
    print('PRIVATE_SESSION_PREPARATION: PASS; PRODUCTION_COOKIE_CHANGED: NO')
except BaseException:
    # Delete only this attempt's newly created files, never original inputs.
    for path, device, inode in created:
        with directory(path.parent) as parent:
            current = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (device, inode):
                os.unlink(path.name, dir_fd=parent)
    raise SystemExit('Private preparation failed; no input details displayed.') from None
```

Invoke with the reviewed repository on PYTHONPATH so the external script imports the utility:

```bash
set -o pipefail
export PYTHONPATH="$PWD"
gpg --decrypt -- "$ENCRYPTED_CONFIG" | python "$PREPARE_SCRIPT" \
  "$BOOTSTRAP_SESSION" "$LEAF_CERT" "$LEAF_KEY"
python -m deployment.phase19.identity_bootstrap check "$BOOTSTRAP_SESSION" "$BOOTSTRAP_EVIDENCE"
```

GPG passphrases remain in the operator's protected terminal/pinentry flow, never arguments or
logs. Do not use shell tracing. A pipeline/preflight error means stop and reconcile exactly
which new files exist; never overwrite, loosen permissions or regenerate the Entra secret.
The approved non-secret fields must exactly match `identity_bootstrap/core.py`: existing tenant,
browser client, bare API UUID audience, tenant v2 issuer/JWKS, `openid` plus delegated API
`access_as_user`, exact `PolyMind.L1Operator`, exact HTTPS callback and `expose_tokens=["access"]`.
The generic repository template remains inert. Extra providers, Graph scopes, other token
exposure, custom OAuth endpoints, placeholders and weak cookie values fail preflight.
`check` parses only supplied private inputs and checks loopback port availability; it does not
perform discovery, JWKS requests, authentication or production initialization.

## 3. Controlled startup — separately authorized future session

Review the authorization window and host-level egress controls first. The utility is not a
firewall. Its controlled child environment excludes inherited provider credentials, proxy
settings, Streamlit overrides and application configuration; HOME/cwd point only to the private
session, with one native secrets source. Application code never reads `.env` or production state.
It does not stop other same-user processes from accessing home files or the internet.

Utility connectivity requires tenant-specific Entra discovery, discovered authorization/token
metadata, authorization-code token exchange and the fixed tenant JWKS URL on HTTPS. The browser
requires local `https://polymind.test:9443`, Entra authorization/login and applicable tenant/MFA
resources. Review any additional browser destinations separately; do not invent an exhaustive
MFA/CDN allowlist. No Graph, Azure management or provider endpoint is required. TLS verification
stays enabled for every outbound HTTPS client. Use host/network egress controls or a reviewed
isolated workstation profile if destination-level restrictions are required. Credentials being
absent is not proof of destination enforcement. No strict operational egress firewall was
established by offline implementation.

Only after independent authorization:

```bash
python -m deployment.phase19.identity_bootstrap serve \
  "$BOOTSTRAP_SESSION" "$BOOTSTRAP_EVIDENCE" --authorize-entra
```

The flag acknowledges external authorization; it cannot grant it. The launcher holds the
callback endpoint, starts native Streamlit at 127.0.0.1:8503 and exposes only the existing exact
Host/Origin HTTPS proxy at 127.0.0.1:9443. No automatic restart. Startup has a 30-second limit;
after readiness the session lasts at most 900 seconds, followed by bounded gateway/child cleanup.
Ctrl-C/SIGTERM requests cleanup. SIGKILL, OS crash or power failure cannot guarantee cleanup:
inspect only these scoped processes/listeners before any retry. Child stdout/stderr and access
logs are discarded to avoid auth diagnostics/codes entering ordinary logs. Terminal status is
sanitized; investigate failures through private configuration/metadata review, never token dumps.

## 4. Authenticate and independently verify

In the dedicated Windows private browser window, visit **https://polymind.test:9443**. Require
normal certificate/hostname trust with no exception. Confirm exact origin, select Sign in and
use the already approved Entra account/registration. Native Streamlit/Authlib owns state, nonce,
code exchange and conditional S256 PKCE when provider metadata advertises support. Do not supply
state/nonce manually. Do not change consent, permissions, registrations or credentials while
troubleshooting. Stop on unexpected consent/account/certificate prompts.

The bootstrap selects only `st.user.tokens.get("access")`. `is_logged_in` alone is insufficient.
Existing OIDCVerifier verifies signature, trusted RS256 key/header, exact tenant issuer/audience,
v2, delegated scope, exact role set, valid integer token times and nonempty API `sub`.
Bootstrap additionally requires signed `azp` to equal the approved browser client. It reads that
claim only after this exact token passes production verification. ID-token subjects, `oid`,
email and display names never determine enrollment. Canonical IDs are the verified Principal's
existing `polymind-identity/1/tenant` and `polymind-identity/1/owner` values, matching production.
No key discovery runs until a token actually needs verification.

Expected UI: `IDENTITY_VERIFICATION: PASS; CANONICAL_OWNER_DERIVATION: PASS`. No subject or
claims are displayed. Invalid/absent/expired/wrong-client tokens fail closed, with no production
fallback. Native login does not refresh API-token validity automatically; reauthentication
requires deliberate logout and another separately authorized login if the token expires.

## 5. Explicit candidate export and provenance

Check the explicit export authorization box, then select Export protected candidate. Fresh
verification runs immediately before the exclusive write. The destination was approved at
launch; browsers cannot choose a different path. One `enrollment-candidate.json` is permitted
per evidence directory, across reruns, repeated clicks, tabs and concurrent sessions.

Expected status: `PROTECTED_EVIDENCE_EXPORT: PASS; EXECUTION_AUTHORIZED: NO`. File schema is
`phase19b-enrollment-candidate/1`, purpose `phase19b_identity_bootstrap`; only issuer, tenant UUID,
API sub, canonical tenant/owner, API audience, verification/expiry UTC times and
`execution_authorized=false` are included. No token, cookie, secret, complete JWT payload or
unnecessary directory identity is exported. Keep it as sensitive operator-owned evidence.
Do not paste the subject, token, or candidate into ChatGPT/Codex/Git or external JWT websites.

A temporary exclusive `.enrollment-candidate.pending` is fsynced then atomically hard-linked to
the final name without overwrite. Cleanup removes only the created pending inode; the final
file has one link, mode 0600. Normal write errors/interruption do not publish partial JSON.
An uncatchable crash can leave a pending file, or a complete final file plus pending link; a
post-publication sync error can report failure despite complete publication. Do not retry or
use such evidence automatically: trusted operator reconciliation must inspect exact inodes,
complete schema, ownership/modes/link count and session provenance. Preserve uncertainty; never
delete an unrelated file or reuse a nonempty directory. A file hash establishes integrity
comparison only, not authenticity, independent approval or current token validity.

## 6. Close the session

Select Log out and clear display. Streamlit 1.58 signs cookies, including token data; cookies
are **not encrypted**. The native user/token cookies may persist 30 days and split into chunks;
the gateway adds Secure, while native cookies use HttpOnly/SameSite=Lax. OAuth middleware has a
separate signed session cookie. Same-origin cookies can be reused across tabs. Logout clears
local auth cookies/new session; it does not prove provider-token revocation or logout of every
existing tab. It may use provider logout when configured; do not equate that with revocation.

Clear all polymind.test site data (including cookie chunks/OAuth session state), close every
private browser window/tab, and stop the launcher with Ctrl-C. Verify **both Windows 9443 and
WSL 9443/8503** are released using step 1. Do not start the future Azure tunnel until then.
If forced termination occurred, identify and stop only the scoped bootstrap worker before
cleaning inputs; never use a broad process-kill command.

After confirming process exit, remove only the three newly provisioned session files,
`.streamlit` directory, empty session directory and the operator's temporary preparation script
using their exact recorded paths. Inspect metadata first; do not recursively delete a guessed
path. Retain the evidence directory/candidate at 0700/0600. Keep original encrypted OIDC/PKI
recovery custody, original production cookie secret and original designated leaf/key exports
unchanged. Ordinary unlinking does not promise secure deletion, browser/profile storage erasure
or guaranteed process-memory erasure. Preserve encrypted backups independently and review
recovery/revocation deadlines.

Confirm no production configuration/authority/source manifest was created or altered and no
provider calls occurred. The utility creates no authority/financial records; bootstrap status
cannot attest to activity by unrelated processes. Record the authorized window, reviewed
revision, operator custody, verification/export/cleanup outcome and any uncertainty privately.

## 7. Subsequent enrollment review

A trusted operator reviews candidate provenance through a protected local channel: reviewed
code/revision and device, controlled session/custody, approved Entra browser/API trust, successful
fresh verification at export, clean closure and protected file history. The artifact is unsigned
and can be edited by its owner; it is not an independently signed identity/execution authority.
Its token-expiry timestamp records the acquisition evidence, not a renewable enrollment grant.
Require another authorized authentication if freshness/provenance is insufficient.

Only a separately authorized enrollment/provisioning session may map the candidate's exact
`[issuer, tenant UUID, API access-token sub]` into reviewed RuntimeManifest enrollment and
owner-bound source approvals. Recompute production stable IDs locally and compare. Review all
remaining source/privacy/semantic/session/provider/finance/quota/obligation and independent
execution gates before production initialization. No utility command consumes the candidate
as an executable manifest or registers a principal. Gate A operational closure remains BLOCKED.
