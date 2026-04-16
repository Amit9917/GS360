import random


class QuizEngine:
    """Build quizzes from question banks with optional topic filtering."""

    def __init__(self, question_bank: list[dict]):
        self.question_bank = question_bank

    def generate(self, size: int = 10, topic: str | None = None, seed: int = 42) -> list[dict]:
        pool = self.question_bank
        if topic:
            pool = [q for q in pool if topic in q.get("topics", [])]

        if not pool:
            return []

        random.seed(seed)
        if len(pool) <= size:
            return pool
        return random.sample(pool, size)
