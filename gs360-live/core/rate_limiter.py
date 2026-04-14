import time
from dataclasses import dataclass


@dataclass
class TokenBucket:
    capacity: int
    refill_rate_per_sec: float
    tokens: float
    last_refill: float

    @classmethod
    def new(cls, capacity: int, refill_rate_per_sec: float):
        now = time.time()
        return cls(capacity, refill_rate_per_sec, float(capacity), now)

    def allow(self, cost: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate_per_sec)
        self.last_refill = now

        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
