from datetime import date


FREEZE_DATE = date(2026, 6, 23)


def is_feature_allowed(today: date, is_bugfix: bool) -> bool:
    if is_bugfix:
        return True
    return today <= FREEZE_DATE
