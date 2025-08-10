from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
from src.exceptions.user import (
    UserNotFoundError, UserPhoneAlreadyExistsError, NoUserUpdateDataError,
    UserIdentityAlreadyExistsError, UserProviderIdAlreadyExistsError
)
from src.message_broker.events.user import UserCreatedEvent
from src.message_broker.publisher.interface import IEventPublisher
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
        identity_service: IUserIdentityService,
        publisher: IEventPublisher
    ) -> None:
        self.repository = repository
        self.identity_service = identity_service
        self.publisher = publisher

    async def create_user(
        self, user_data: UserRegister
    ) -> UserRead | UserWithTokens:
        logger.info(
            f"User service: Creating user with provider: {user_data.provider}, "
            f"username: {user_data.username}"
        )

        identity_check = IdentityCheck(
            provider=user_data.provider,
            provider_id=user_data.provider_id,
            username=user_data.username
        )

        if await self.identity_service.identity_exists(identity_check):
            logger.warning(
                f"User service: Provider ID {user_data.provider_id} "
                f"already exists for {user_data.provider}"
            )
            raise UserProviderIdAlreadyExistsError(
                user_data.provider_id, user_data.provider
            )

        if await self.identity_service.username_exists(identity_check):
            logger.warning(
                f"User service: Username {user_data.username} already exists "
                f"for {user_data.provider}"
            )
            raise UserIdentityAlreadyExistsError(
                user_data.username, user_data.provider
            )

        try:
            user = await self.repository.create(user_data.model_dump(
                exclude={"provider", "provider_id", "username"}
            ))
            logger.info(
                f"User service: User created successfully with ID: {user.id}"
            )
        except IntegrityError:
            logger.error(
                f"User service: User creation failed due to integrity error"
            )
            raise UserPhoneAlreadyExistsError(user_data.phone_number)

        new_identity = IdentityCreate(**user_data.model_dump())

        try:
            await self.identity_service.create_identity(user.id, new_identity)
            logger.info(
                f"User service: User identity was created for user "
                f"{user.id} with provider {user_data.provider}"
            )
        except UserIdentityAlreadyExistsError:
            logger.error(
                f"User service: Identity creation failed for user {user.id}"
            )
            raise

        event = UserCreatedEvent(user_id=user.id)
        await self.publisher.publish(TOPIC_USER_CREATED, event.model_dump())
        logger.info(
            f"User service: UserCreatedEvent was published for user {user.id}"
        )

        if user_data.provider == ProviderEnum.web:
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            logger.info(
                f"User service: JWT tokens generated for web user {user.id}"
            )

            return UserWithTokens(
                user=UserRead.model_validate(user),
                access_token=access_token,
                refresh_token=refresh_token
            )

        logger.info(
            f"User service: User {user.id} was created for {user_data.provider}"
        )
        return UserRead.model_validate(user)

    async def log_in_user(self, phone_number: str):
        # ...SMS verification...
        ...

    async def get_users(
        self, pagination_params: PaginationParams
    ) -> PaginatedUserResponse:
        logger.info(
            f"User service: Fetching users - page: "
            f"{pagination_params.page}, per_page: {pagination_params.per_page}"
        )
        offset = (pagination_params.page - 1) * pagination_params.per_page
        users = await self.repository.get_all(
            pagination_params.per_page, offset
        )
        total = await self.repository.get_total_count()
        total_pages = (
            (total + pagination_params.per_page - 1) // pagination_params.per_page
        )
        logger.info(
            f"User service: Retrieved {len(users)} users out of {total} total users"
        )

        return PaginatedUserResponse(
            total=total,
            page=pagination_params.page,
            total_pages=total_pages,
            items=[UserRead.model_validate(user) for user in users]
        )

    async def get_user(self, user_id: int) -> UserRead | None:
        logger.debug(
            f"User service: Getting user {user_id}"
        )
        user = await self.repository.get_by_id(user_id)

        if not user:
            logger.warning(f"User service: User {user_id} was not found")
            raise UserNotFoundError(user_id)
        return UserRead.model_validate(user)

    async def update_user(
        self,
        user_id: int,
        user_data: UserPutUpdate | UserPatchUpdate,
        is_partial: bool = False
    ) -> UserRead | None:
        update_type = "partial" if is_partial else "full"
        logger.debug(f"User service: {update_type} update for user {user_id}")

        new_data = (
            user_data.model_dump(exclude_unset=True) if is_partial
            else user_data.model_dump()
        )

        if not new_data:
            logger.warning(
                f"User service: No update data provided for user {user_id}"
            )
            raise NoUserUpdateDataError()

        if not await self.repository.get_by_id(user_id):
            logger.warning(
                f"User service: User {user_id} was not found for update"
            )
            raise UserNotFoundError(user_id)

        try:
            upd_user = await self.repository.update(user_id, new_data)
            logger.info(f"User service: User {user_id} was updated")
        except IntegrityError:
            logger.warning(
                f"User service: User {user_id} with this phone already exists"
            )
            raise UserPhoneAlreadyExistsError(new_data["phone_number"])
        return UserRead.model_validate(upd_user)

    async def delete_user(self, user_id: int) -> None:
        logger.debug(f"User service: Deleting user {user_id}")
        user = await self.repository.get_by_id(user_id)

        if not user:
            logger.warning(
                f"User service: User {user_id} was not found for deletion"
            )
            raise UserNotFoundError(user_id)

        await self.repository.delete(user_id)
        logger.info(f"User service: User {user_id} was deleted")
