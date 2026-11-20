"""Explicit offline-only container composition for the integration harness.

Never imported by production. All signing is test-purpose; provider effects use
MockHTTP. Real Redis, Chroma and baked CPU retrieval models exercise the topology.
"""
import os
from pathlib import Path
import socket
from threading import Lock


def main():
    if os.environ.get('DEPLOYMENT_ENV') != 'compose' or os.environ.get('DOCUMENTS_PROFILE') != 'synthetic':
        raise SystemExit('Explicit offline fixture composition required')
    import pytest
    import sentence_transformers
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from rag.vector_store_factory import create_publication_vector_store
    from memory.memory_store import RedisMemoryStore
    from tests.integration.test_phase19_operator import external
    from tests.integration.test_phase19_execution_bridge import bridge, attach_reviews
    import redis
    import uvicorn
    from fastapi import Request
    from deployment.phase19.runtime import configuration
    from documents.operator.app import create_app
    from documents.publication.encoding import RetrievalEncoder
    from documents.publication.models import RetrievalProfile
    from graph.semantic_router import semantic_route
    real_connect = socket.socket.connect
    patch = pytest.MonkeyPatch()
    root = Path('/runtime/integration'); root.mkdir(mode=0o700)
    external_generator = external.__wrapped__(root, patch)
    external_env = next(external_generator)
    bridge_generator = bridge.__wrapped__(external_env, patch)
    env = next(bridge_generator)
    patch.setattr(socket.socket, 'connect', real_connect)
    patch.setattr(sentence_transformers, 'SentenceTransformer', SentenceTransformer)
    patch.setattr(sentence_transformers, 'CrossEncoder', CrossEncoder)
    cfg = configuration(env['root'])
    vectors = create_publication_vector_store(cfg, administrative=True)
    encoder = RetrievalEncoder(RetrievalProfile(), SentenceTransformer('/opt/polymind/models/embedding', local_files_only=True, device='cpu'))
    ranker = CrossEncoder('/opt/polymind/models/reranker', local_files_only=True, device='cpu')
    def rerank(query, docs, top_k):
        if not docs:return []
        scores = ranker.predict([(query,d['text']) for d in docs])
        return [dict(d,rerank_score=float(score)) for d,score in sorted(zip(docs,scores),key=lambda pair:float(pair[1]),reverse=True)][:top_k]
    publication = env['workflow'].pilot.publication
    publication.vectors, publication.encoder = vectors, encoder
    env['workflow'].pilot.reranker = rerank
    env['chat'].reranker, env['chat'].route = rerank, semantic_route
    env['chat'].memory = RedisMemoryStore(redis.Redis.from_url('redis://redis:6379/0', decode_responses=False,
        socket_connect_timeout=3, socket_timeout=3), 20, 0)
    runner = env['runner']
    def admission_ready():
        with env['runtime'].admission._transaction() as db:
            rows=list(db.execute('SELECT started,active FROM inference_calls WHERE quota=?',(env['runtime'].admission.quota_key,)))
        return not any(r['active'] for r in rows) and (not rows or env['clock'][0] >= max(r['started'] for r in rows)+61)
    runner.admission_ready = admission_ready
    dispatch = Lock(); once = runner.once
    def synchronized_once():
        with dispatch:once()
    runner.once = synchronized_once
    app = create_app(env['runtime'], env['workflow'], runner, chat=env['chat'])
    @app.post('/documents/operator/offline-step')
    def step(request: Request):
        env['workflow'].operator(request.state.principal)
        with dispatch:
            env['clock'][0]+=61;once()
        return {'session':env['session'],'calls':env['http'].calls}
    @app.post('/documents/operator/offline-review')
    def review(request: Request, body: dict):
        env['workflow'].operator(request.state.principal)
        attach_reviews(env,body['evidence'])
        return {'test_reviews_attached':True}
    try:
        uvicorn.run(app,host='0.0.0.0',port=8001,access_log=False,log_level='warning')
    finally:
        vectors.close();bridge_generator.close();external_generator.close();patch.undo()


if __name__ == '__main__':
    main()
