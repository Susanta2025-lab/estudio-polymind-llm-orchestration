"""Deterministic development transport and vector substitutes, without network.

These fixtures exercise managed-prompt/11 decoding and provenance. Their output
is synthetic plumbing evidence, never a semantic-quality judgment.
"""
import json
import time
from dataclasses import asdict
from pathlib import Path

from rag.vector_store import VectorDocument, VectorMatch


class FixtureHTTP:
    def __init__(self):
        self.attempts = 0
        self.external_attempts = 0
        self.last_call = 0

    def post(self, url, **kwargs):
        if url != "https://fixture.invalid/v1/chat/completions":
            self.external_attempts += 1
            raise RuntimeError("fixture_transport_denied")
        self.attempts += 1
        self.last_call = time.time()
        sent = kwargs["json"]
        data = json.loads(sent["messages"][1]["content"])
        if "\nCONTROL\n" in sent["messages"][0]["content"]:
            control = json.loads(sent["messages"][0]["content"].split("\nCONTROL\n")[1])
            if control["kind"] == "analysis":
                claims = [dict(text="Synthetic inspection requires a valve check; field safety remains untested.",
                    kind="fact", status="supported", stance="unknown", subject=None,
                    evidence_refs=[p["evidence_ref"] for p in data["UNTRUSTED_DOCUMENT_DATA"]],
                    contradicting_evidence_refs=[], qualifications=[], child_refs=[])]
            else:
                claims = [dict(text="Inherited findings and qualifications apply.", kind="commentary",
                    status="supported", stance="unknown", subject=None, evidence_refs=[],
                    contradicting_evidence_refs=[], qualifications=[], child_refs=control["required_child_refs"])]
            result = dict(schema_version="stage-proposal/1", request_binding=control["request_binding"],
                          outcome="analyzed", claims=claims, open_questions=[],
                          limitations=["Synthetic fixture; semantic support has not been evaluated."])
        else:
            evidence = data["ORIGINAL_SOURCE_EVIDENCE"]
            # Only the authored question has a fixture oracle. Everything else abstains.
            query = data.get("question", "")
            supported = "valve" in str(query).lower() and bool(evidence)
            result = dict(answer=evidence[0]["excerpt"] if supported else "Evidence is insufficient.",
                          evidence_status="available" if supported else "insufficient",
                          citation_ids=[evidence[0]["citation_id"]] if supported else [])
        raw = json.dumps(dict(model="offline-model", choices=[dict(message=dict(content=json.dumps(result)),
            finish_reason="stop")], usage=dict(prompt_tokens=30, completion_tokens=40, total_tokens=70))).encode()

        class Response:
            status_code = 200
            headers = {}

            def iter_content(self, chunk_size):
                yield raw

            def close(self):
                pass
        return Response()


class FixtureModel:
    max_seq_length = 256

    class Tokenizer:
        model_max_length = 512

        def __call__(self, text, **kwargs):
            if kwargs.get("truncation") is not False:
                raise ValueError("fixture_truncation_denied")
            return {"input_ids": list(range(len(text) + 2))}
    tokenizer = Tokenizer()

    def get_sentence_embedding_dimension(self):
        return 384

    def encode(self, text, **kwargs):
        class Vector:
            def tolist(self):
                return [1.] + [0.] * 383
        return Vector()


class FixtureVectors:
    """Private persistent derived index. No network, no semantic ranking claim."""
    def __init__(self, path, *, initialize=False):
        self.path = Path(path)
        if initialize:
            with self.path.open("x") as stream:
                json.dump({}, stream)
        self._read()

    def _read(self):
        return {k: VectorDocument(**v) for k, v in json.loads(self.path.read_text()).items()}

    def upsert(self, ids, documents, embeddings, metadatas):
        rows = self._read()
        rows.update({k: VectorDocument(t, m) for k, t, m in zip(ids, documents, metadatas)})
        temp = self.path.with_suffix(".pending")
        temp.write_text(json.dumps({k: asdict(v) for k, v in rows.items()}))
        temp.replace(self.path)

    def list_documents(self, *, scope=None):
        return [r for r in self._read().values() if scope is None or (
            r.metadata["generation"] == scope.generation and
            (not scope.document_ids or r.metadata["document_id"] in scope.document_ids))]

    def similarity_search(self, embedding, limit, *, scope=None):
        return [VectorMatch(r.document, r.metadata, .1) for r in self.list_documents(scope=scope)[:limit]]

    def close(self):
        pass
