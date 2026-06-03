import chromadb


CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "knowledge_base"


client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def get_collection():

    return collection


def reset_collection():

    try:

        client.delete_collection(
            COLLECTION_NAME
        )

        print(
            f"🗑️ Deleted collection: "
            f"{COLLECTION_NAME}"
        )

    except Exception:

        pass

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )
