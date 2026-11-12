"""Untrusted stage-proposal/1 selections; deterministic application identities.

Aliases are local vocabulary, never authority. Reconstruct tables from the exact
immutable request on every decode. Durable provenance is checked by receipts.py.
"""

import json
from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from documents.digestion.codec import encode
from documents.digestion.models import DigestionError, StageResult
from documents.jobs.models import fingerprint
from documents.models import stable_id

VERSION: Literal["stage-proposal/1"] = "stage-proposal/1"
DECODER: Literal["stage-decoder/1"] = "stage-decoder/1"
MAX_SOURCES = 256


@dataclass(frozen=True)
class References:
    request_sha256: str
    evidence: tuple[UUID, ...]
    children: tuple[tuple[UUID, UUID], ...]

    def payload(self):
        return {
            "version": DECODER,
            "request_sha256": self.request_sha256,
            "evidence": [str(e) for e in self.evidence],
            "children": [[str(s), str(c)] for s, c in self.children],
        }

    @property
    def digest(self):
        return fingerprint(self.payload())


def references(request):
    evidence = tuple(
        sorted(
            {p.evidence_id() for p in request.source_data}
            | {
                e
                for child in request.children
                for claim in child.result.claims
                for e in (*claim.evidence_ids, *claim.contradicting_evidence_ids)
            },
            key=str,
        )
    )
    children = tuple(
        (child.result.stage_id, c.claim_id)
        for child in request.children
        for c in child.result.claims
    )
    if len(evidence) > MAX_SOURCES or len(children) != len(set(children)):
        raise DigestionError("synthesis_limit_exceeded")
    return References(fingerprint(request.model_dump(mode="json")), evidence, children)


def keys(prefix, values):
    return [f"{prefix}{i + 1}" for i in range(len(values))]


def schema(table=None):
    """Only the existing strict converter subset; bounds are enforced locally."""
    value = StageResult.model_json_schema()
    props = value["properties"]
    del props["stage_id"], props["kind"]
    props["schema_version"] = {"type": "string", "const": VERSION}
    props["request_binding"] = (
        {"type": "string"}
        if table is None
        else {"type": "string", "enum": [table.digest]}
    )
    claim = value["$defs"]["Claim"]["properties"]
    del claim["claim_id"], claim["originating_stage"]
    del value["$defs"]["ClaimLink"]
    for definition, fields in (
        (
            claim,
            (
                ("evidence_ids", "evidence_refs"),
                ("contradicting_evidence_ids", "contradicting_evidence_refs"),
                ("lineage", "child_refs"),
            ),
        ),
        (
            value["$defs"]["Qualification"]["properties"],
            (("evidence_ids", "evidence_refs"),),
        ),
    ):
        for old, new in fields:
            definition[new] = definition.pop(old)
            definition[new]["items"] = {
                "$ref": "#/$defs/"
                + ("ChildReference" if new == "child_refs" else "SourceEvidence")
            }
    for name, prefix, values in (
        ("SourceEvidence", "E", () if table is None else table.evidence),
        ("ChildReference", "C", () if table is None else table.children),
    ):
        allowed = keys(prefix, values)
        branches = [
            {"type": "string", "enum": allowed[i : i + 128]}
            for i in range(0, len(allowed), 128)
        ]
        value["$defs"][name] = (
            {"type": "string"}
            if table is None
            else {"type": "null"}
            if not branches
            else branches[0]
            if len(branches) == 1
            else {"anyOf": branches}
        )

    def require(node):
        if isinstance(node, dict):
            if "properties" in node:
                node["required"] = list(node["properties"])
            for child in node.values():
                require(child)
        elif isinstance(node, list):
            for child in node:
                require(child)

    require(value)
    return value


def _fail(category="inference_contract_error"):
    raise DigestionError(category)


def _object(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        _fail()


def _array(value, bound):
    if type(value) is not list:
        _fail()
    if len(value) > bound:
        _fail("synthesis_limit_exceeded")


def _text(value, bound):
    if type(value) is not str or not 1 <= len(value) <= bound:
        _fail()


def construct(raw, request, table):
    """Strict wire validation, then canonical construction; G2 remains separate.

    This pure function checks consistency, not provider origin. Only the fenced
    capture/receipt path may turn its result into an accepted v10 checkpoint.
    """
    from documents.digestion.planning import check_request

    check_request(request)
    if type(raw) is not bytes or len(raw) > request.profile.response_byte_limit:
        _fail("synthesis_limit_exceeded")
    if table != references(request):
        _fail("incompatible_checkpoint")
    if request.profile.prompt_profile != "managed-prompt/10":
        _fail("incompatible_checkpoint")

    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                _fail()
            out[key] = value
        return out

    try:
        data = json.loads(
            raw, object_pairs_hook=unique, parse_constant=lambda _: _fail()
        )
    except DigestionError:
        raise
    except (ValueError, TypeError, RecursionError, UnicodeError):
        _fail()
    _object(
        data,
        (
            "schema_version",
            "request_binding",
            "outcome",
            "claims",
            "open_questions",
            "limitations",
        ),
    )
    if data["schema_version"] != VERSION or data["request_binding"] != table.digest:
        _fail("incompatible_checkpoint")
    if type(data["outcome"]) is not str or data["outcome"] not in (
        "analyzed",
        "unavailable",
    ):
        _fail()
    profile = request.profile
    _array(data["claims"], profile.max_claims)
    for field in ("open_questions", "limitations"):
        _array(data[field], profile.max_annotations)
        for text in data[field]:
            _text(text, 4096)

    def resolve(value, prefix, values):
        # Resource bounds are distinct from membership. In particular an E1
        # under empty authority, or a duplicate under singleton authority, is
        # an evidence rejection rather than a misleading response-size error.
        _array(
            value,
            MAX_SOURCES
            if prefix == "E"
            else request.profile.max_fan_in * request.profile.max_claims,
        )
        allowed = dict(zip(keys(prefix, values), values, strict=True))
        if any(type(k) is not str or k not in allowed for k in value):
            _fail("evidence_validation_failed")
        if len(value) != len(set(value)):
            _fail("evidence_validation_failed")
        return [allowed[k] for k in value]

    claims = []
    for position, item in enumerate(data["claims"]):
        _object(
            item,
            (
                "text",
                "kind",
                "status",
                "subject",
                "stance",
                "evidence_refs",
                "contradicting_evidence_refs",
                "qualifications",
                "child_refs",
            ),
        )
        _text(item["text"], profile.max_claim_characters)
        for field, allowed in (
            ("kind", ("fact", "unknown", "unsupported", "commentary", "structural")),
            ("status", ("supported", "unknown", "unsupported")),
            ("stance", ("affirmed", "denied", "unknown")),
        ):
            if type(item[field]) is not str or item[field] not in allowed:
                _fail()
        if item["subject"] is not None:
            _text(item["subject"], 128)
        _array(item["qualifications"], profile.max_annotations)
        qualifications = []
        for q in item["qualifications"]:
            _object(q, ("text", "evidence_refs"))
            _text(q["text"], profile.max_claim_characters)
            qualifications.append(
                {
                    "text": q["text"],
                    "evidence_ids": resolve(q["evidence_refs"], "E", table.evidence),
                }
            )
        pairs = resolve(item["child_refs"], "C", table.children)
        claims.append(
            dict(
                claim_id=stable_id(str(request.stage_id), str(position)),
                originating_stage=request.stage_id,
                **{k: item[k] for k in ("text", "kind", "status", "subject", "stance")},
                evidence_ids=resolve(item["evidence_refs"], "E", table.evidence),
                contradicting_evidence_ids=resolve(
                    item["contradicting_evidence_refs"], "E", table.evidence
                ),
                qualifications=qualifications,
                lineage=[{"stage_id": s, "claim_id": c} for s, c in pairs],
            )
        )
    try:
        result = StageResult(
            stage_id=request.stage_id,
            kind=request.stage,
            outcome=data["outcome"],
            claims=claims,
            open_questions=data["open_questions"],
            limitations=data["limitations"],
        )
        canonical = encode(result)
    except (ValueError, TypeError):
        _fail()
    if len(canonical) > profile.max_result_characters:
        _fail("synthesis_limit_exceeded")
    return canonical
