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


@dataclass(frozen=True)
class VectorMatch:
    document: str
    metadata: Dict[str, Any]
    distance: float


@dataclass(frozen=True)
class VectorDocument:
    document: str
    metadata: Dict[str, Any]


class VectorStore(Protocol):
    provider: str

    def similarity_search(self, embedding: Sequence[float], limit: int) -> List[VectorMatch]: ...
    def list_documents(self) -> List[VectorDocument]: ...
    def check_readiness(self) -> VectorReadiness: ...
    def close(self) -> None: ...


class MutableVectorStore(VectorStore, Protocol):
    def upsert(self, ids: Sequence[str], documents: Sequence[str], embeddings: Sequence[Sequence[float]], metadatas: Sequence[Dict[str, Any]]) -> None: ...
    def reset(self) -> None: ...

