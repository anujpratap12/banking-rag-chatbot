from backend.rag.retriever import load_model
from backend.rag.vector_store import collection


def hybrid_search(query, top_k=4):

    try:

        model = load_model()

        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = results["documents"][0]

        return retrieved_chunks

    except Exception as e:

        print("Retriever Error:", e)

        return []