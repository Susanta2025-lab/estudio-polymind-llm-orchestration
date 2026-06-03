import uuid
from pathlib import Path

from rag.chunking import chunk_text
from rag.embeddings import get_embedding
from rag.vectordb import collection

from rag.loaders.pdf_loader import load_pdf
from rag.loaders.text_loader import load_text

DOCS_PATH = Path("data/docs")


def load_document(path: Path):

    if path.suffix.lower() == ".pdf":
        return load_pdf(str(path))

    elif path.suffix.lower() == ".txt":
        return load_text(str(path))

    return None


def ingest_documents():

    total_documents = 0
    total_chunks = 0

    print("\n🚀 Starting document ingestion...\n")

    for file in DOCS_PATH.iterdir():

        if not file.is_file():
            continue

        text = load_document(file)

        if not text:

            print(f"⚠️ Skipped: {file.name}")

            continue

        chunks = chunk_text(text)

        print(
            f"📄 {file.name} | "
            f"{len(chunks)} chunks"
        )

        for i, chunk in enumerate(chunks):

            embedding = get_embedding(chunk)

            collection.add(
                ids=[str(uuid.uuid4())],

                documents=[chunk],

                embeddings=[embedding],

                metadatas=[{
                    "source": file.name,
                    "chunk_id": i,
                    "file_type": file.suffix.lower(),
                    "chunk_length": len(chunk)
                }]
            )

            total_chunks += 1

        total_documents += 1

        print(
            f"✅ Ingested: {file.name}"
        )

    print("\n📊 Ingestion Summary")
    print(
        f"Documents: {total_documents}"
    )
    print(
        f"Chunks: {total_chunks}"
    )
    print("🎉 Ingestion complete!\n")


if __name__ == "__main__":

    ingest_documents()
