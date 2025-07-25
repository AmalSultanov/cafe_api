from sqlalchemy.exc import IntegrityError

from src.exceptions.user import (
    UserAlreadyExistsError, UserNotFoundError, UserPhoneAlreadyExistsError,
    NoUserUpdateDataError, UserIdentityAlreadyExistsError
)
from src.repositories.user.interface import IUserRepository
from src.schemas.common import PaginationParams
from src.schemas.user import (
    UserRegister, UserPutUpdate, UserPatchUpdate, UserRead, IdentityCheck,
    IdentityCreate, PaginatedUserResponse
)
from src.services.user.identity.interface import IUserIdentityService


class UserService:
    def __init__(
        self,
        repository: IUserRepository,
        identity_service: IUserIdentityService
    ) -> None:
        self.repository = repository
        self.identity_service = identity_service

    async def create_user(self, user_data: UserRegister) -> UserRead:
        identity_check = IdentityCheck(
            provider=user_data.provider,
            provider_id=user_data.provider_id
        )

        if await self.identity_service.identity_exists(identity_check):
            raise UserAlreadyExistsError(
                user_data.username, user_data.provider
            )

        try:
            user = await self.repository.create(user_data.model_dump(
                exclude={"provider", "provider_id", "username"}
            ))
        except IntegrityError:
            raise UserAlreadyExistsError(
                user_data.username, user_data.provider
            )

        new_identity = IdentityCreate.model_validate(user_data)

        try:
            await self.identity_service.create_identity(user.id, new_identity)
        except UserIdentityAlreadyExistsError:
            raise
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
