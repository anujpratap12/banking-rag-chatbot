from fastapi import APIRouter

from backend.rag.hybrid_retriever import hybrid_search
from backend.rag.prompt_builder import build_prompt
from backend.rag.generator import generate_response

from backend.rag.memory import (
    add_to_memory,
    get_memory
)

router = APIRouter()


@router.post("/chat")
def chat(query: str):

    conversation_history = get_memory()

    # FOLLOW-UP QUESTION DETECTION

    follow_up_keywords = [
        "them",
        "it",
        "those",
        "that",
        "repeat",
        "again",
        "shortly",
        "explain the second one"
    ]

    is_follow_up = any(
        keyword in query.lower()
        for keyword in follow_up_keywords
    )

    # SKIP RETRIEVAL FOR FOLLOW-UP QUESTIONS

    if is_follow_up:

        retrieved_chunks = []

    else:

        retrieved_chunks = hybrid_search(query)

    # BUILD PROMPT

    prompt = build_prompt(
        query,
        retrieved_chunks,
        conversation_history
    )

    # GENERATE RESPONSE

    answer = generate_response(prompt)

    # STORE MEMORY

    add_to_memory(query, answer)

    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }