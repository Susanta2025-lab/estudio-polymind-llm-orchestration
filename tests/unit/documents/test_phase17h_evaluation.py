from dataclasses import replace
from io import BytesIO
import json
from pathlib import Path
from uuid import UUID

import pytest

from documents.extraction import extract
from documents.models import EvidenceRef, Span
from documents.storage import LocalObjectStore
from tests.performance.fixtures import pdf, NOW, SCOPE
from tests.performance.quality import ClaimJudgment, Observation, evaluate, ranking, structural_validity


def sample(**changes):
    base=Observation('case',(True,), (ClaimJudgment('claim',True,True,('finding',)),),
                     ('finding',),False,False,True,True,'independent synthetic oracle')
    return replace(base,**changes)


def test_valid_citation_does_not_imply_supported_claim():
    result=evaluate([sample(claims=(ClaimJudgment('wrong',False,True),),preservation_correct=False)])
    assert result['citation_validity']['rate']==1
    assert result['claim_support']['rate']==0
    assert result['critical_unsupported_conclusions']==1
    assert result['required_finding_coverage']['rate']==0
    assert result['contradiction_qualification_preservation']['rate']==0
    assert result['real_model_certification'].startswith('PENDING')


def test_exact_denominators_no_zero_percent_and_no_double_counted_findings():
    two=(ClaimJudgment('one',True,False,('finding',)),ClaimJudgment('two',True,False,('finding',)))
    result=evaluate([sample(claims=two),sample(case_id='absent',claims=(),required_findings=(),
        citation_validity=(),insufficient_evidence=True,abstained=True,preservation_required=False)])
    assert result['required_finding_coverage']=={'numerator':1,'denominator':1,'rate':1}
    assert result['claim_support']['denominator']==2
    assert result['abstention_correctness']['rate']==1
    assert evaluate([])['claim_support']['rate'] is None
    assert evaluate([sample(insufficient_evidence=True,abstained=True)])['abstention_correctness']['rate']==0


@pytest.mark.parametrize('mutation', ['duplicate_case','duplicate_claim','self_confidence','unknown_finding','unsupported_finding'])
def test_evaluator_rejects_unusable_annotations(mutation):
    value=sample()
    if mutation=='duplicate_case': values=[value,value]
    else:
        if mutation=='duplicate_claim': value=replace(value,claims=value.claims*2)
        if mutation=='self_confidence': value=replace(value,annotation_source='')
        if mutation=='unknown_finding': value=replace(value,claims=(ClaimJudgment('x',True,False,('unknown',)),))
        if mutation=='unsupported_finding': value=replace(value,claims=(ClaimJudgment('x',False,False,('finding',)),))
        values=[value]
    with pytest.raises(ValueError): evaluate(values)


def test_ranking_uses_exact_ids_and_separate_denominators():
    result=ranking(['irrelevant','far-page','similar-text'],{'far-page','qualified-page'},3)
    assert result['recall']['rate']==.5 and result['precision']['rate']==1/3
    assert result['reciprocal_rank']==.5
    assert ranking([],set(),5)['recall']['rate'] is None
    with pytest.raises(ValueError): ranking(['x','x'],{'x'},2)


def test_real_pdf_citation_checks_page_span_identity_and_authority(tmp_path):
    raw,_=pdf(4)
    artifact,_=extract(BytesIO(raw),scope=SCOPE,document_id=UUID(int=4),display_filename='test.pdf',
        declared_mime='application/pdf',store=LocalObjectStore(tmp_path/'objects'),created_at=NOW,extracted_at=NOW)
    unit=artifact.units[2]; block=unit.blocks[0]
    ref=EvidenceRef(scope=SCOPE,document_version_id=artifact.document.document_version_id,
        extraction_id=artifact.extraction_id,source_id=unit.source_id,block_id=block.block_id,span=block.span)
    assert structural_validity(artifact,ref,page=3,excerpt=unit.text,authorized=True)
    assert not structural_validity(artifact,ref,page=2,excerpt=unit.text,authorized=True)
    assert not structural_validity(artifact,ref,page=3,excerpt=unit.text,authorized=False)
    assert not structural_validity(artifact,ref.model_copy(update={'span':Span(start=0,end=99999)}),
                                   page=3,excerpt=unit.text,authorized=True)
    assert not structural_validity(artifact,ref.model_copy(update={'document_version_id':UUID(int=99)}),
                                   page=3,excerpt=unit.text,authorized=True)


def test_dataset_exercises_all_metrics_without_claiming_model_evaluation(tmp_path):
    data=json.loads(Path('tests/fixtures/phase17h/quality.json').read_text())
    observations=[]
    for case in data['cases']:
        observations.append(Observation(case['case_id'],tuple(True for _ in case['required_pages']),
            tuple(ClaimJudgment(f,True,case['criticality']=='high',(f,)) for f in case['required_findings']),
            tuple(case['required_findings']),case['insufficient_evidence'],case['insufficient_evidence'],
            case['preservation_required'],True,data['annotation_origin']))
    result=evaluate(observations)
    assert result['case_count']==12
    assert result['categories']==['synthetic']
    assert result['claim_support']['denominator']>0
    assert result['abstention_correctness']['denominator']==4
    # This measures the rubric arithmetic on authored judgments, not inference.
    (tmp_path/'metrics.json').write_text(json.dumps(result))
