"""Conservative bounded inventory: observations, never a physical erasure claim."""

import json
from uuid import UUID

from documents.models import ObjectRef

CLASSES = (
    "source_objects",
    "extracted_text",
    "jobs",
    "step_artifacts",
    "provider_receipts",
    "checkpoints",
    "digests",
    "publication_generations",
    "vectors",
    "sparse_retrieval",
    "temporary_processing",
    "session_presentation",
    "feedback",
    "audit",
    "usage_reservations",
    "backups",
    "upstream_provider_copies",
    "conversation_memory",
    "participant_metadata",
)


def inventory(pilot, principal, session):
    row, tracked, operations = pilot.control.inventory(
        session, principal.scope.identity()
    )
    approval = row["approval"]
    with pilot.control.transaction() as db:
        access_revoked = (
            bool(pilot.control._config(db)["stopped"])
            or row["state"] != "OPEN"
            or approval is None
            or approval.expires_at.timestamp() <= pilot.clock()
            or row["source"].expires_at.timestamp() <= pilot.clock()
        )
    retention_until = (
        approval.metadata_retention_until.isoformat()
        if approval
        else row["data"]["metadata_retention_until"]
    )
    retention_reference = (
        approval.retention_reference if approval else row["data"]["retention_reference"]
    )
    mode = approval.mode if approval else row["data"]["original_mode"]
    scope = principal.scope
    observations, refs = [], {r.key: (r, state) for r, state in tracked}
    job_id = row["data"].get("job")
    manifests = set()
    job_state = "NOT_ADMITTED"
    jobs_verified = True
    try:
        if job_id:
            job = pilot.jobs.get_job(scope, UUID(job_id))
            job_state = job.state.value
            for step in pilot.jobs.steps(scope, UUID(job_id)):
                for ref in step.manifest:
                    refs.setdefault(ref.key, (ref, "ACCEPTED_MANIFEST"))
                    manifests.add(ref.key)
            # Include write intents that failed between register/write/commit.
            with pilot.jobs._transaction(write=False) as (db, _):
                for r in db.execute(
                    "SELECT i.ref FROM object_intents i JOIN job_steps s ON s.step_id=i.step_id WHERE s.job_id=?",
                    (job_id,),
                ):
                    ref = ObjectRef.model_validate_json(r[0])
                    refs.setdefault(ref.key, (ref, "WRITE_INTENT"))
    except Exception:  # noqa: BLE001 - report unverified adapter state, never erase on error
        jobs_verified = False
        observations.append({"class": "jobs", "state": "UNKNOWN_UNVERIFIED"})
    for ref, intent in refs.values():
        try:
            exists = (
                pilot.objects.inspect(scope, ref, max_bytes=max(ref.byte_size, 1))
                == ref
            )
        except Exception:  # noqa: BLE001 - missing/corrupt/unavailable are all unverified
            exists = False
        kind = "source_objects" if ref.kind == "source" else "step_artifacts"
        if exists and ref.kind == "artifact":
            try:
                schema = json.loads(
                    pilot.objects.read(scope, ref, max_bytes=ref.byte_size)
                ).get("schema_version")
                kind = {
                    "extraction/1": "extracted_text",
                    "document-digest/1": "digests",
                    "synthesis-checkpoint/1": "checkpoints",
                    "stage-provider-record/1": "provider_receipts",
                    "stage-decoding-receipt/1": "provider_receipts",
                    "publication/1": "publication_generations",
                }.get(schema, kind)
            except Exception:  # noqa: BLE001 - unknown content cannot establish an artifact class
                kind = "step_artifacts"
        observations.append(
            {
                "class": kind,
                "reference": str(ref.key),
                "sha256": ref.sha256,
                "state": "LOGICALLY_REVOKED_RETAINED"
                if exists and row["state"] != "OPEN"
                else "RETAINED_BY_POLICY"
                if exists
                else "UNKNOWN_UNVERIFIED",
                "write": intent,
                "accepted": ref.key in manifests,
            }
        )
    generations = []
    try:
        for generation in pilot.publication.authority.inventory():
            manifest = pilot.publication.manifest(generation, compatible=False)
            if any(
                d.document_id == row["source"].document_id for d in manifest.documents
            ):
                generations.append(str(generation))
                observations.append(
                    {
                        "class": "publication_generations",
                        "reference": str(generation),
                        "state": "RETAINED_BY_POLICY",
                        "records": len(manifest.records),
                    }
                )
        physical = pilot.publication.vectors.list_documents()
        observations.append(
            {
                "class": "vectors",
                "state": "RETAINED_BY_POLICY",
                "records": sum(
                    r.metadata.get("generation") in generations for r in physical
                ),
            }
        )
    except Exception:  # noqa: BLE001 - inventory interruption is an explicit residual
        observations.append(
            {"class": "publication_generations", "state": "UNKNOWN_UNVERIFIED"}
        )
    try:
        with pilot.governance.transaction() as db:
            pilot.governance._current_policy(db)
            rows = [
                dict(r)
                for r in db.execute(
                    "SELECT * FROM reservations WHERE owner=? AND tenant=?",
                    (str(scope.owner), str(scope.tenant)),
                )
            ]
        steps = {o["id"] for o in operations}
        usage = [
            r
            for r in rows
            if json.loads(r["identity"])["step"] in steps
            or json.loads(r["identity"])["job"] == job_id
        ]
        with pilot.admission._transaction() as db:
            provider_calls = [
                dict(r)
                for r in db.execute(
                    "SELECT ticket,job,step,active,outcome,usage FROM inference_calls WHERE quota=? AND scope=?",
                    (pilot.admission.quota_key, scope.identity()),
                )
                if r["step"] in steps or r["job"] == job_id
            ]
        observations.append(
            {
                "class": "usage_reservations",
                "state": "RETAINED_BY_POLICY",
                "records": [
                    {
                        "ticket": r["ticket"],
                        "state": r["state"],
                        "actual_cost": r["actual_cost"],
                        "reserved_cost": r["cost"],
                    }
                    for r in usage
                ],
                "provider_calls": provider_calls,
            }
        )
        if any(r["state"] not in {"SETTLED", "RELEASED"} for r in usage):
            observations.append(
                {"class": "usage_reservations", "state": "PENDING_RECONCILIATION"}
            )
    except Exception:  # noqa: BLE001 - financial unavailability must remain unknown
        observations.append(
            {"class": "usage_reservations", "state": "UNKNOWN_UNVERIFIED"}
        )
    with pilot.control.transaction() as db:
        feedback = (
            db.execute(
                "SELECT 1 FROM feedback WHERE session=?", (str(session),)
            ).fetchone()
            is not None
        )
        answers = db.execute(
            "SELECT COUNT(*) FROM answers WHERE session=?", (str(session),)
        ).fetchone()[0]
    observations.extend(
        [
            {
                "class": "jobs",
                "state": "RETAINED_BY_POLICY"
                if jobs_verified
                else "UNKNOWN_UNVERIFIED",
                "reference": job_id,
                "job_state": job_state,
            },
            {
                "class": "sparse_retrieval",
                "state": "UNKNOWN_UNVERIFIED",
                "reason": "process_local_copies_not_enumerable",
            },
            {
                "class": "temporary_processing",
                "state": "UNKNOWN_UNVERIFIED",
                "reason": "normal_parser_cleanup_not_crash_or_host_inventory",
            },
            {
                "class": "session_presentation",
                "state": "LOGICALLY_REVOKED_RETAINED"
                if row["state"] != "OPEN"
                else "RETAINED_BY_POLICY",
                "reason": "protected_review_answers_and_delivered_display_copies_not_recallable",
                "protected_answers": answers,
            },
            {
                "class": "feedback",
                "state": "RETAINED_BY_POLICY"
                if feedback
                else "LOGICALLY_REDACTED_PURGE_PENDING"
                if approval is None
                else "NOT_CREATED",
            },
            {
                "class": "participant_metadata",
                "state": "LOGICALLY_REDACTED_PURGE_PENDING"
                if approval is None
                else "RETAINED_BY_POLICY",
                "retention_until": retention_until,
                "policy": retention_reference,
            },
            {
                "class": "audit",
                "state": "RETAINED_BY_POLICY",
                "reason": "immutable_security_governance_pilot_history",
            },
            {
                "class": "backups",
                "state": "UNKNOWN_UNVERIFIED",
                "reason": "no_backup_inventory_adapter",
            },
            {
                "class": "upstream_provider_copies",
                "state": "OUTSIDE_DIRECT_CONTROL",
                "reason": "fixture_has_no_upstream_copy"
                if mode == "synthetic"
                else "provider_policy_requires_review",
            },
            {
                "class": "conversation_memory",
                "state": "NOT_CREATED",
                "reason": "pilot_never_uses_legacy_memory",
            },
        ]
    )
    for kind in CLASSES:
        if not any(o["class"] == kind for o in observations):
            observations.append(
                {
                    "class": kind,
                    "state": "NOT_CREATED" if not job_id else "UNKNOWN_UNVERIFIED",
                }
            )
    for observation in observations:
        kind = observation["class"]
        uncontrolled = kind in {"upstream_provider_copies", "backups"}
        private_metadata = kind in {
            "participant_metadata",
            "feedback",
            "session_presentation",
        }
        observation.update(
            owner=scope.identity(),
            custodian="provider"
            if kind == "upstream_provider_copies"
            else "UNKNOWN_UNVERIFIED"
            if kind == "backups"
            else "operator",
            location="provider_controlled"
            if kind == "upstream_provider_copies"
            else "UNKNOWN_UNVERIFIED"
            if kind == "backups"
            else "private_local_authorities",
            reason=observation.get(
                "reason", "approved_nonpersonal_retention_immutable_store"
            ),
            deadline="UNKNOWN_UNVERIFIED"
            if uncontrolled
            else retention_until
            if private_metadata
            else "APPROVED_NONPERSONAL_RETENTION_NO_ERASURE_DEADLINE",
        )
    return {
        "session_id": str(session),
        "state": row["state"],
        "access": "REVOKED" if access_revoked else "OPERATOR_ONLY",
        "purge_status": "PURGE_PENDING",
        "physical_erasure_verified": False,
        "operations": operations,
        "inventory": observations,
        "blocker": "immutable_object_vector_stores_shared_references_backups_and_upstream_deletion_unproven",
    }
