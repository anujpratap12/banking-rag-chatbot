from rank_bm25 import BM25Okapi
from backend.rag.vector_store import collection


def hybrid_search(query, top_k=2):

    try:

        # Semantic Search
        semantic_results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        semantic_chunks = semantic_results["documents"][0]

        # Get All Docs
        all_docs = collection.get()["documents"]

        if not all_docs:
            return semantic_chunks

        # BM25
        tokenized_docs = [
            doc.split() for doc in all_docs
        ]

        bm25 = BM25Okapi(tokenized_docs)

        tokenized_query = query.split()

        bm25_results = bm25.get_top_n(
            tokenized_query,
            all_docs,
            n=top_k
        )

        # Merge Results
        combined_results = list(
            set(semantic_chunks + bm25_results)
        )

        return combined_results[:top_k]

    except Exception as e:

        print("Hybrid Search Error:", e)

        return []