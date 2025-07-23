from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.dependencies.cart import get_cart_service
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.repositories.user.identity_repository import UserIdentityRepository
from src.repositories.user.interface import IUserRepository
from src.repositories.user.repository import UserRepository
from src.services.cart.interface import ICartService
from src.services.user.identity.interface import IUserIdentityService
from src.services.user.identity.service import UserIdentityService
from src.services.user.interface import IUserService
from src.services.user.registration.interface import IUserRegistrationService
from src.services.user.registration.service import (
    UserRegistrationService
)
from src.services.user.service import UserService


def get_user_identity_repo(
    db: AsyncSession = Depends(get_session)
) -> IUserIdentityRepository:
    return UserIdentityRepository(db)


def get_user_identity_service(
    user_identity_repo: IUserIdentityRepository = Depends(
        get_user_identity_repo
    )
) -> IUserIdentityService:
    return UserIdentityService(user_identity_repo)


def get_user_repo(
    db: AsyncSession = Depends(get_session)
) -> IUserRepository:
    return UserRepository(db)


def get_user_service(
    repository: IUserRepository = Depends(get_user_repo),
    user_identity_service: IUserIdentityService = Depends(
        get_user_identity_service
    )
) -> IUserService:
    return UserService(repository, user_identity_service)


def get_user_registration_service(
    user_service: IUserService = Depends(get_user_service),
    cart_service: ICartService = Depends(get_cart_service)
) -> IUserRegistrationService:
    return UserRegistrationService(user_service, cart_service)
