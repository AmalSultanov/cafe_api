from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import get_user_service, get_user_identity_service
from src.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from src.schemas.user import (
    UserRegister, UserRead, UserUpdate, UserPartialUpdate, IdentityCheck
)
from src.services.user import UserService
from src.services.user_identity import UserIdentityService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserRead)
async def register(
    user_data: UserRegister, service: UserService = Depends(get_user_service)
):
    try:
        return await service.create_user(user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/log-in")
async def log_in(
    phone_number: str,
    service: UserService = Depends(get_user_service)
):
    return await service.log_in_user(phone_number)


@router.get("/is-registered")
async def is_registered(
    identity_data: IdentityCheck = Depends(IdentityCheck),
    service: UserIdentityService = Depends(get_user_identity_service)
):
    is_user_registered = await service.is_registered(identity_data)
    return {"registered": is_user_registered}


@router.get("", response_model=list[UserRead])
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.update_user(user_id, user_data)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.patch("/{user_id}", response_model=UserRead)
async def partial_update_user(
    user_id: int,
    user_data: UserPartialUpdate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.partial_update_user(user_id, user_data)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
