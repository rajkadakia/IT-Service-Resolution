


MAX_INCIDENTS = 2
MAX_CHARS_PER_INCIDENT = 800
MAX_TOTAL_CHARS = 1500


def limit_text(text: str, max_chars: int) -> str:
    return text[:max_chars]


def apply_context_limits(items):
    """
    items: list of dicts with keys:
        - incident_id
        - text
    """
    context = []
    total_chars = 0

    for item in items[:MAX_INCIDENTS]:
        text = limit_text(item["text"], MAX_CHARS_PER_INCIDENT)

        if total_chars + len(text) > MAX_TOTAL_CHARS:
            break

        context.append({
            "incident_id": item["incident_id"],
            "text": text
        })
        total_chars += len(text)

    return context
