"""Read-only worst-case forecast on the EXISTING financial/provider authorities.

No capacity is reserved by this report. Admission still rechecks actual state.
Future planned calls are simulated as known full-reservation usage, never refunds.
"""

from datetime import datetime, timezone
from decimal import Decimal, localcontext

from documents.pilot.models import PilotError
from security.models import Action


def forecast(ledger, admission, authority, principal, calls, *, now=None):
    authority.authorize(principal, Action.PUBLICATION_MANAGE)
    if not calls or len(calls) > 18:
        raise PilotError("pilot_limit")
    _, owner_limits, tenant_limits = ledger.policy.select(principal.scope)
    now = ledger.clock() if now is None else now
    with ledger.transaction() as db:
        ledger._current_policy(db)
        rows = [
            dict(r)
            for r in db.execute(
                "SELECT * FROM reservations WHERE tenant=?",
                (str(principal.scope.tenant),),
            )
        ]
    # UNKNOWN and unfinished current obligations are a hard pilot stop.
    if any(r["state"] not in {"SETTLED", "RELEASED"} for r in rows):
        raise PilotError("pilot_reconciliation_required")
    with admission._transaction() as db:
        provider_rows = [
            dict(r)
            for r in db.execute(
                "SELECT * FROM inference_calls WHERE quota=?", (admission.quota_key,)
            )
        ]
    if any(r["active"] for r in provider_rows):
        raise PilotError("pilot_reconciliation_required")
    previous = now - 1
    for call in calls:
        if set(call) != {"at", "input", "output", "provider", "model", "workload"}:
            raise PilotError()
        at, inp, out = call["at"], call["input"], call["output"]
        if (
            type(at) not in {int, float}
            or not now <= at
            or at <= previous
            or type(inp) is not int
            or type(out) is not int
            or inp < 0
            or out <= 0
            or call["workload"] not in {"INTERACTIVE", "DOCUMENT_BACKGROUND"}
        ):
            raise PilotError()
        previous = at
        price = ledger.catalog.price(call["provider"], call["model"])
        date = datetime.fromtimestamp(at, timezone.utc)
        if ledger.catalog.effective_date > date.strftime("%Y-%m-%d"):
            raise PilotError()
        day = date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        month = date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        ).timestamp()
        for limits, selected in (
            (tenant_limits, rows),
            (
                owner_limits,
                [r for r in rows if r["owner"] == str(principal.scope.owner)],
            ),
        ):
            with localcontext() as ctx:
                ctx.prec = 60
                spent = [r for r in selected if r["state"] != "RELEASED"]
                if (
                    sum(r["created"] > at - limits.window_seconds for r in selected)
                    >= limits.requests_per_window
                    or inp + out > limits.reserved_tokens
                    or sum(
                        r["actual_input"] + r["actual_output"]
                        for r in spent
                        if r["created"] >= day
                    )
                    + inp
                    + out
                    > limits.daily_tokens
                    or sum(
                        r["actual_input"] + r["actual_output"]
                        for r in spent
                        if r["created"] >= month
                    )
                    + inp
                    + out
                    > limits.monthly_tokens
                    or sum(
                        (
                            Decimal(r["actual_cost"])
                            for r in spent
                            if r["created"] >= month
                        ),
                        Decimal(0),
                    )
                    + price.cost(inp, out)
                    > limits.monthly_cost
                ):
                    raise PilotError("pilot_limit")
        policy = admission.policy
        recent = [r for r in provider_rows if r["started"] > at - 60]
        bg = call["workload"] == "DOCUMENT_BACKGROUND"
        docs = [r for r in recent if r["workload"] == "DOCUMENT_BACKGROUND"]
        if (
            len(recent) >= policy.rpm
            or sum(r["estimated_input"] + r["reserved_output"] for r in recent)
            + inp
            + out
            > policy.tpm
            or (
                bg
                and (
                    len(docs) >= policy.rpm - policy.interactive_rpm
                    or sum(r["estimated_input"] + r["reserved_output"] for r in docs)
                    + inp
                    + out
                    > policy.tpm - policy.interactive_tpm
                )
            )
        ):
            raise PilotError("pilot_limit")
        rows.append(
            {
                "owner": str(principal.scope.owner),
                "state": "SETTLED",
                "created": at,
                "actual_input": inp,
                "actual_output": out,
                "actual_cost": str(price.cost(inp, out)),
            }
        )
        provider_rows.append(
            {
                "started": at,
                "estimated_input": inp,
                "reserved_output": out,
                "workload": call["workload"],
            }
        )
    return {
        "status": "FORECAST_FITS_NOT_AUTHORIZATION",
        "calls": len(calls),
        "policy": ledger.policy.version,
        "catalog": ledger.catalog.version,
        "request_window": "created > at-window_seconds",
        "token_windows": "UTC day/month",
        "unknown_obligations": 0,
    }
