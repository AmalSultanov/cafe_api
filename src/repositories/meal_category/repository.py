from sqlalchemy import update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.meal_category import MealCategoryModel


class MealCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: dict[str, str]) -> MealCategoryModel:
        category = MealCategoryModel(**category_data)
        self.db.add(category)

        try:
            await self.db.commit()
            await self.db.refresh(category)
            return category
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_all(
        self, limit: int, offset: int
    ) -> list[MealCategoryModel]:
        result = await self.db.execute(
            select(MealCategoryModel).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> MealCategoryModel | None:
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(
        self, category_name: str
    ) -> MealCategoryModel | None:
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.name == category_name)
        )
        return result.scalar_one_or_none()

    async def get_total_count(self) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(MealCategoryModel)
        )
        return result.scalar_one()

    async def update(
        self, category_id: int, category_data: dict[str, str]
    ) -> MealCategoryModel:
        await self.db.execute(
            update(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
            .values(**category_data)
        )

        try:
            await self.db.commit()
            return await self.get_by_id(category_id)
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete(self, category_id: int) -> None:
        await self.db.execute(
            delete(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        await self.db.commit()
