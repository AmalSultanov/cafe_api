from sqlalchemy.exc import IntegrityError

from src.models.user import UserIdentityModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserIdentityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, user_id: int, identity_data: dict[str, str]
    ) -> UserIdentityModel:
        identity = UserIdentityModel(
            user_id=user_id,
            provider=identity_data["provider"],
            provider_id=identity_data["provider_id"],
            username=identity_data["username"]
        )
        self.db.add(identity)

        try:
            await self.db.commit()
            await self.db.refresh(identity)
            return identity
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_by_provider(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        result = await self.db.execute(
            select(UserIdentityModel)
            .where(
                UserIdentityModel.provider == identity_data["provider"],
                UserIdentityModel.provider_id == identity_data["provider_id"]
            )
        )
        return result.scalar_one_or_none()

    async def get_by_provider_and_username(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        result = await self.db.execute(
            select(UserIdentityModel)
            .where(
                UserIdentityModel.provider == identity_data["provider"],
                UserIdentityModel.username == identity_data["username"]
            )
        )
        return result.scalar_one_or_none()
