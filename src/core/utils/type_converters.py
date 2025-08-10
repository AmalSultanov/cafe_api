from pydantic import HttpUrl

from src.core.logging import logger


def url_to_str(image_url: HttpUrl) -> str:
    logger.debug(f"Converting HttpUrl to string: {image_url}")

    try:
        result = str(image_url)
        logger.debug(f"URL converted successfully: {image_url} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to convert URL to string {image_url}: {e}")
        raise
