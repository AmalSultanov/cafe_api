from typing import Protocol

from src.models.user import UserIdentityModel


class IUserIdentityRepository(Protocol):
    async def create(
        self, user_id: int, identity_data: dict[str, str]
    ) -> UserIdentityModel:
        ...

    async def get_by_provider(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        ...

    async def get_by_provider_and_username(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        ...
