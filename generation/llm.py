import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def call_llm(prompt):
    """
    Sends a RAG prompt to OpenAI and returns the generated answer.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error calling LLM: {str(e)}"