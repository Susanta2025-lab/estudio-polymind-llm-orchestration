"""Replaceable native parser runner; application limits are not a process sandbox."""

from contextvars import ContextVar
from dataclasses import dataclass
from io import BytesIO
import logging
import sys
from typing import Protocol

import pypdf
from pypdf import PdfReader
from documents.config import ExtractionSettings
from documents.errors import DocumentError

PARSER_VERSION = f"pypdf/{pypdf.__version__}"
_suppress = ContextVar("document_parser_diagnostics", default=False)


class _ContentFree(logging.Filter):
    def filter(self, record):
        return not _suppress.get()


# pypdf emits diagnostics from module-named loggers. Suppress only this runner's
# context, preserving legacy RAG diagnostics and concurrent unrelated operations.
_filter = _ContentFree()
for _module in tuple(sys.modules):
    if _module == "pypdf" or _module.startswith("pypdf."):
        logging.getLogger(_module).addFilter(_filter)


@dataclass(frozen=True)
class ParsedPage:
    ordinal: int
    text: str = ""
    label: str | None = None
    width: float | None = None
    height: float | None = None
    rotation: int | None = None
    has_images: bool | None = None
    has_graphics: bool | None = None
    failed: bool = False


class ParserRunner(Protocol):
    version: str

    def parse(self, data: bytes, limits: ExtractionSettings) -> tuple[ParsedPage, ...]: ...


class NativePdfRunner:
    version = PARSER_VERSION

    def parse(self, data: bytes, limits: ExtractionSettings) -> tuple[ParsedPage, ...]:
        if len(data) > limits.max_source_bytes:
            raise DocumentError("source_too_large")
        token = _suppress.set(True)
        try:
            reader = PdfReader(BytesIO(data), strict=True)
            if reader.is_encrypted:
                raise DocumentError("encrypted_document")
            count = len(reader.pages)
            if count > limits.max_pages:
                raise DocumentError("page_limit_exceeded")
            if not count:
                raise DocumentError("invalid_document")
            labels = reader.page_labels if "/PageLabels" in reader.root_object else None
            pages, characters = [], 0
            for index in range(count):
                try:
                    page = reader.pages[index]
                    text = page.extract_text() or ""
                    characters += len(text)
                    if characters > limits.max_characters:
                        raise DocumentError("extraction_limit_exceeded")
                    # Do not decode images. Inline/XObject graphics and drawing
                    # operations count as graphics even if image classification is unknown.
                    resources = page.get("/Resources")
                    resources = resources.get_object() if resources is not None else {}
                    objects = resources.get("/XObject", {}).get_object() if "/XObject" in resources else {}
                    images = any(obj.get_object().get("/Subtype") == "/Image" for obj in objects.values())
                    contents = page.get_contents()
                    ops = contents.operations if contents is not None else ()
                    images = images or any(op == b"INLINE IMAGE" for _, op in ops)
                    graphics = any(op in (b"Do", b"INLINE IMAGE", b"S", b"s", b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*") for _, op in ops)
                    pages.append(ParsedPage(index + 1, text, labels[index] if labels else None,
                                            float(page.mediabox.width), float(page.mediabox.height),
                                            int(page.rotation), images, graphics))
                except DocumentError:
                    raise
                except Exception:
                    # Account for failed pages; never silently omit them.
                    pages.append(ParsedPage(index + 1, failed=True))
            return tuple(pages)
        except DocumentError:
            raise
        except Exception:
            raise DocumentError("invalid_document") from None
        finally:
            _suppress.reset(token)
