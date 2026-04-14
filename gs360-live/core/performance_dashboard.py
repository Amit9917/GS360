from dataclasses import dataclass


@dataclass
class QuizResult:
    user_id: str
    quiz_id: str
    score_percent: float


class PerformanceDashboard:
    def __init__(self):
        self.results = []

    def add_result(self, result: QuizResult):
        self.results.append(result)

    def summary(self, user_id: str) -> dict:
        rows = [r for r in self.results if r.user_id == user_id]
        if not rows:
            return {"attempts": 0, "avg_score": 0.0}

        avg = sum(r.score_percent for r in rows) / len(rows)
        return {"attempts": len(rows), "avg_score": round(avg, 2)}
