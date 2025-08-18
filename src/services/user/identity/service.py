from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
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
        logger.info(
            f"User identity service: Creating identity for user "
            f"{user_id} with provider {identity_data.provider}"
        )
        identity_dict = identity_data.model_dump()

        try:
            identity = await self.repository.create(user_id, identity_dict)
            logger.info(
                f"User identity service: Identity was created for user {user_id}"
            )
        except IntegrityError:
            logger.warning(
                f"User identity service: Identity already exists for username "
                f"{identity_dict['username']} in {identity_dict['provider']}"
            )
            raise UserIdentityAlreadyExistsError(
                identity_dict["username"], identity_dict["provider"]
            )

        return IdentityRead.model_validate(identity)

    async def get_identity(
        self, identity_data: IdentityCheck
    ) -> IdentityRead:
        logger.debug(
            f"User identity service: Getting identity for provider "
            f"{identity_data.provider}, provider_id: {identity_data.provider_id}"
        )
        identity_dict = identity_data.model_dump()
        identity = await self.repository.get_by_provider(identity_dict)

        if not identity:
            logger.warning(
                f"User identity service: Identity was not found for "
                f"provider_id {identity_dict['provider_id']} in "
                f"{identity_dict['provider']}"
            )
            raise UserIdentityNotFoundError(
                identity_dict["provider_id"], identity_dict["provider"]
            )

        logger.debug(
            f"User identity service: Found identity for user {identity.user_id}"
        )
        return IdentityRead.model_validate(identity)

    async def identity_exists(self, identity_data: IdentityCheck) -> bool:
        logger.debug(
            f"User identity service: Checking if identity exists for provider "
            f"{identity_data.provider}, provider_id: {identity_data.provider_id}"
        )
        exists = (
            await self.repository.get_by_provider(
                identity_data.model_dump()
            ) is not None
        )
        logger.debug(f"User identity service: Identity exists - {exists}")

        return exists

    async def username_exists(self, identity_data: IdentityCheck) -> bool:
        logger.debug(
            f"User identity service: Checking if username exists for provider "
            f"{identity_data.provider}, username: {identity_data.username}"
        )
        exists = (
            await self.repository.get_by_provider_and_username(
                identity_data.model_dump()
            ) is not None
        )
        logger.debug(f"User identity service: Username exists - {exists}")

        return exists
