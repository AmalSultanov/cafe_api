from abc import ABC, abstractmethod

from src.models.user import UserModel


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: dict[str, int, str]) -> UserModel:
        pass

    @abstractmethod
    async def get_all(self) -> list[UserModel]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserModel:
        pass

    @abstractmethod
    async def get_by_phone(self, phone_number: str) -> UserModel:
        pass

    @abstractmethod
    async def update(
        self, user_id: int, user_data: dict[str, int, str]
    ) -> UserModel:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass
