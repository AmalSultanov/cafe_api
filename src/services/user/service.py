from sqlalchemy.exc import IntegrityError

from src.exceptions.user import (
    UserNotFoundError, UserPhoneAlreadyExistsError, NoUserUpdateDataError,
    UserIdentityAlreadyExistsError, UserProviderIdAlreadyExistsError
)
from src.message_broker.config import broker
from src.message_broker.events.user import UserCreatedEvent
from src.message_broker.publisher import EventPublisher
from src.message_broker.topics import TOPIC_USER_CREATED
from src.repositories.user.interface import IUserRepository
from src.schemas.common import PaginationParams
from src.schemas.user import (
    UserRegister, UserPutUpdate, UserPatchUpdate, UserRead, IdentityCheck,
    IdentityCreate, PaginatedUserResponse, ProviderEnum, UserWithTokens
)
from src.services.user.identity.interface import IUserIdentityService
from src.core.utils.jwt import create_access_token, create_refresh_token


class UserService:
    def __init__(
        self,
        repository: IUserRepository,
        identity_service: IUserIdentityService
    ) -> None:
        self.repository = repository
        self.identity_service = identity_service

    async def create_user(
        self, user_data: UserRegister
    ) -> UserRead | UserWithTokens:
        identity_check = IdentityCheck(
            provider=user_data.provider,
            provider_id=user_data.provider_id,
            username=user_data.username
        )

        if await self.identity_service.identity_exists(identity_check):
            raise UserProviderIdAlreadyExistsError(
                user_data.provider_id, user_data.provider
            )

        if await self.identity_service.username_exists(identity_check):
            raise UserIdentityAlreadyExistsError(
                user_data.username, user_data.provider
            )

        try:
            user = await self.repository.create(user_data.model_dump(
                exclude={"provider", "provider_id", "username"}
            ))
        except IntegrityError:
            raise UserPhoneAlreadyExistsError(user_data.phone_number)

        new_identity = IdentityCreate(**user_data.model_dump())

        try:
            await self.identity_service.create_identity(user.id, new_identity)
        except UserIdentityAlreadyExistsError:
            raise

        event = UserCreatedEvent(user_id=user.id)
        publisher = EventPublisher(broker)

        await publisher.publish(TOPIC_USER_CREATED, event.model_dump())

        if user_data.provider == ProviderEnum.web:
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            return UserWithTokens(
                user=UserRead.model_validate(user),
                access_token=access_token,
                refresh_token=refresh_token
            )
        return UserRead.model_validate(user)

    async def log_in_user(self, phone_number: str):
        # ...SMS verification...
        ...

    async def get_users(
        self, pagination_params: PaginationParams
    ) -> PaginatedUserResponse:
        offset = (pagination_params.page - 1) * pagination_params.per_page
        users = await self.repository.get_all(
            pagination_params.per_page, offset
        )
        total = await self.repository.get_total_count()
        total_pages = (
            (total + pagination_params.per_page - 1) // pagination_params.per_page
        )

        return PaginatedUserResponse(
            total=total,
            page=pagination_params.page,
            total_pages=total_pages,
            items=[UserRead.model_validate(user) for user in users]
        )

    async def get_user(self, user_id: int) -> UserRead | None:
        user = await self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)
        return UserRead.model_validate(user)

    async def update_user(
        self,
        user_id: int,
        user_data: UserPutUpdate | UserPatchUpdate,
        is_partial: bool = False
    ) -> UserRead | None:
        new_data = (
            user_data.model_dump(exclude_unset=True) if is_partial
            else user_data.model_dump()
        )

        if not new_data:
            raise NoUserUpdateDataError()
        if not await self.repository.get_by_id(user_id):
            raise UserNotFoundError(user_id)

        try:
            upd_user = await self.repository.update(user_id, new_data)
        except IntegrityError:
            raise UserPhoneAlreadyExistsError(new_data["phone_number"])
        return UserRead.model_validate(upd_user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return await self.repository.delete(user_id)
