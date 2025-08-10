from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging import logger
from src.models.user import UserModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: dict[str, str]) -> UserModel:
        logger.debug(
            f"User repo: Creating user in database: "
            f"{user_data.get('name')} {user_data.get('surname')}"
        )
        user = UserModel(
            name=user_data["name"],
            surname=user_data["surname"],
            phone_number=user_data["phone_number"]
        )
        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            logger.debug(
                f"User repo: User created in database with ID: {user.id}"
            )

            return user
        except IntegrityError as e:
            logger.error(
                f"User repo: Database integrity error creating user: {e}"
            )
            await self.db.rollback()
            raise

    async def get_all(self, limit: int, offset: int) -> list[UserModel]:
        logger.debug(
            f"User repo: Getting users, limit: {limit}, offset: {offset}"
        )
        result = await self.db.execute(
            select(UserModel).limit(limit).offset(offset)
        )
        users = result.scalars().all()
        logger.debug(f"User repo: Retrieved {len(users)} users")

        return users

    async def get_by_id(self, user_id: int) -> UserModel | None:
        logger.debug(f"User repo: Getting user by ID: {user_id}")
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user:
            logger.debug(
                f"User repo: Found user {user_id}: {user.name} {user.surname}"
            )
        else:
            logger.debug(f"User repo: User {user_id} not found")

        return user

    async def get_by_phone(self, phone_number: str) -> UserModel | None:
        logger.debug(f"User repo: Getting user by phone: {phone_number}")
        result = await self.db.execute(
            select(UserModel).where(UserModel.phone_number == phone_number)
        )
        user = result.scalar_one_or_none()

        if user:
            logger.debug(
                f"User repo: Found user with phone {phone_number}: ID={user.id}"
            )
        else:
            logger.debug(f"User repo: No user found with phone {phone_number}")

        return user

    async def get_total_count(self) -> int:
        logger.debug("User repo: Getting total user count")
        result = await self.db.execute(
            select(func.count()).select_from(UserModel)
        )
        count = result.scalar_one()
        logger.debug(f"User repo: Total users: {count}")

        return count

    async def update(
        self, user_id: int, user_data: dict[str, str]
    ) -> UserModel:
        logger.debug(
            f"User repo: Updating user {user_id} with data: {user_data}"
        )
        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user_data)
        )

        try:
            await self.db.commit()
            updated_user = await self.get_by_id(user_id)
            logger.info(f"User repo: User {user_id} was updated")
            return updated_user
        except IntegrityError as e:
            logger.error(
                f"User repo: Failed to update user {user_id} "
                f"due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def delete(self, user_id: int) -> None:
        logger.debug(f"User repo: Deleting user {user_id}")
        await self.db.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.db.commit()
        logger.info(f"User repo: User {user_id} was deleted")
