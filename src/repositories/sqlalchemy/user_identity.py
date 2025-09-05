from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
from src.models.user import UserIdentityModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUserIdentityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, user_id: int, identity_data: dict[str, str]
    ) -> UserIdentityModel:
        logger.debug(
            f"SQLAlchemy User Identity repo: Creating identity for user "
            f"{user_id} with provider {identity_data['provider']}"
        )
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
            logger.info(
                f"SQLAlchemy User Identity repo: Identity created  for "
                f"user {user_id} with ID {identity.id}"
            )

            return identity
        except IntegrityError as e:
            logger.error(
                f"SQLAlchemy User Identity repo: Failed to create identity "
                f"for user {user_id} due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def get_by_provider(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        provider = identity_data["provider"]
        provider_id = identity_data["provider_id"]
        logger.debug(
            f"SQLAlchemy User Identity repo: Getting identity by provider "
            f"{provider} and provider_id {provider_id}"
        )
        result = await self.db.execute(
            select(UserIdentityModel)
            .where(
                UserIdentityModel.provider == provider,
                UserIdentityModel.provider_id == provider_id
            )
        )
        identity = result.scalar_one_or_none()

        if identity:
            logger.debug(
                f"SQLAlchemy User Identity repo: Found identity for "
                f"{provider}:{provider_id} - user_id: {identity.user_id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy User Identity repo: No identity found for "
                f"{provider} with ID {provider_id}"
            )

        return identity

    async def get_by_provider_and_username(
        self, identity_data: dict[str, str]
    ) -> UserIdentityModel | None:
        provider = identity_data["provider"]
        username = identity_data["username"]
        logger.debug(
            f"SQLAlchemy User Identity repo: Getting identity by provider "
            f"{provider} and username {username}"
        )
        result = await self.db.execute(
            select(UserIdentityModel)
            .where(
                UserIdentityModel.provider == provider,
                UserIdentityModel.username == username
            )
        )
        identity = result.scalar_one_or_none()

        if identity:
            logger.debug(
                f"SQLAlchemy User Identity repo: Found identity for "
                f"{provider}:{username} - user_id: {identity.user_id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy User Identity repo: No identity found for "
                f"{provider} with ID{username}"
            )

        return identity
