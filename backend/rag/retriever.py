from backend.rag.vector_store import collection

model = None


def load_model():

    global model

    if model is None:

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def retrieve_chunks(query, top_k=5):

    model_instance = load_model()

    query_embedding = model_instance.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = results["documents"][0]

    return retrieved_chunks