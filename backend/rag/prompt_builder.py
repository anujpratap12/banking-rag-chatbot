def build_prompt(query, retrieved_chunks, history):

    context = "\n".join(retrieved_chunks[:4])

    return f"""
You are an AI Banking Assistant.

Answer ONLY using the provided context.

Try to infer related meanings carefully.
For example:
- benefits may include cashback or rewards
- eligibility may include salary or income requirements

If answer is not found, say:
'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{query}
"""