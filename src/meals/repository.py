from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.meals.models import MealModel, MealCategoryModel


class MealCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            category_data: dict[str, Any]
    ) -> MealCategoryModel:
        category = MealCategoryModel(**category_data)
        self.db.add(category)

        await self.db.commit()
        await self.db.refresh(category)

        return category

    async def get_all(self) -> list[MealCategoryModel]:
        result = await self.db.execute(select(MealCategoryModel))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> MealCategoryModel | None:
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )

        return result.scalar_one_or_none()

    async def update(
            self,
            category_id: int,
            category_data: dict[str, Any]
    ) -> MealCategoryModel | None:
        await self.db.execute(
            update(MealCategoryModel)
            .where(MealCategoryModel.id == category_id).values(**category_data)
        )
        await self.db.commit()

        return await self.get_by_id(category_id)

    async def delete(self, category: MealCategoryModel) -> MealCategoryModel:
        await self.db.delete(category)
        await self.db.commit()

        return category


class MealRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, meal_data: dict[str, Any]) -> MealModel:
        meal = MealModel(**meal_data)
        self.db.add(meal)

        await self.db.commit()
        await self.db.refresh(meal)

        return meal

    async def get_all_by_category(self, category_id: int) -> list[MealModel]:
        result = await self.db.execute(
            select(MealModel).where(MealModel.category_id == category_id)
        )
        return result.scalars().all()

    async def get_by_id(self, meal_id: int) -> MealModel | None:
        result = await self.db.execute(
            select(MealModel).where(MealModel.id == meal_id)
        )
        return result.scalar_one_or_none()

    async def update(
            self,
            meal_id: int,
            meal_data: dict[str, Any]
    ) -> MealModel | None:
        await self.db.execute(
            update(MealModel)
            .where(MealModel.id == meal_id).values(**meal_data)
        )
        await self.db.commit()

        return await self.get_by_id(meal_id)

    async def delete(self, meal: MealModel) -> MealModel:
        await self.db.delete(meal)
        await self.db.commit()

        return meal
