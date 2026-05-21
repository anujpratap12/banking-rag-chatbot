from sentence_transformers import SentenceTransformer
from backend.rag.vector_store import collection

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query, top_k=3):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = results["documents"][0]

    return retrieved_chunks