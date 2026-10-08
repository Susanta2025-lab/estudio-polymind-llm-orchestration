"""Explicit tokenizer bounds; exact source slices, never tokenizer truncation."""
import math

from config.model_artifacts import EMBEDDING_MODEL
from documents.publication.models import PublicationError


class RetrievalEncoder:
    def __init__(self, profile, model=None):
        if (profile.embedding_model != EMBEDDING_MODEL.identifier
                or profile.embedding_revision != EMBEDDING_MODEL.revision or profile.dimension != 384):
            raise PublicationError('publication_incompatible')
        if model is None:
            from rag.embeddings import get_embedding_model
            model = get_embedding_model()
        self.profile, self.model = profile, model
        self.tokenizer = model.tokenizer
        if (model.max_seq_length < profile.max_tokens
                or model.get_sentence_embedding_dimension() != profile.dimension
                or self.tokenizer.model_max_length < profile.max_tokens):
            raise PublicationError('publication_incompatible')

    def count(self, text):
        return len(self.tokenizer(text, add_special_tokens=True, truncation=False)['input_ids'])

    def validate(self, text):
        if not text or len(text) > self.profile.max_characters or self.count(text) > self.profile.max_tokens:
            raise PublicationError('embedding_limit')

    def split(self, text):
        start = 0
        while start < len(text):
            end = min(len(text), start + self.profile.max_characters)
            # Halving is deterministic and does not assume monotonic WordPiece counts.
            while self.count(text[start:end]) > self.profile.max_tokens:
                end = start + (end - start) // 2
                if end <= start:
                    raise PublicationError('embedding_limit')
            yield start, end, text[start:end]
            start = end

    def embed(self, text):
        self.validate(text)
        result = self.model.encode(text, normalize_embeddings=True).tolist()
        if len(result) != self.profile.dimension or not all(math.isfinite(x) for x in result):
            raise PublicationError('publication_write_failure')
        return result
