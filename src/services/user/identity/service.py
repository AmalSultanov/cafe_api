from sqlalchemy.exc import IntegrityError

from src.exceptions.user import (
    UserIdentityNotFoundError, UserIdentityAlreadyExistsError
)
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.schemas.user import IdentityCheck, IdentityRead, IdentityCreate


class UserIdentityService:
    def __init__(self, repository: IUserIdentityRepository) -> None:
        self.repository = repository

    async def create_identity(
         self, user_id: int, identity_data: IdentityCreate
    ) -> IdentityRead:
        identity_dict = identity_data.model_dump()

        try:
            identity = await self.repository.create(user_id, identity_dict)
        except IntegrityError:
            raise UserIdentityAlreadyExistsError(
                identity_dict["provider_id"], identity_dict["provider"]
            )

        return IdentityRead.model_validate(identity)

    async def get_identity(
        self, identity_data: IdentityCheck
    ) -> IdentityRead:
        identity_dict = identity_data.model_dump()
        identity = await self.repository.get_by_provider(identity_dict)

        if not identity:
            raise UserIdentityNotFoundError(identity_dict["provider_id"])
        return IdentityRead.model_validate(identity)

    async def identity_exists(self, identity_data: IdentityCheck) -> bool:
        return (
            await self.repository.get_by_provider(
                identity_data.model_dump()
            ) is not None
        )
