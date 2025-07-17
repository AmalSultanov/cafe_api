from fastapi import HTTPException

from src.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from src.models.user import UserModel
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.repositories.user.interface import IUserRepository
from src.schemas.user import UserRegister, UserUpdate, UserPartialUpdate, \
    IdentityCheck


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        user_identity_repo: IUserIdentityRepository
    ):
        self.user_repo = user_repo
        self.user_identity_repo = user_identity_repo

    async def create_user(self, user_data: UserRegister) -> UserModel:
        identity_data = user_data.model_dump(
            include={"provider", "provider_id", "username"}
        )

        if await self.user_identity_repo.get_by_provider(identity_data):
            raise UserAlreadyExistsError(user_data.username)

        user = await self.user_repo.create(user_data.model_dump())
        await self.user_identity_repo.create(user.id, identity_data)

        return user

    async def log_in_user(self, phone_number: str):
        user = await self.user_repo.get_by_phone(phone_number)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # ...SMS verification...

    async def get_users(self) -> list[UserModel]:
        return await self.user_repo.get_all()

    async def get_user(self, user_id: int) -> UserModel | None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)
        return user

    async def update_user(
        self, user_id: int, user_data: UserUpdate
    ) -> UserModel | None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return await self.user_repo.update(user_id, user_data.model_dump())

    async def partial_update_user(
        self, user_id: int, user_data: UserPartialUpdate
    ) -> UserModel | None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return await self.user_repo.update(
            user_id, user_data.model_dump(exclude_unset=True)
        )

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return await self.user_repo.delete(user_id)
