"""Pure deterministic planning; no inference, dispatch, retrieval or network."""

from collections import defaultdict
import hashlib
from typing import Protocol

from documents.models import EvidenceRef, ExtractionArtifact, Span, stable_id
from documents.serialization import serialize
from documents.jobs.models import fingerprint
from documents.digestion.codec import encode
from documents.digestion.models import (
    AnalysisChunk, DigestionError, DigestionProfile, Plan, ReductionNode,
    SourcePiece, StageRequest, StructuralMap, StructuralUnit,
)

class SizeEstimator(Protocol):
    def estimate(self, value: str) -> int: ...


class CharacterEstimator:
    """One canonical JSON character per estimated token. NOT provider usage."""
    def estimate(self, value):
        return len(value)


def request_size(request):
    return CharacterEstimator().estimate(encode(request).decode('ascii')) + request.profile.template_tokens


def check_request(request):
    size = request_size(request)
    if size + request.profile.reserved_output_tokens > request.profile.context_tokens:
        raise DigestionError('synthesis_limit_exceeded')
    return size


def _structure(artifact, ref, profile):
    doc = artifact.document
    root_id = stable_id(str(artifact.extraction_id), profile.digest(), 'structure-root')
    blocks = {b.block_id: b for u in artifact.units for b in u.blocks}
    headings = {key: b for key, b in blocks.items() if b.kind == 'heading'}
    # Canonical heading parents declare hierarchy; font/whitespace never invents it.
    parents = {}
    for key, block in headings.items():
        parent = block.parent_id
        if parent is not None and parent not in headings:
            raise DigestionError('structural_planning_failed')
        seen = {key}
        while parent is not None:
            if parent in seen or len(seen) > profile.max_depth:
                raise DigestionError('structural_planning_failed')
            seen.add(parent)
            parent = headings[parent].parent_id
        parents[key] = block.parent_id
    nodes = {root_id: dict(structural_unit_id=root_id, parent_id=None, child_ids=[], order=0,
                          kind='document', source='root', confidence='source-declared',
                          block_ids=[], source_ids=[], physical_pages=[], path=())}
    heading_nodes = {key: stable_id(str(root_id), str(key)) for key in headings}
    fallback = stable_id(str(root_id), 'fallback')

    def add(key, parent, **kw):
        if key in nodes:
            return
        nodes[key] = dict(structural_unit_id=key, parent_id=parent, child_ids=[],
                          order=len(nodes[parent]['child_ids']), block_ids=[], source_ids=[],
                          physical_pages=[], **kw)
        nodes[parent]['child_ids'].append(key)

    current = None
    for unit in artifact.units:
        for block in unit.blocks:
            if block.block_id in headings:
                parent_key = parents[block.block_id]
                parent = heading_nodes[parent_key] if parent_key else root_id
                if parent not in nodes:
                    raise DigestionError('structural_planning_failed')  # Forward/ambiguous section.
                current = heading_nodes[block.block_id]
                heading = block.source_text
                add(current, parent, kind='subsection' if parent_key else 'section',
                    source='canonical-heading', confidence='source-declared', heading=heading,
                    path=nodes[parent]['path'] + (heading,))
            elif block.parent_id in heading_nodes:
                current = heading_nodes[block.parent_id]
                if current not in nodes:
                    raise DigestionError('structural_planning_failed')
            if current is None:
                add(fallback, root_id, kind='fallback',
                    source='canonical-page' if doc.page_count else 'canonical-text',
                    confidence='fallback', path=())
                current = fallback
            node = nodes[current]
            node['block_ids'].append(block.block_id)
            if not node['source_ids'] or node['source_ids'][-1] != unit.source_id:
                node['source_ids'].append(unit.source_id)
            if unit.physical_page and (not node['physical_pages'] or node['physical_pages'][-1] != unit.physical_page):
                node['physical_pages'].append(unit.physical_page)
    if not nodes[root_id]['child_ids']:
        add(fallback, root_id, kind='fallback', source='canonical-page' if doc.page_count else 'canonical-text',
            confidence='fallback', path=())
    nodes[root_id]['source_ids'] = [u.source_id for u in artifact.units]
    nodes[root_id]['physical_pages'] = [u.physical_page for u in artifact.units if u.physical_page is not None]
    return StructuralMap(extraction=ref, document_version_id=doc.document_version_id,
                         profile=profile.digest(), units=tuple(StructuralUnit(**n) for n in nodes.values()))


def build_plan(artifact, extraction_ref, profile):
    """Fully bound plan before admission; unknown/unsupported content stays inventoried."""
    try:
        artifact = ExtractionArtifact.model_validate(artifact.model_dump(mode='json'))
        profile = DigestionProfile.model_validate(profile.model_dump(mode='json'))
        data = serialize(artifact)
        if (extraction_ref.scope != artifact.document.scope or extraction_ref.kind != 'artifact'
                or extraction_ref.object_id != artifact.extraction_id
                or extraction_ref.sha256 != hashlib.sha256(data).hexdigest()
                or extraction_ref.byte_size != len(data)):
            raise DigestionError('evidence_validation_failed')
        return _build(artifact, extraction_ref, profile)
    except DigestionError:
        raise
    except Exception:
        raise DigestionError('structural_planning_failed') from None


def _build(artifact, ref, profile):
    inventory = [(u, b) for u in artifact.units for b in u.blocks]
    if len(inventory) + sum(not u.blocks for u in artifact.units) > profile.max_source_units:
        raise DigestionError('synthesis_limit_exceeded')
    structure = _structure(artifact, ref, profile)
    by_block = {b.block_id: (u, b) for u, b in inventory}
    eligible, skipped, unsupported = [], [], []
    for unit in artifact.units:
        ids = [b.block_id for b in unit.blocks] or [unit.source_id]
        if unit.status == 'failed' or unit.decision.outcome != 'native_accepted':
            unsupported.extend(ids)
        elif not unit.text.strip():
            skipped.extend(ids)  # Explicit policy: known blank units have no analysis.
        else:
            eligible.extend(ids)
    eligible_set = set(eligible)
    chunks = []
    chunk_ids = defaultdict(list)
    profile_hash = profile.digest()

    def make_chunk(node, pieces):
        key = stable_id(str(artifact.extraction_id), profile_hash, 'chunk',
                        str(node.structural_unit_id), *(str(p.evidence_id()) for p in pieces))
        request = StageRequest(stage_id=key, stage='analysis', profile=profile,
                               structural_path=node.path, source_data=tuple(pieces))
        estimate = check_request(request)
        return AnalysisChunk(chunk_id=key, document_version_id=artifact.document.document_version_id,
                             structural_parent=node.structural_unit_id, path=node.path,
                             sequence=len(chunks), profile=profile_hash, pieces=tuple(pieces),
                             estimated_tokens=estimate)

    def append(node, pieces):
        if not pieces:
            return
        if len(chunks) >= profile.max_chunks:
            raise DigestionError('synthesis_limit_exceeded')
        chunk = make_chunk(node, pieces)
        chunks.append(chunk)
        chunk_ids[node.structural_unit_id].append(chunk.chunk_id)

    # A parent can own text after a subsection. Chunk in canonical order rather
    # than collecting all of that parent's discontiguous text before its children.
    owners = {key: node for node in structure.units for key in node.block_ids}
    groups = []
    for _, block in inventory:
        owner = owners[block.block_id]
        if not groups or groups[-1][0].structural_unit_id != owner.structural_unit_id:
            groups.append((owner, []))
        groups[-1][1].append(block.block_id)
    for node, block_ids in groups:
        pending, characters = [], 0
        for block_id in block_ids:
            if block_id not in eligible_set:
                continue
            unit, block = by_block[block_id]
            start = block.span.start
            line_start = block.span.line_start
            visual = block.visual
            cells = visual.cells if visual and visual.state == 'parsed' else None
            first = True
            while start < block.span.end or first:
                first = False
                end = min(block.span.end, start + profile.chunk_characters)
                if end < block.span.end:
                    boundary = unit.text.rfind('\n', start, end)
                    if boundary >= start:
                        end = boundary + 1
                while True:
                    text = unit.text[start:end]
                    evidence = EvidenceRef(scope=artifact.document.scope,
                                           document_version_id=artifact.document.document_version_id,
                                           extraction_id=artifact.extraction_id, source_id=unit.source_id,
                                           block_id=block_id, span=Span(start=start, end=end,
                                               line_start=line_start,
                                               line_end=line_start + text.rstrip('\n').count('\n') if line_start else None))
                    # 17B cells lack row-to-text offsets: whole table or explicit failure.
                    if cells is not None and (start != block.span.start or end != block.span.end):
                        raise DigestionError('synthesis_limit_exceeded')
                    limitation = ('visual_uninterpreted' if block.kind in ('table', 'figure') and cells is None
                                  else 'hard_split' if start != block.span.start or end != block.span.end else 'none')
                    piece = SourcePiece(evidence=evidence, text=text, kind=block.kind,
                                        cells=cells, limitation=limitation)
                    try:
                        make_chunk(node, [piece])
                        break
                    except DigestionError:
                        if cells is not None or end-start <= 1:
                            raise
                        end = start + (end-start)//2
                fits = characters + len(text) <= profile.chunk_characters
                if pending and fits:
                    try:
                        make_chunk(node, pending + [piece])
                    except DigestionError:
                        fits = False
                if pending and not fits:
                    append(node, pending)
                    pending, characters = [], 0
                pending.append(piece)
                characters += len(text)
                start = end
                if line_start is not None:
                    line_start += text.count("\n")
        append(node, pending)

    if not chunks:
        raise DigestionError('coverage_failed')
    reducers, levels = [], {c.chunk_id: 0 for c in chunks}
    outputs = {}
    positions = {c.chunk_id: c.sequence for c in chunks}
    # Conservative worst-case serialized child result, reference and request wrapper.
    # Account context/profile/path exactly; child refs have a fixed bounded encoding.
    empty = StageRequest(stage_id=structure.units[0].structural_unit_id, stage='reduction',
                         profile=profile, structural_path=())
    base = request_size(empty)
    per_child = profile.max_result_characters + 1024

    def reduce_group(node, children):
        if not children:
            return None
        overhead = base + len(encode(empty.model_copy(update={'structural_path': node.path}))) + 512
        capacity = min(profile.max_fan_in,
                       (profile.context_tokens-profile.reserved_output_tokens-overhead) // per_child)
        if capacity < 2:
            raise DigestionError('synthesis_limit_exceeded')
        current = list(children)
        while True:
            following = []
            for offset in range(0, len(current), capacity):
                group = tuple(current[offset:offset+capacity])
                level = 1 + max(levels[k] for k in group)
                if level > profile.max_depth:
                    raise DigestionError('synthesis_limit_exceeded')
                key = stable_id(str(artifact.extraction_id), profile_hash, 'reduction',
                                str(node.structural_unit_id), *(str(k) for k in group))
                reducers.append(ReductionNode(stage_id=key, structural_parent=node.structural_unit_id,
                                              children=group, level=level, path=node.path,
                                              estimated_tokens=overhead + len(group)*per_child))
                levels[key] = level
                positions[key] = min(positions[k] for k in group)
                following.append(key)
                if len(chunks)+len(reducers)+2 > profile.max_steps:
                    raise DigestionError('synthesis_limit_exceeded')
            if len(following) == 1:
                return following[0]
            current = following

    for node in reversed(structure.units):
        children = chunk_ids[node.structural_unit_id] + [outputs[k] for k in node.child_ids if outputs.get(k)]
        outputs[node.structural_unit_id] = reduce_group(node, sorted(children, key=positions.__getitem__))
    return Plan(profile=profile, structure=structure, chunks=tuple(chunks), reducers=tuple(reducers),
                root_id=outputs[structure.units[0].structural_unit_id], eligible=tuple(eligible),
                skipped=tuple(skipped), unsupported=tuple(unsupported))
