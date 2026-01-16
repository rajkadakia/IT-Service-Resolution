from sentence_transformers import SentenceTransformer
from backend.scripts.vector_index import load_faiss_index
from backend.scripts.limiter import apply_context_limits


try:
    
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
except Exception:
    
    print("Local model not found, attempting download...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

TOP_K = 2
def retrieve_context(query: str, category: str | None = None):
    index, store = load_faiss_index()

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    distances, indices = index.search(query_embedding, TOP_K)

    matched = []
    categories = set()

    for idx in indices[0]:
        item = store[idx]
        matched.append(item)
        categories.add(item["category"])

    confidence = 1 / (1 + distances[0][0])  

    return {
        "results": apply_context_limits(matched),
        "confidence": confidence,
        "categories": list(categories)
    }



def main():
    query = input("Describe the issue: ")
    context = retrieve_context(query)

    print("\nContext (via limiter.py):\n")
    for c in context:
        print(f"Incident ID: {c['incident_id']}")
        print(c["text"])
        print("-" * 40)


if __name__ == "__main__":
    main()
