from typing import Protocol

from src.schemas.user import (
    UserRegister, UserPutUpdate, UserPatchUpdate, UserRead
)


class IUserService(Protocol):
    async def create_user(self, user_data: UserRegister) -> UserRead:
        ...

    async def log_in_user(self, phone_number: str) -> None:
        ...

    async def get_users(self) -> list[UserRead]:
        ...

    async def get_user(self, user_id: int) -> UserRead | None:
        ...

    async def update_user(
        self,
        user_id: int,
        user_data: UserPutUpdate | UserPatchUpdate,
        is_partial: bool = False
    ) -> UserRead | None:
        ...

    async def delete_user(self, user_id: int) -> None:
        ...
