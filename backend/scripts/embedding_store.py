from sentence_transformers import SentenceTransformer
import json
from pathlib import Path
from backend.scripts.chunker import get_all_chunks

BASE_DIR = Path(__file__).resolve().parent.parent  
STORE_PATH = BASE_DIR / "embeddings_store.json"

def build_embedding_store():
    chunks = get_all_chunks()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    store = []

    for chunk in chunks:
        embedding = model.encode(chunk["text"])

        store.append({
            "incident_id": chunk["incident_id"],
            "category": chunk["category"],
            "chunk_type": chunk["chunk_type"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(str(STORE_PATH), "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

    print(f"Embedding store created with {len(store)} chunks.")


def load_embedding_store():
    with open(str(STORE_PATH), "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    build_embedding_store()
