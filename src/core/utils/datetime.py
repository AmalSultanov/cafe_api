from datetime import datetime


def strip_timezone(dt: datetime) -> datetime:
    if dt and dt.tzinfo:
        return dt.astimezone(tz=None).replace(tzinfo=None)
    return dt
