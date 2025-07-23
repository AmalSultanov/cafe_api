from typing import Protocol

from src.schemas.user import UserRegister, UserRead


class IUserRegistrationService(Protocol):
    async def register_user(self, user_data: UserRegister) -> UserRead: ...
