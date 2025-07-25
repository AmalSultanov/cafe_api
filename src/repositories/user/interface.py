from typing import Protocol

from src.models.user import UserModel


class IUserRepository(Protocol):
    async def create(self, user_data: dict[str, int, str]) -> UserModel:
        ...

    async def get_all(self, limit: int, offset: int) -> list[UserModel]:
        ...

    async def get_by_id(self, user_id: int) -> UserModel | None:
        ...

    async def get_by_phone(self, phone_number: str) -> UserModel | None:
        ...

    async def get_total_count(self) -> int:
        ...

    async def update(
        self, user_id: int, user_data: dict[str, int, str]
    ) -> UserModel:
        ...

    async def delete(self, user_id: int) -> None:
        ...
