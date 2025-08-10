from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.core.config import Settings, get_settings
from src.core.dependencies.user import (
    get_user_service, get_user_identity_service
)
from src.core.logging import logger
from src.exceptions.cart import CartAlreadyExistsError
from src.exceptions.user import (
    UserNotFoundError, UserIdentityNotFoundError, UserPhoneAlreadyExistsError,
    NoUserUpdateDataError, UserIdentityAlreadyExistsError, UserPhoneError,
    UserProviderIdAlreadyExistsError
)
from src.schemas.common import PaginationParams
from src.schemas.http_error import HTTPError
from src.schemas.user import (
    UserRegister, UserRead, IdentityCheck, UserPutUpdate, UserPatchUpdate,
    IdentityRead, IdentityStatusResponse, PaginatedUserResponse,
    UserWithTokens, LogoutResponse
)
from src.services.user.identity.interface import IUserIdentityService
from src.services.user.interface import IUserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead | UserWithTokens,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Create a new user account with the provided registration data. If "
        "the request comes from a web client, access and refresh JWT tokens "
        "will be generated and returned. Otherwise, only user information is "
        "returned. An empty cart is also created for the new user as part of "
        "the registration process."
    ),
    response_description="Details of the newly registered user",
    responses={
        400: {
            "model": HTTPError,
            "description": "User phone number does not consist of all numbers"
        },
        409: {
            "model": HTTPError,
            "description": (
                "User already exists, user phone number exists, "
                "or cart was already created"
            )
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def register(
    user_data: UserRegister,
    response: Response,
    service: IUserService = Depends(get_user_service),
    settings: Settings = Depends(get_settings)
):
    logger.info(
        f"User registration request for provider: {user_data.provider}, "
        f"username: {user_data.username}"
    )

    try:
        result = await service.create_user(user_data)

        if isinstance(result, UserWithTokens):
            response.set_cookie(
                key="access_token", value=result.access_token,
                max_age=settings.jwt_access_token_cookie_max_age, secure=True,
                httponly=True, samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token", value=result.refresh_token,
                max_age=settings.jwt_refresh_token_cookie_max_age, secure=True,
                httponly=True, samesite="Lax"
            )
            logger.info(f"User registered with tokens for web platform")
        else:
            logger.info(f"User registered for {user_data.provider} platform")

        return result
    except (
        UserProviderIdAlreadyExistsError, UserIdentityAlreadyExistsError,
        UserPhoneAlreadyExistsError, CartAlreadyExistsError
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )
    except UserPhoneError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post(
    "/log-in",
    response_model=UserRead,
    description=(
        "Log in a user using their phone number. Returns the user if found."
    ),
    response_description="Logged-in user",
    responses={
        404: {
            "model": HTTPError,
            "description": "User not found with the provided phone number"
        }
    }
)
async def log_in(
    phone_number: str,
    service: IUserService = Depends(get_user_service)
):
    logger.info(f"API request: User login with phone number: {phone_number}")
    try:
        result = await service.log_in_user(phone_number)
        logger.info(f"API response: User login for phone: {phone_number}")
        return result
    except Exception as e:
        logger.error(
            f"API error: User login failed for phone {phone_number}: {e}"
        )
        raise


@router.get(
    "/check-identity",
    response_model=IdentityStatusResponse,
    description="Check if a user identity (e.g., Telegram, Web) exists in db.",
    response_description="Identity existence status"
)
async def check_identity_exists(
    identity_data: IdentityCheck = Depends(IdentityCheck),
    service: IUserIdentityService = Depends(get_user_identity_service)
):
    logger.info(
        f"API request: Check identity exists for "
        f"{identity_data.provider}: {identity_data.username}"
    )
    try:
        exists = await service.identity_exists(identity_data)
        status = "registered" if exists else "not_registered"
        logger.info(
            f"API response: Identity check result for "
            f"{identity_data.username}: {status}"
        )
        return {"status": status}
    except Exception as e:
        logger.error(
            f"API error: Identity check failed for {identity_data.username}: {e}"
        )
        raise


@router.get(
    "/by-provider",
    response_model=IdentityRead,
    description="Fetch the user identity based on provider and provider ID.",
    response_description="User identity details",
    responses={
        404: {
            "model": HTTPError,
            "description": "User identity not found"
        }
    }
)
async def get_user_by_provider(
    identity_data: IdentityCheck = Depends(IdentityCheck),
    service: IUserIdentityService = Depends(get_user_identity_service)
):
    logger.info(
        f"API request: Get user by provider "
        f"{identity_data.provider}: {identity_data.username}"
    )
    try:
        result = await service.get_identity(identity_data)
        logger.info(
            f"API response: User found for "
            f"{identity_data.provider}: {identity_data.username}"
        )
        return result
    except UserIdentityNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get(
    "",
    response_model=PaginatedUserResponse,
    description=(
        "Retrieve a paginated list of all registered users. Supports "
        "`page` (page number) and `per_page` (page size) query parameters."
    ),
    response_description="Paginated list of users"
)
async def get_users(
    pagination_params: PaginationParams = Depends(PaginationParams),
    service: IUserService = Depends(get_user_service)
):
    logger.info(
        f"API request: Get users - page: {pagination_params.page}, "
        f"per_page: {pagination_params.per_page}"
    )
    try:
        result = await service.get_users(pagination_params)
        logger.info(f"API response: Retrieved {len(result.users)} users")
        return result
    except Exception as e:
        logger.error(f"API error: Failed to get users: {e}")
        raise


@router.get(
    "/{user_id}",
    response_model=UserRead,
    description="Fetch details of a specific user by their ID.",
    response_description="User details",
    responses={
        404: {
            "model": HTTPError,
            "description": "User not found"
        }
    }
)
async def get_user(
    user_id: int,
    service: IUserService = Depends(get_user_service)
):
    logger.info(f"API request: Get user {user_id}")
    try:
        result = await service.get_user(user_id)
        logger.info(f"API response: User {user_id} was retrieved")
        return result
    except UserNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.put(
    "/{user_id}",
    response_model=UserRead,
    description="Update the full user information for a specific user.",
    response_description="Updated user details",
    responses={
        400: {
            "model": HTTPError,
            "description": "Phone number should contain only numbers"
        },
        404: {
            "model": HTTPError,
            "description": "User not found"
        },
        409: {
            "model": HTTPError,
            "description": "Phone number already exists"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def update_user(
    user_id: int,
    user_data: UserPutUpdate,
    service: IUserService = Depends(get_user_service)
):
    logger.info(f"API request: Update user {user_id}")
    try:
        result = await service.update_user(user_id, user_data)
        logger.info(f"API response: User {user_id} was updated")
        return result
    except UserPhoneError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except UserNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except UserPhoneAlreadyExistsError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    description=(
        "Update one or more fields of a specific user. "
        "Only the fields that need to be updated must be provided."
    ),
    response_description="Updated user details",
    responses={
        400: {
            "model": HTTPError,
            "description": (
                "No fields to update or "
                "phone number does not consist of all numbers"
            )
        },
        404: {
            "model": HTTPError,
            "description": "User not found"
        },
        409: {
            "model": HTTPError,
            "description": "Phone number already exists"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def partial_update_user(
    user_id: int,
    user_data: UserPatchUpdate,
    service: IUserService = Depends(get_user_service)
):
    logger.info(f"API request: Partial update user {user_id}")
    try:
        result = await service.update_user(user_id, user_data, True)
        logger.info(f"API response: User {user_id} was partially updated")
        return result
    except (UserPhoneError, NoUserUpdateDataError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except UserNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except UserPhoneAlreadyExistsError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.post(
    "/{user_id}/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    description="Logout user",
    response_description="Logout confirmation",
    responses={
        400: {
            "model": HTTPError,
            "description": "Invalid refresh token"
        }
    }
)
async def logout(
    response: Response
):
    logger.info("API request: User logout")
    try:
        response.delete_cookie(
            key="access_token", httponly=True, secure=True, samesite="Lax"
        )
        response.delete_cookie(
            key="refresh_token", httponly=True, secure=True, samesite="Lax"
        )
        logger.info("API response: User logged out")
        return LogoutResponse(message="Successfully logged out")
    except Exception as e:
        logger.error(f"API error: Logout failed: {e}")
        raise


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a user by their ID.",
    response_description="User successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "User not found"
        }
    }
)
async def delete_user(
    user_id: int,
    service: IUserService = Depends(get_user_service)
):
    logger.info(f"API request: Delete user {user_id}")
    try:
        await service.delete_user(user_id)
        logger.info(f"API response: User {user_id} was deleted")
    except UserNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
