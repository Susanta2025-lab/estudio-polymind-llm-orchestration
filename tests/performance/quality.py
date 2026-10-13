"""Versioned, annotation-driven quality metrics, independent of model confidence.

Semantic judgments are supplied by a named evaluator/annotation source. This
module does not infer entailment from matching citation IDs or text similarity.
"""
from dataclasses import dataclass

VERSION = 'phase17h-rubric/1'


@dataclass(frozen=True)
class ClaimJudgment:
    claim_id: str
    supported: bool
    critical: bool
    correct_findings: tuple[str, ...] = ()


@dataclass(frozen=True)
class Observation:
    case_id: str
    citation_validity: tuple[bool, ...]
    claims: tuple[ClaimJudgment, ...]
    required_findings: tuple[str, ...]
    insufficient_evidence: bool
    abstained: bool
    preservation_required: bool
    preservation_correct: bool
    annotation_source: str
    category: str = 'synthetic'


def rate(numerator, denominator):
    if denominator < 0 or not 0 <= numerator <= denominator:
        raise ValueError('invalid metric counts')
    return {'numerator':numerator,'denominator':denominator,
            'rate':numerator/denominator if denominator else None}


def evaluate(observations):
    observations=tuple(observations)
    if len({o.case_id for o in observations})!=len(observations):
        raise ValueError('duplicate evaluation case')
    for o in observations:
        if (not o.annotation_source or o.category not in {'synthetic','human-reviewed-model'}
                or len(set(o.required_findings))!=len(o.required_findings)
                or len({c.claim_id for c in o.claims})!=len(o.claims)
                or any(type(v) is not bool for v in (*o.citation_validity,o.insufficient_evidence,
                        o.abstained,o.preservation_required,o.preservation_correct))):
            raise ValueError('invalid independent annotation')
        for c in o.claims:
            if (type(c.supported) is not bool or type(c.critical) is not bool
                    or not set(c.correct_findings)<=set(o.required_findings)
                    or (c.correct_findings and not c.supported)):
                raise ValueError('invalid claim annotation')
    claims=[c for o in observations for c in o.claims]
    citations=[v for o in observations for v in o.citation_validity]
    insufficient=[o for o in observations if o.insufficient_evidence]
    preservation=[o for o in observations if o.preservation_required]
    return {'rubric_version':VERSION,'case_count':len(observations),
        'categories':sorted({o.category for o in observations}),
        'annotation_sources':sorted({o.annotation_source for o in observations}),
        'citation_validity':rate(sum(citations),len(citations)),
        'claim_support':rate(sum(c.supported for c in claims),len(claims)),
        'required_finding_coverage':rate(sum(len({f for c in o.claims if c.supported for f in c.correct_findings})
                                              for o in observations),sum(len(o.required_findings) for o in observations)),
        'critical_unsupported_conclusions':sum(c.critical and not c.supported for c in claims),
        'abstention_correctness':rate(sum(o.abstained and not o.claims for o in insufficient),len(insufficient)),
        'contradiction_qualification_preservation':rate(sum(o.preservation_correct for o in preservation),len(preservation)),
        'real_model_certification':'PENDING: metrics alone do not establish representative expert sampling'}


def ranking(retrieved, relevant, k):
    if type(k) is not int or k<=0 or len(set(retrieved))!=len(retrieved):
        raise ValueError('invalid ranking')
    selected=list(retrieved[:k]); relevant=set(relevant)
    found=sum(item in relevant for item in selected)
    first=next((1/(i+1) for i,item in enumerate(selected) if item in relevant),0.)
    return {'k':k,'returned':len(selected),'relevant':len(relevant),
            'recall':rate(found,len(relevant)), 'precision':rate(found,k),
            'reciprocal_rank':first if relevant else None}


def structural_validity(artifact, evidence, *, page, excerpt, authorized):
    """Validate canonical source/version/block/span plus separately granted access."""
    from documents.digestion.validation import EvidenceIndex
    if not authorized:
        return False
    try:
        index=EvidenceIndex(artifact)
        text=index.resolve(evidence)
        unit,_=index.blocks[evidence.block_id]
        return unit.physical_page==page and text==excerpt
    except Exception:
        return False


def evaluate_completed_benchmark(directory, output):
    """Evaluate authored synthetic leaf facts in an actually accepted 200-page digest.

    Exact-text labels are an oracle for these fixed fixtures only; this is not a
    natural-language entailment evaluator or independent expert review.
    """
    from pathlib import Path
    import json
    from uuid import UUID
    from documents.jobs.models import JobSettings
    from documents.jobs.sqlite import SQLiteJobLedger
    from documents.digestion.workflow import load_digest
    from documents.serialization import deserialize
    from documents.storage import LocalObjectStore
    from documents.digestion.models import SourcePiece
    from tests.performance.fixtures import SCOPE
    from tests.performance.phase17h import write
    directory=Path(directory);output=Path(output)
    dataset_path=Path('tests/fixtures/phase17h/quality.json')
    dataset=json.loads(dataset_path.read_text())
    ledger=SQLiteJobLedger(JobSettings(database_path=directory/'jobs.sqlite',lease_seconds=120))
    # Read-only enumeration of this isolated benchmark ledger; no production store.
    import sqlite3
    with sqlite3.connect(directory/'jobs.sqlite') as db:
        rows=db.execute('SELECT job_id FROM jobs').fetchall()
    if len(rows)!=1:raise ValueError('one benchmark job required')
    store=LocalObjectStore(directory/'objects')
    digest=load_digest(ledger,store,SCOPE,UUID(rows[0][0]))
    artifact=deserialize(store.read(SCOPE,digest.extraction,max_bytes=32000000))
    by_id={SourcePiece(evidence=e,text='',kind='text').evidence_id():e for e in digest.evidence}
    from documents.digestion.validation import EvidenceIndex
    index=EvidenceIndex(artifact);observations=[];materialized=[]
    for page,text in dataset['facts'].items():
        matched=[f for f in digest.findings if f.text==text]
        if len(matched)!=1:raise AssertionError('expected synthetic leaf finding missing')
        finding=matched[0];refs=[by_id[e] for e in finding.evidence_ids]
        valid=tuple(structural_validity(artifact,e,page=int(page),excerpt=index.resolve(e),authorized=True) for e in refs)
        # Support labels require the actual cited excerpt to contain the independently
        # recorded exact synthetic proposition, rather than trusting citation identity.
        supported=bool(refs) and all(valid) and any(text in index.resolve(e) for e in refs)
        preservation=int(page) in (5,180)
        preserved=bool(finding.qualifications) and bool(digest.contradictions) if preservation else True
        observations.append(Observation('page-'+page,valid,(ClaimJudgment(str(finding.claim_id),supported,True,('fact',) if supported else ()),),
            ('fact',),False,False,preservation,preserved,dataset['annotation_origin']))
        materialized.append({'page':int(page),'fact':text,'finding_id':str(finding.claim_id),
            'references':[e.model_dump(mode='json') for e in refs],
            'excerpts':[index.resolve(e) for e in refs]})
    # Adversarial control: perfectly valid evidence coordinates plus a false assertion.
    negative=Observation('false-critical',(True,), (ClaimJudgment('ORION capacity 500',False,True),),
        ('capacity25',),False,False,False,False,'engineer-authored adversarial control')
    result={'dataset_version':dataset['version'],'dataset_sha256':__import__('hashlib').sha256(dataset_path.read_bytes()).hexdigest(),
        'source_sha256':artifact.document.source.sha256,'document_version':str(artifact.document.document_version_id),
        'accepted_digest':evaluate(observations),'negative_control':evaluate([negative]),'materialized_ground_truth':materialized,
        'question_cases':dataset['cases'], 'question_answer_evaluation':'PENDING: no actual model answers supplied',
        'authorization_scope':'trusted offline owning scope; live authorization is separately tested',
        'expert_sampling':'NOT VALIDATED'}
    write(output,result);return result


if __name__=='__main__':
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser();parser.add_argument('--benchmark',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():raise ValueError('new output required')
    evaluate_completed_benchmark(args.benchmark,args.output)
