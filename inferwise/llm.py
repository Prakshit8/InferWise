import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "llama-3.1-8b-instant"
)


def call_llm(messages, model=None):
    """
    Calls Groq LLM and returns response text.
    """

    model = model or DEFAULT_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return {
        "content": response.choices[0].message.content,
        "model": model,
        "usage": response.usage,
    }