from datetime import datetime


def build_grounded_notes(topic: str, context_chunks: list[str]) -> dict:
    """Simple grounded notes formatter for Week 3 scaffold."""
    bullets = []
    for chunk in context_chunks[:8]:
        cleaned = chunk.strip().replace("\n", " ")
        if cleaned:
            bullets.append(f"- {cleaned}")

    return {
        "topic": topic,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "summary": "\n".join(bullets) if bullets else "- No context found for this topic.",
        "grounded": True,
    }
