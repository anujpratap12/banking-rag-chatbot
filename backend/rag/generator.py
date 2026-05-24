from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_response(prompt):

    try:

        final_prompt = f"""
You are an AI Banking Support Assistant.

Answer ONLY from the provided retrieved context.

Rules:
1. Do NOT make up information.
2. Do NOT hallucinate.
3. If the answer is not present in the context, say:
   'I could not find this information in the uploaded documents.'
4. Keep answers clear and professional.
5. Give concise responses unless detailed explanation is asked.

Retrieved Context:
{prompt}
"""

        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"Error generating response: {str(e)}"