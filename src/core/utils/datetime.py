from datetime import datetime

from src.core.logging import logger


def strip_timezone(dt: datetime) -> datetime:
    logger.debug(f"Stripping timezone from datetime: {dt}")

    try:
        if dt and dt.tzinfo:
            result = dt.astimezone(tz=None).replace(tzinfo=None)
            logger.debug(f"Timezone stripped successfully: {dt} -> {result}")
            return result

        logger.debug(f"No timezone to strip from: {dt}")
        return dt
    except Exception as e:
        logger.error(f"Failed to strip timezone from {dt}: {e}")
        raise
