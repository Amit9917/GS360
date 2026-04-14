from dataclasses import dataclass


@dataclass
class ServiceStatus:
    name: str
    healthy: bool
    detail: str


def summarize(statuses: list[ServiceStatus]) -> dict:
    total = len(statuses)
    healthy = sum(1 for s in statuses if s.healthy)
    return {
        "total": total,
        "healthy": healthy,
        "degraded": total - healthy,
        "all_green": healthy == total,
        "services": [s.__dict__ for s in statuses],
    }
