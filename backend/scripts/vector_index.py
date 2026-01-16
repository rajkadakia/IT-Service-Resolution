import faiss
import numpy as np
from pathlib import Path
from backend.scripts.embedding_store import load_embedding_store


BASE_DIR = Path(__file__).resolve().parent.parent  
INDEX_PATH = BASE_DIR / "faiss_index.bin"

def build_faiss_index():
    store = load_embedding_store()

    embeddings = np.array([item["embedding"] for item in store]).astype("float32")
    dim = embeddings.shape[1]

    
    index = faiss.IndexFlat(dim, faiss.METRIC_L1)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))
    print(f"FAISS index built with {index.ntotal} vectors.")

def load_faiss_index():
    index = faiss.read_index(str(INDEX_PATH))
    store = load_embedding_store()
    return index, store

if __name__ == "__main__":
    build_faiss_index()
