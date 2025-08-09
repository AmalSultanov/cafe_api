from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.dependencies.message_broker import get_event_publisher
from src.message_broker.publisher.interface import IEventPublisher
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.repositories.user.identity_repository import UserIdentityRepository
from src.repositories.user.interface import IUserRepository
from src.repositories.user.repository import UserRepository
from src.services.user.identity.interface import IUserIdentityService
from src.services.user.identity.service import UserIdentityService
from src.services.user.interface import IUserService
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
    ),
    publisher: IEventPublisher = Depends(get_event_publisher)
) -> IUserService:
    return UserService(repository, user_identity_service, publisher)
