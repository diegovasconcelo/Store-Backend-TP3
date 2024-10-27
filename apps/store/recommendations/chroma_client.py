import os

import chromadb
from chromadb.config import Settings


DB_PATH = os.getenv("CHROMA_DB_PATH")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")


def get_chroma_client(db_path, collection_name):
    client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(allow_reset=True)
    )
    collection = client.get_or_create_collection(collection_name)
    return client, collection


def reset_collection(client):
    """
        Empties and completely resets the database.
        ⚠️ This is destructive and not reversible.
    """
    client.reset()


client, collection = get_chroma_client(DB_PATH, COLLECTION_NAME)
