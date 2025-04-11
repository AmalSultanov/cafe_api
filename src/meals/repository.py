from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.meals.models import MealModel, MealCategoryModel
from src.meals.schemas import (
    MealCreate, MealUpdate, MealCategoryCreate, MealCategoryUpdate,
    MealPutUpdate
)


class MealCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            category_data: MealCategoryCreate
    ) -> MealCategoryModel:
        category = MealCategoryModel(name=category_data.name)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_all(self):
        result = await self.db.execute(select(MealCategoryModel))
        return result.scalars().all()

    async def get_by_id(self, category_id: int):
        result = await self.db.execute(
            select(MealCategoryModel).where(
                MealCategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def update(
            self,
            category_id: int,
            category_data: MealCategoryUpdate
    ) -> MealCategoryModel | None:
        category = await self.get_by_id(category_id)

        for key, value in category_data.items():
            if hasattr(category, key) and value is not None:
                setattr(category, key, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int):
        category = await self.get_by_id(category_id)

        if category:
            await self.db.delete(category)
            await self.db.commit()
        return category


class MealRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, meal_data: MealCreate) -> MealModel:
        meal_data.image_url = str(meal_data.image_url)
        meal = MealModel(**meal_data.dict())
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
            select(MealModel).where(MealModel.id == meal_id))
        return result.scalar_one_or_none()

    async def update(
            self,
            meal_id: int,
            meal_data: MealPutUpdate | MealUpdate
    ) -> MealModel | None:
        if 'image_url' in meal_data and meal_data['image_url'] is not None:
            meal_data['image_url'] = str(meal_data['image_url'])

        await self.db.execute(
            update(MealModel).where(MealModel.id == meal_id).values(**meal_data)
        )
        await self.db.commit()

        result = await self.db.execute(
            select(MealModel).where(MealModel.id == meal_id))
        return result.scalar_one_or_none()

    async def delete(self, meal: MealModel):
        await self.db.delete(meal)
        await self.db.commit()
        return meal
