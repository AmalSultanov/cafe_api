from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.user import (
    get_user_registration_service, get_user_service, get_user_identity_service
)
from src.exceptions.cart import CartAlreadyExistsError
from src.exceptions.user import (
    UserNotFoundError, UserIdentityNotFoundError, UserAlreadyExistsError,
    UserPhoneAlreadyExistsError, NoUserUpdateDataError,
    UserIdentityAlreadyExistsError
)
from src.schemas.common import PaginationParams
from src.schemas.http_error import HTTPError
from src.schemas.user import (
    UserRegister, UserRead, IdentityCheck, UserPutUpdate, UserPatchUpdate,
    IdentityRead, IdentityStatusResponse, PaginatedUserResponse
)
from src.services.user.identity.interface import IUserIdentityService
from src.services.user.interface import IUserService
from src.services.user.registration.interface import IUserRegistrationService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Register a new user with the given information. "
        "An empty cart is automatically created for this user."
    ),
    response_description="Details of the newly registered user",
    responses={
        400: {
            "model": HTTPError,
            "description": (
                "User already exists, identity already exists, "
                "or cart was already created."
            )
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def register(
    user_data: UserRegister,
    service: IUserRegistrationService = Depends(get_user_registration_service)
):
    try:
        return await service.register_user(user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except UserIdentityAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except CartAlreadyExistsError as e:
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
            "description": "User not found with the provided phone number."
        }
    }
)
async def log_in(
    phone_number: str,
    service: IUserService = Depends(get_user_service)
):
    return await service.log_in_user(phone_number)


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
    exists = await service.identity_exists(identity_data)
    return {"status": "registered" if exists else "not_registered"}


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
    try:
        return await service.get_identity(identity_data)
    except UserIdentityNotFoundError as e:
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
    return await service.get_users(pagination_params)


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
    try:
        return await service.get_user(user_id)
    except UserNotFoundError as e:
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
            "description": "Phone number already exists"
        },
        404: {
            "model": HTTPError,
            "description": "User not found"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def update_user(
    user_id: int,
    user_data: UserPutUpdate,
    service: IUserService = Depends(get_user_service)
):
    try:
        return await service.update_user(user_id, user_data)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except UserPhoneAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
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
            "description": "No fields to update or phone number already exists"
        },
        404: {
            "model": HTTPError,
            "description": "User not found"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def partial_update_user(
    user_id: int,
    user_data: UserPatchUpdate,
    service: IUserService = Depends(get_user_service)
):
    try:
        return await service.update_user(user_id, user_data, True)
    except NoUserUpdateDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except UserPhoneAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


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
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
