"""Prewritten substantive outputs pass real wire/G2/receipt/publication boundaries.

This establishes acceptance and labelled fixture properties, never model quality.
"""

import json
from functools import partial
from hashlib import sha256

import pytest

from documents.digestion import managed
from documents.digestion.codec import read
from documents.digestion.models import Checkpoint
from documents.digestion.receipts import DecodingReceipt, ProposalRecord
from documents.digestion.validation import validate_result
from documents.digestion.wire import construct, references
from documents.jobs.models import canonical
from tests.performance import fixtures, foundry_preflight
from tests.reducer_semantic_fixtures import DOMAINS, rubric_checks, valve_case


@pytest.mark.parametrize("domain", ["valves", "science", "regulation"])
def test_authored_content_through_complete_workflow(tmp_path, monkeypatch, domain):
    monkeypatch.setattr(
        managed,
        "StageProfile",
        partial(managed.StageProfile, template_version="managed-prompt/11"),
    )
    if domain == "valves":
        raw, manifest, case = valve_case()
        assert (
            sha256(raw).hexdigest()
            == "1be99e19a56040fb55c74682a19f874d4d4573f18d9f52a9a7ae19c8158ea92d"
        )
        monkeypatch.setattr(foundry_preflight, "pdf", lambda pages: (raw, manifest))
        leaves = [f"Pre-operation inspection covers unit {i:04d}." for i in range(1, 5)]
        # Preserve the actual supported valve lists at the leaf as well.
        import re

        leaves = [
            text
            + " Valves: "
            + ", ".join(re.findall(r"inspect valve (\d{4})", source))
            + "."
            for text, source in zip(leaves, case["pages"], strict=True)
        ]
    else:
        case = DOMAINS[domain]
        monkeypatch.setattr(
            fixtures,
            "page_lines",
            lambda page, count, rng: [f"Section {page}", case["pages"][page - 1]],
        )
        leaves = case["pages"]
    qualifications = {
        "valves": {i: "Inspection is required before operation." for i in range(4)},
        "science": {
            2: "Field safety was not tested.",
            3: "Effects at other temperatures are not established.",
        },
        "regulation": {
            0: "Draft guidance is not yet binding; it takes effect in 2027.",
            3: "Emergency shutdown may precede notice.",
        },
    }[domain]
    observed = []
    original_analyze = managed.ManagedDigestionHandler.analyze

    def analyze(handler, request, *args):
        observed.append((handler, request, args[0]))
        return original_analyze(handler, request, *args)

    monkeypatch.setattr(managed.ManagedDigestionHandler, "analyze", analyze)

    class HTTP(foundry_preflight.OfflineHTTP):
        def response(self, sent, result, stage):
            if stage == "question":
                data = json.loads(sent["messages"][1]["content"])
                evidence = data["ORIGINAL_SOURCE_EVIDENCE"][0]
                value = {
                    "answer": evidence["excerpt"],
                    "evidence_status": "available",
                    "citation_ids": [evidence["citation_id"]],
                }
            else:
                request = observed[-1][1]
                table = references(request)
                texts = leaves if stage == "chunk" else case["summary"]
                claims = []
                for i, text in enumerate(texts):
                    evidence = (
                        [
                            f"E{table.evidence.index(request.source_data[i].evidence_id()) + 1}"
                        ]
                        if stage == "chunk"
                        else []
                    )
                    # Each valve synthesis covers its corresponding units.
                    # At root, select those structural claims, never leaf links.
                    child_keys = [f"C{j + 1}" for j in range(len(table.children))]
                    if stage != "chunk" and len(texts) > 1:
                        assert len(child_keys) % len(texts) == 0
                        width = len(child_keys) // len(texts)
                        child_keys = child_keys[i * width : (i + 1) * width]
                    claims.append(
                        {
                            "text": text,
                            "kind": "fact",
                            "status": "supported",
                            "stance": "unknown",
                            "subject": None,
                            "evidence_refs": evidence,
                            "contradicting_evidence_refs": [],
                            "qualifications": [
                                {"text": qualifications[i], "evidence_refs": evidence}
                            ]
                            if stage == "chunk" and i in qualifications
                            else [],
                            "child_refs": [] if stage == "chunk" else child_keys,
                        }
                    )
                value = {
                    "schema_version": "stage-proposal/1",
                    "request_binding": table.digest,
                    "outcome": "analyzed",
                    "claims": claims,
                    "open_questions": [],
                    "limitations": [],
                }
            return super().response(sent, json.dumps(value), stage)

    monkeypatch.setattr(foundry_preflight, "OfflineHTTP", HTTP)
    result = foundry_preflight.execute(tmp_path, "L1")
    assert result["job_state"] == "COMPLETED" and result["digest_status"] == "COMPLETE"
    assert result["calls"] == 4 and result["billable_calls"] == 0
    assert result["questions"]["status"] == "COMPLETE"
    assert "publication" in result
    from documents.digestion.workflow import load_digest
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.storage import LocalObjectStore

    handler, _, old_job = observed[-1]
    scope = old_job.admission.scope
    store = LocalObjectStore(tmp_path / "objects")
    ledger = SQLiteJobLedger(handler.ledger.settings)
    job = ledger.get_job(scope, old_job.job_id)
    plan, index = handler._load(store, scope, job.admission.profile.max_artifact_bytes)
    assert plan.profile.prompt_profile == "managed-prompt/11"
    steps = {s.spec.unit_id: s for s in ledger.steps(scope, job.job_id)}
    handler._verify_proposals(store, job, steps, plan)
    digest = load_digest(ledger, store, scope, job.job_id)
    assert digest.coverage.fraction == 1 and digest.qualifications
    accepted = [s for s in steps.values() if len(s.manifest) == 3]
    assert len(accepted) == 3
    limit = job.admission.profile.max_artifact_bytes
    for step in accepted:
        cp = read(store, scope, step.manifest[0], Checkpoint, limit)
        receipt = read(store, scope, step.manifest[1], DecodingReceipt, limit)
        record = read(store, scope, step.manifest[2], ProposalRecord, limit)
        assert (
            receipt.canonical_sha256
            and record.raw_sha256 == sha256(record.raw.encode()).hexdigest()
        )
        if cp.result.kind == "analysis":
            continue
        text = " ".join(c.text for c in cp.result.claims)
        assert all(rubric_checks(text, case).values())
        assert not all(
            rubric_checks(
                "Processed four child claims in wrappers C1 and C2.", case
            ).values()
        )
        assert not rubric_checks(text + " " + case["unsupported"], case)[
            "known_unsupported_conclusion_absent"
        ]
        # Valid references do not prove semantic quality. The same G2-valid
        # selections with metadata-dominated prose fail this fixture's rubric.
        request = next(r for _, r, _ in observed if r.stage_id == cp.result.stage_id)
        metadata = json.loads(record.raw)
        metadata["claims"][0]["text"] = (
            "Processed four child claims in wrappers C1 and C2."
        )
        decoded = construct(canonical(metadata).encode(), request, references(request))
        assert validate_result(decoded, request, index)
        assert not rubric_checks(metadata["claims"][0]["text"], case)[
            "standalone_content"
        ]
