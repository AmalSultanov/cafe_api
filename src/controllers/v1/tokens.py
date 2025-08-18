from fastapi import (
    APIRouter, Response, Request, HTTPException, Depends, status
)
from jose.exceptions import JWTError, ExpiredSignatureError

from src.core.config import Settings, get_settings
from src.core.logging import logger
from src.core.utils.jwt import decode_refresh_token, create_access_token
from src.schemas.http_error import HTTPError
from src.schemas.token import AccessTokenResponse

router = APIRouter(prefix="/tokens", tags=["Tokens"])


@router.post(
    "/refresh-access",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Refresh the access token using a valid refresh token stored in the "
        "cookies. This endpoint should be used when the access token expires, "
        "but the refresh token is still valid."
    ),
    response_description="Access token refreshed",
    responses={
        401: {
            "model": HTTPError,
            "description": (
                "Refresh token is missing, invalid, expired, "
                "or of an incorrect type"
            )
        }
    }
)
async def refresh_access_token(
    request: Request,
    response: Response,
    settings: Settings = Depends(get_settings)
):
    logger.info("API request: Refresh access token")
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        logger.warning("API error: Refresh token missing")
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = decode_refresh_token(refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")

        user_id = int(payload["sub"])
        new_access_token = create_access_token(user_id)

        response.set_cookie(
            key="access_token", value=new_access_token,
            max_age=settings.jwt_access_token_cookie_max_age, secure=False,
            httponly=True, samesite="Lax"
        )

        logger.info(
            f"API response: Access token was refreshed for user {user_id}"
        )
        return AccessTokenResponse(status="access_token_refreshed")
    except (ExpiredSignatureError, JWTError) as e:
        logger.warning(f"API error: Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
