from typing import Protocol

from src.schemas.user import IdentityCheck, IdentityRead, IdentityCreate


class IUserIdentityService(Protocol):
    async def create_identity(
         self, user_id: int, identity_data: IdentityCreate
    ) -> IdentityRead:
        ...

    async def get_identity(
        self, identity_data: IdentityCheck
    ) -> IdentityRead:
        ...

    async def identity_exists(self, identity_data: IdentityCheck) -> bool:
        ...
