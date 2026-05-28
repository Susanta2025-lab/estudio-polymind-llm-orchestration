import uuid
from pathlib import Path

from rag.embeddings import get_embedding
from rag.vectordb import collection

DOCS_PATH = Path("data/docs")


def ingest_documents():

    for file in DOCS_PATH.glob("*.txt"):

        text = file.read_text(encoding="utf-8")

        chunks = text.split("\n")

        for chunk in chunks:

            chunk = chunk.strip()

            if not chunk:
                continue

            embedding = get_embedding(chunk)

            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding]
            )

    print("✅ Documents ingested successfully")


if __name__ == "__main__":
    ingest_documents()
