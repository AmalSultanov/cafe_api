from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: dict[str, str]) -> UserModel:
        user = UserModel(
            name=user_data["name"],
            surname=user_data["surname"],
            phone_number=user_data["phone_number"]
        )
        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_all(self, limit: int, offset: int) -> list[UserModel]:
        result = await self.db.execute(
            select(UserModel).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> UserModel | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone_number: str) -> UserModel | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.phone_number == phone_number)
        )
        return result.scalar_one_or_none()

    async def get_total_count(self) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(UserModel)
        )
        return result.scalar_one()

    async def update(
        self, user_id: int, user_data: dict[str, str]
    ) -> UserModel:
        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user_data)
        )

        try:
            await self.db.commit()
            return await self.get_by_id(user_id)
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete(self, user_id: int) -> None:
        await self.db.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.db.commit()
