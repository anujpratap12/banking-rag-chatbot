def build_prompt(
    query,
    retrieved_chunks,
    conversation_history
):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI Banking Support Assistant.

Use:
1. Retrieved context
2. Previous conversation history

to answer the user question.

-----------------------------------
PREVIOUS CONVERSATION:
{conversation_history}
-----------------------------------

RETRIEVED CONTEXT:
{context}
-----------------------------------

CURRENT USER QUESTION:
{query}

Instructions:
- Answer professionally.
- Use previous conversation if needed.
- Answer ONLY from context/history.
- If answer is unavailable, say:
'I could not find this information in the uploaded documents.'
"""

    return prompt