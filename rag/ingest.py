import uuid
from pathlib import Path

from rag.chunking import chunk_text
from rag.embeddings import get_embedding
from rag.vectordb import collection

from rag.loaders.pdf_loader import load_pdf
from rag.loaders.text_loader import load_text

DOCS_PATH = Path("data/docs")


def load_document(path: Path):

    if path.suffix == ".pdf":
        return load_pdf(str(path))

    elif path.suffix == ".txt":
        return load_text(str(path))

    return None


def ingest_documents():

    for file in DOCS_PATH.iterdir():

        if not file.is_file():
            continue

        text = load_document(file)

        if not text:
            continue

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            embedding = get_embedding(chunk)

            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": file.name,
                    "chunk_id": i
                }]
            )

        print(f"✅ Ingested: {file.name}")


if __name__ == "__main__":
    ingest_documents()
