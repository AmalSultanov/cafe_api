from datetime import datetime, timedelta
from jose import jwt

from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()


def create_access_token(subject: int) -> str:
    logger.debug(f"Creating access token for user {subject}")
    expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    logger.debug(f"Returning access token for user {subject}")
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(subject: int) -> str:
    logger.debug(f"Creating refresh token for user {subject}")
    try:
        expires_delta = timedelta(days=settings.jwt_refresh_token_expire_days)
        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }

        token = jwt.encode(
            payload,
            settings.jwt_refresh_secret_key,
            algorithm=settings.jwt_algorithm
        )
        logger.debug(f"Refresh token created successfully for user {subject}")
        return token
    except Exception as e:
        logger.error(f"Failed to create refresh token for user {subject}: {e}")
        raise


def decode_access_token(token: str) -> dict:
    logger.debug("Decoding access token")
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        logger.debug(
            f"Access token decoded successfully for user {payload.get('sub')}"
        )
        return payload
    except Exception as e:
        logger.error(f"Failed to decode access token: {e}")
        raise


def decode_refresh_token(token: str) -> dict:
    logger.debug("Decoding refresh token")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_refresh_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        logger.debug(
            f"Refresh token decoded successfully for user {payload.get('sub')}"
        )
        return payload
    except Exception as e:
        logger.error(f"Failed to decode refresh token: {e}")
        raise
