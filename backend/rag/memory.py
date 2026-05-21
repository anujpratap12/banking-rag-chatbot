chat_memory = []


def add_to_memory(user_query, bot_response):

    chat_memory.append({
        "user": user_query,
        "assistant": bot_response
    })

    # keep only last 5 conversations
    if len(chat_memory) > 5:
        chat_memory.pop(0)


def get_memory():

    conversation = ""

    for chat in chat_memory:

        conversation += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

    return conversation