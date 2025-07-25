from decimal import Decimal

from sqlalchemy import update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.meal import MealModel


class MealRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        meal = MealModel(**meal_data)
        self.db.add(meal)

        try:
            await self.db.commit()
            await self.db.refresh(meal)
            return meal
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_all_by_category_id(
        self, category_id: int, limit: int, offset: int
    ) -> list[MealModel]:
        result = await self.db.execute(
            select(MealModel)
            .where(MealModel.category_id == category_id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_id(self, meal_id: int) -> MealModel | None:
        result = await self.db.execute(
            select(MealModel).where(MealModel.id == meal_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, meal_name: str) -> MealModel | None:
        result = await self.db.execute(
            select(MealModel).where(MealModel.name == meal_name)
        )
        return result.scalar_one_or_none()

    async def get_total_count(self, category_id: int) -> int:
        result = await self.db.execute(
            select(func.count())
            .where(MealModel.category_id == category_id)
            .select_from(MealModel)
        )
        return result.scalar_one()

    async def update(
        self, meal_id: int, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        await self.db.execute(
            update(MealModel)
            .where(MealModel.id == meal_id)
            .values(**meal_data)
        )

        try:
            await self.db.commit()
            return await self.get_by_id(meal_id)
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete(self, meal_id: int) -> None:
        await self.db.execute(delete(MealModel).where(MealModel.id == meal_id))
        await self.db.commit()
