"""Content-free operational errors at document service boundaries."""

from typing import Literal

Category = Literal[
    "unsupported_format", "invalid_document", "encrypted_document",
    "source_too_large", "page_limit_exceeded", "extraction_limit_exceeded",
    "extraction_failed", "integrity_error", "storage_error", "object_conflict",
    "object_not_found", "scope_mismatch", "serialization_error", "invalid_reference",
]


class DocumentError(RuntimeError):
    def __init__(self, category: Category):
        self.category = category
        super().__init__(category)
