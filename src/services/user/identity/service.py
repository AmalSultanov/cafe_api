from src.exceptions.user import UserIdentityNotFoundError
from src.models.user import UserIdentityModel
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.schemas.user import IdentityCheck


class UserIdentityService:
    def __init__(self, user_identity_repo: IUserIdentityRepository):
        self.user_identity_repo = user_identity_repo

    async def create_identity(
         self, user_id: int, identity_data: IdentityCheck
    ):
        await self.user_identity_repo.create(
            user_id, identity_data.model_dump()
        )

    async def get_identity(
        self, identity_data: IdentityCheck
    ) -> UserIdentityModel:
        user = await self.user_identity_repo.get_by_provider(
            identity_data.model_dump()
        )

        if not user:
            raise UserIdentityNotFoundError(identity_data.provider_id)
        return user

    async def is_registered(self, identity_data: IdentityCheck) -> bool:
        return (
            await self.user_identity_repo.get_by_provider(
                identity_data.model_dump()
            ) is not None
        )
