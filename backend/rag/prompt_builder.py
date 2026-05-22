def build_prompt(query, retrieved_chunks, history):

    context = "\n".join(retrieved_chunks[:4])

    return f"""
You are an AI Document Assistant.

Answer ONLY from the provided context.

If answer is not present, say:
'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{query}
"""