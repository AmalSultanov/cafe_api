from abc import ABC, abstractmethod

from src.models.user import UserIdentityModel


class IUserIdentityRepository(ABC):
    @abstractmethod
    async def create(
        self, user_id: int, identity_data: dict[str, str]
    ) -> UserIdentityModel:
        pass

    @abstractmethod
    async def get_by_provider(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        pass
