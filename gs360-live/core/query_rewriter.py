def hyde_variants(query: str) -> list[str]:
    """Generate retrieval-friendly variants for analytical queries."""
    q = query.strip()
    if not q:
        return []

    return [
        q,
        f"Explain with causes, effects, and examples: {q}",
        f"UPSC analytical framing for: {q}",
    ]
