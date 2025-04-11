from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.meals.repository import MealRepository, MealCategoryRepository
from src.meals.schemas import (
    MealCreate, MealCategoryUpdate, MealUpdate, MealPutUpdate,
    MealCategoryCreate
)


class MealCategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repo = MealCategoryRepository(db)

    async def create_category(self, category_data: MealCategoryCreate):
        return await self.category_repo.create(category_data)

    async def get_categories(self):
        return await self.category_repo.get_all()

    async def get_category(self, category_id: int):
        return await self.category_repo.get_by_id(category_id)

    async def update_category(
            self,
            category_id: int,
            category_data: MealCategoryUpdate
    ):
        category = await self.category_repo.get_by_id(category_id)

        if not category:
            raise HTTPException(status_code=404, detail='Category not found')

        result = await self.category_repo.update(
            category_id,
            category_data.dict(exclude_unset=True)
        )
        return result

    async def delete_category(self, category_id: int):
        return await self.category_repo.delete(category_id)


class MealService:
    def __init__(self, db: AsyncSession):
        self.category_repo = MealCategoryRepository(db)
        self.meal_repo = MealRepository(db)

    async def create_meal(self, meal_data: MealCreate):
        category = await self.category_repo.get_by_id(meal_data.category_id)

        if not category:
            raise HTTPException(status_code=404, detail='Category not found')

        return await self.meal_repo.create(meal_data)

    async def get_meals_by_category(self, category_id: int):
        return await self.meal_repo.get_all_by_category(category_id)

    async def get_meal(self, category_id: int, meal_id: int):
        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise HTTPException(status_code=404,
                                detail='Meal not found in this category')
        return meal

    async def update_meal(
            self,
            category_id: int,
            meal_id: int,
            meal_data: MealPutUpdate
    ):
        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise HTTPException(status_code=404,
                                detail='Meal not found in this category')

        return await self.meal_repo.update(meal_id, meal_data.dict())

    async def partial_update_meal(
            self,
            category_id: int,
            meal_id: int,
            meal_data: MealUpdate
    ):
        meal = await self.meal_repo.get_by_id(meal_id)
        if not meal or meal.category_id != category_id:
            raise HTTPException(status_code=404,
                                detail='Meal not found in this category')

        return await self.meal_repo.update(meal_id,
                                           meal_data.dict(exclude_unset=True))

    async def delete_meal(self, category_id: int, meal_id: int):
        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal:
            raise HTTPException(status_code=404, detail='Meal not found')
        if meal.category_id != category_id:
            raise HTTPException(status_code=400,
                                detail='Meal does not belong to this category')

        return await self.meal_repo.delete(meal)
