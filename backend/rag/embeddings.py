model = None


def load_model():

    global model

    if model is None:

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def generate_embeddings(chunks):

    model_instance = load_model()

    embeddings = model_instance.encode(
        chunks
    ).tolist()

    return embeddings