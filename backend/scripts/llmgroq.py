import os
from groq import Groq

MODEL = "llama-3.1-8b-instant"


def generate_answer(query: str, context: list[dict], force: bool = False) -> str:
    """
    context: list of dicts with keys:
        - incident_id
        - text
    """

    if force:
        system_prompt = """
You are an expert IT Incident Resolution Assistant.
The user has already answered clarification questions.
You MUST provide the best possible resolution now.
Do NOT ask follow-up questions.
Make reasonable assumptions if information is incomplete.
Be decisive and operational.

**Response Structure & Tone:**
- **Structure:** Use succinct Markdown sections.
  - `### Analysis`: Brief diagnosis of the situation.
  - `### Resolution`: Clear, numbered steps to fix the issue.
  - `### Verification`: Specific command or action to confirm success.
- **Format:** Use nice looking Markdown.
- **Tone:** Professional, precise, and helpful.
"""
    else:
        system_prompt = """
You are an expert IT Incident Resolution Assistant.
Use ONLY the provided context for factual claims.
You may suggest standard validation steps IF clearly labeled as verification.
Do NOT invent new root causes.
If the context is insufficient, state this clearly.

**Response Structure:**
- **Structure:** Use succinct Markdown sections.
  - `### Analysis`: Brief diagnosis based on known incidents.
  - `### Resolution`: Clear, numbered steps to fix the issue.
  - `### Verification`: Specific command or action to confirm success.
- **Format:** Use nice looking Markdown.
- **Tone:** Professional, precise, and helpful.

"""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    context_block = "\n\n".join(
        f"[Incident {c['incident_id']}]\n{c['text']}"
        for c in context
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
User issue:
{query}

Known incidents:
{context_block}
"""
            }
        ],
        temperature=0.2,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    fake_context = [
        {
            "incident_id": "DNS-004",
            "text": "DNS queries timing out due to unreachable DNS server. Resolution: verify connectivity to DNS server and switch to secondary DNS."
        }
    ]

    print("NORMAL:\n")
    print(generate_answer("dns timeout internal app", fake_context))

    print("\nFORCED:\n")
    print(generate_answer("dns timeout internal app", fake_context, force=True))
