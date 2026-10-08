"""Provider-neutral vector storage boundary for retrieval and administration."""

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol, Sequence


class VectorStoreError(RuntimeError):
    """Sanitized operational vector-store failure."""

    def __init__(self, category: str):
        self.category = category
        super().__init__(category)


@dataclass(frozen=True)
class VectorReadiness:
    provider: str
    ready: bool
    status: str
    corpus_version: str | None = None


@dataclass(frozen=True)
class VectorMatch:
    document: str
    metadata: Dict[str, Any]
    distance: float


@dataclass(frozen=True)
class VectorDocument:
    document: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class VectorFilter:
    generation: str
    document_ids: tuple[str, ...] = ()


class VectorStore(Protocol):
    provider: str

    def similarity_search(self, embedding: Sequence[float], limit: int, *, scope: VectorFilter | None = None) -> List[VectorMatch]: ...
    def list_documents(self, *, scope: VectorFilter | None = None) -> List[VectorDocument]: ...
    def check_readiness(self) -> VectorReadiness: ...
    def corpus_version(self) -> str | None: ...
    def close(self) -> None: ...


class MutableVectorStore(VectorStore, Protocol):
    def upsert(self, ids: Sequence[str], documents: Sequence[str], embeddings: Sequence[Sequence[float]], metadatas: Sequence[Dict[str, Any]]) -> None: ...
    def reset(self) -> None: ...
    def publish_corpus_version(self, version: str) -> None: ...
