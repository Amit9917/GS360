def merge_rank(vector_hits: list[dict], keyword_hits: list[dict], top_k: int = 5) -> list[dict]:
    """Simple hybrid ranking by summed normalized scores."""
    merged = {}

    for item in vector_hits:
        key = item["id"]
        merged.setdefault(key, {"id": key, "score": 0.0, "text": item.get("text", "")})
        merged[key]["score"] += float(item.get("score", 0)) * 0.6

    for item in keyword_hits:
        key = item["id"]
        merged.setdefault(key, {"id": key, "score": 0.0, "text": item.get("text", "")})
        merged[key]["score"] += float(item.get("score", 0)) * 0.4

    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]
