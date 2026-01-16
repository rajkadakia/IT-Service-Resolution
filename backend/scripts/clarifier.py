import os
from groq import Groq

MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_clarifying_question(query: str, categories: list[str]) -> str:
    """
    Ask ONE clarifying question to disambiguate category.
    """

    prompt = f"""
User query:
"{query}"

Possible categories:
{", ".join(categories)}

Ask ONE clarifying question to identify the correct category.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a network support triage assistant. "
                    "Ask ONE clarifying question only. "
                    "No explanations. No solutions. "
                    "The question must be concrete and short. "
                    "Output in the THIRD PERSON (e.g., 'The system needs to know...'). Do NOT use 'I' or 'me'."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()
