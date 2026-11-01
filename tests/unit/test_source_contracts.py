"""Portable contract comparison, using fixed references and synthetic mutations."""

from itertools import product
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.source_contracts import (
    DOMAIN_NAMES,
    assert_source_contract,
    canonical_source,
    source_sections,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures/digestion_contracts"
VALIDATION = (FIXTURES / "validation.py.txt").read_text(encoding="utf-8")
MODELS = (FIXTURES / "models.py.txt").read_text(encoding="utf-8")

SYNTHETIC = """\
def validate_result(result, request):
    if result.stage_id != request.stage_id:
        raise DigestionError("stage", diagnostic=ValidationDiagnostic.STAGE_BINDING,
                             reason=Reason.STAGE_ID_MISMATCH)
    if result.claim_id != request.claim_id:
        raise DigestionError("identity", reason=Reason.CLAIM_ID_MISMATCH)
    if result.coverage != request.coverage:
        raise DigestionError("coverage", reason=Reason.MISSING_SOURCE_COVERAGE)
    if result.evidence not in request.evidence:
        raise DigestionError("evidence", reason=Reason.FOREIGN_EVIDENCE)
    return True
"""


def mutated(source, before, after):
    """Prove each controlled mutation is unique and remains valid Python."""
    assert source.count(before) == 1
    changed = source.replace(before, after)
    compile(changed, "<synthetic-contract>", "exec")
    return changed


@pytest.mark.parametrize(
    "source", [SYNTHETIC, VALIDATION, *source_sections(MODELS, DOMAIN_NAMES).values()]
)
def test_fixed_source_is_deterministic(source):
    assert canonical_source(source) == canonical_source(source)


def test_token_representation_has_an_independent_literal_oracle():
    assert canonical_source("limit = 4\n") == (
        ("NAME", "limit"),
        ("OP", "="),
        ("NUMBER", "4"),
        ("NEWLINE", ""),
    )


def test_whitespace_comments_and_unicode_locations_are_not_contract_changes():
    approved = 'def check():\n    label = "é"; return 1\n'
    changed = 'def check( ):  # comment\n        label="é"; return 1  # comment\n'
    assert_source_contract(changed, approved)
    assert_source_contract(changed.replace("\n", "\r\n"), approved)


@pytest.mark.parametrize(
    "before,after",
    [
        (
            "claim.claim_id != stable_id(str(request.stage_id), str(position))\n                or ",
            "",
        ),
        ("used != set(permitted)", "not used <= set(permitted)"),
        (" or not set(values) <= allowed", ""),
        (
            "if result.stage_id != request.stage_id or",
            "if result.stage_id == request.stage_id or",
        ),
        ("linked != links.keys()", "not linked <= links.keys()"),
        ("or not set(qualification.evidence_ids) <= allowed", ""),
        ("or not set(lineage) <= links.keys()", ""),
        ("len(encode(result)) > profile.max_result_characters", "False"),
        ("len(result.open_questions) > profile.max_annotations", "False"),
        ("claim.subject is not None and claim.kind != 'fact'", "False"),
        (
            '"coverage_failed",\n            diagnostic=ValidationDiagnostic.COVERAGE_VALIDATION,\n            reason=(Reason.MISSING_SOURCE_COVERAGE),',
            '"inference_contract_error",\n            diagnostic=ValidationDiagnostic.COVERAGE_VALIDATION,\n            reason=(Reason.MISSING_SOURCE_COVERAGE),',
        ),
    ],
    ids=[
        "claim-identity-removed",
        "source-coverage-weakened",
        "evidence-membership-removed",
        "stage-binding-changed",
        "reduction-coverage-weakened",
        "qualification-membership-removed",
        "child-lineage-removed",
        "response-limit-removed",
        "annotation-limit-removed",
        "claim-contract-removed",
        "public-error-category-changed",
    ],
)
def test_acceptance_mutations_fail_for_source_mismatch(before, after):
    changed = mutated(VALIDATION, before, after)
    with pytest.raises(AssertionError, match="Frozen source contract changed"):
        assert_source_contract(changed, VALIDATION, allow_diagnostics=True)


@pytest.mark.parametrize(
    "name,before,after",
    [
        ("Text", "max_length=4096", "max_length=8192"),
        (
            "DigestionProfile",
            "max_claims: int = Field(ge=1, le=64)",
            "max_claims: int = Field(ge=0, le=64)",
        ),
        ("DigestionProfile", "self.context_tokens <=", "self.context_tokens <"),
        ("DigestionProfile", "if self.max_response_bytes is None:", "if False:"),
        ("ClaimLink", "claim_id: UUID", "claim_id: str"),
        (
            "Qualification",
            "evidence_ids: tuple[UUID, ...]",
            "evidence_ids: tuple[str, ...]",
        ),
        ("Claim", "'structural']", "'structural', 'new']"),
        ("StageResult", "claims: tuple[Claim, ...]", "claims: tuple[Claim, ...] = ()"),
        ("StageRequest", "len(ids) != len(set(ids))", "False"),
    ],
)
def test_domain_types_constraints_validation_and_serialization_remain_frozen(
    name, before, after
):
    approved = source_sections(MODELS, DOMAIN_NAMES)[name]
    changed = mutated(approved, before, after)
    with pytest.raises(AssertionError, match="Frozen source contract changed"):
        assert_source_contract(changed, approved)


def test_generation_instruction_mutation_is_detected():
    approved = 'SYSTEM = "Use ONLY the supplied source evidence."\n'
    changed = mutated(approved, "ONLY", "any of")
    with pytest.raises(AssertionError, match="Frozen source contract changed"):
        assert_source_contract(changed, approved)


@pytest.mark.parametrize(
    "before,after",
    [
        ("Reason.CANONICAL_RESPONSE_LIMIT", "Reason.TEXT_LIMIT"),
        ("ValidationDiagnostic.RESPONSE_LIMIT", "ValidationDiagnostic.STAGE_BINDING"),
        ("Reason.STAGE_ID_MISMATCH", "Reason.STAGE_KIND_MISMATCH"),
        ("diagnostic=ValidationDiagnostic.CLAIM_IDENTITY,", ""),
    ],
)
def test_permitted_diagnostic_only_changes_match_the_approved_contract(before, after):
    # Constant diagnostics may appear on multiple rejections; all remain inert.
    changed = VALIDATION.replace(before, after)
    assert changed != VALIDATION
    compile(changed, "<diagnostic-only-copy>", "exec")
    assert_source_contract(changed, VALIDATION, allow_diagnostics=True)


def test_diagnostics_do_not_change_synthetic_acceptance_or_public_errors():
    changed = SYNTHETIC.replace("Reason.STAGE_ID_MISMATCH", "Reason.FOREIGN_EVIDENCE")
    changed = changed.replace(
        ", diagnostic=ValidationDiagnostic.STAGE_BINDING", ""
    ).replace(", reason=Reason.CLAIM_ID_MISMATCH", "")
    assert_source_contract(changed, SYNTHETIC, allow_diagnostics=True)

    class Rejection(Exception):
        def __init__(self, category, **metadata):
            super().__init__(category)

    def load(source):
        namespace = {
            "DigestionError": Rejection,
            "ValidationDiagnostic": SimpleNamespace(STAGE_BINDING="stage"),
            "Reason": SimpleNamespace(
                STAGE_ID_MISMATCH="stage",
                CLAIM_ID_MISMATCH="claim",
                MISSING_SOURCE_COVERAGE="coverage",
                FOREIGN_EVIDENCE="evidence",
            ),
        }
        exec(compile(source, "<synthetic-only>", "exec"), namespace)  # noqa: S102 - Fixed synthetic fixture only.
        return namespace["validate_result"]

    def outcome(function, result, request):
        try:
            return function(result, request)
        except Rejection as exc:
            return str(exc)

    original, modified = load(SYNTHETIC), load(changed)
    request = SimpleNamespace(stage_id=1, claim_id=1, coverage=1, evidence={1})
    outcomes = set()
    for values in product((0, 1), repeat=4):
        result = SimpleNamespace(
            **dict(zip(("stage_id", "claim_id", "coverage", "evidence"), values))
        )
        expected = outcome(original, result, request)
        assert outcome(modified, result, request) == expected
        outcomes.add(expected)
    assert outcomes == {True, "stage", "identity", "coverage", "evidence"}


@pytest.mark.parametrize(
    "expression",
    [
        "mutate_acceptance()",
        "(changed := request.stage_id)",
        "Reason.STAGE_ID_MISMATCH if side_effect() else Reason.FOREIGN_EVIDENCE",
        "Reason.UNKNOWN_UNAPPROVED_MEMBER",
    ],
)
def test_executable_or_unapproved_metadata_cannot_be_ignored(expression):
    changed = mutated(
        SYNTHETIC, "reason=Reason.STAGE_ID_MISMATCH", "reason=" + expression
    )
    with pytest.raises(ValueError, match="Unapproved executable diagnostic metadata"):
        assert_source_contract(changed, SYNTHETIC, allow_diagnostics=True)


def test_unrecognized_error_keywords_cannot_disappear():
    changed = mutated(
        SYNTHETIC, 'DigestionError("stage",', 'DigestionError("stage", accepted=True,'
    )
    with pytest.raises(AssertionError, match="Frozen source contract changed"):
        assert_source_contract(changed, SYNTHETIC, allow_diagnostics=True)


def test_metadata_exception_is_limited_to_direct_rejections():
    approved = 'accepted = DigestionError("stage", reason=Reason.STAGE_ID_MISMATCH)\n'
    changed = approved.replace("STAGE_ID_MISMATCH", "FOREIGN_EVIDENCE")
    with pytest.raises(AssertionError, match="Frozen source contract changed"):
        assert_source_contract(changed, approved, allow_diagnostics=True)


def test_indentation_block_boundaries_and_literal_spaces_are_significant():
    for changed in (
        "if ready:\n    accept()\nreject()\n",
        'if ready:\n    accept()\n    reject("a b")\n',
    ):
        with pytest.raises(AssertionError, match="Frozen source contract changed"):
            assert_source_contract(changed, "if ready:\n    accept()\n    reject()\n")


def test_decorators_are_protected_and_duplicate_or_missing_declarations_fail():
    approved = "@frozen\nclass Claim:\n    value: int\n"
    assert source_sections(approved, ("Claim",))["Claim"] == approved.rstrip()
    with pytest.raises(ValueError, match="Duplicate frozen declaration"):
        source_sections(approved + approved, ("Claim",))
    with pytest.raises(ValueError, match="Missing frozen declaration"):
        source_sections(approved, ("Other",))


def test_utf8_offsets_preserve_literals_before_metadata():
    approved = SYNTHETIC.replace('"stage"', '"étape"')
    changed = approved.replace("Reason.STAGE_ID_MISMATCH", "Reason.FOREIGN_EVIDENCE")
    assert_source_contract(changed, approved, allow_diagnostics=True)


def test_formatted_string_grammar_requires_explicit_review():
    with pytest.raises(
        ValueError, match="Formatted strings require reviewed canonicalization"
    ):
        canonical_source('instruction = f"Use {source}"\n')
