from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.meals.schemas import (
    MealCategoryRead, MealCategoryCreate, MealRead, MealCreate,
    MealCategoryUpdate, MealUpdate, MealPutUpdate
)
from src.meals.service import MealCategoryService, MealService

meals_router = APIRouter(prefix='/meals', tags=['Meals'])


@meals_router.post('/categories', response_model=MealCategoryRead)
async def create_category(
        category_data: MealCategoryCreate,
        db: AsyncSession = Depends(get_session)
):
    service = MealCategoryService(db)
    return await service.create_category(category_data)


@meals_router.get('/categories', response_model=list[MealCategoryRead])
async def get_categories(db: AsyncSession = Depends(get_session)):
    service = MealCategoryService(db)
    return await service.get_categories()


@meals_router.get('/categories/{category_id}', response_model=MealCategoryRead)
async def get_category(
        category_id: int,
        db: AsyncSession = Depends(get_session)
):
    service = MealCategoryService(db)
    return await service.get_category(category_id)


@meals_router.patch(
    '/categories/{category_id}',
    response_model=MealCategoryRead
)
async def update_category(
        category_id: int,
        category_data: MealCategoryUpdate,
        db: AsyncSession = Depends(get_session)
):
    service = MealCategoryService(db)
    return await service.update_category(category_id, category_data)


@meals_router.delete(
    '/categories/{category_id}',
    response_model=MealCategoryRead
)
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_session)
):
    service = MealCategoryService(db)
    return await service.delete_category(category_id)


@meals_router.post('/categories/{category_id}/meals', response_model=MealRead)
async def create_meal(
        meal_data: MealCreate,
        db: AsyncSession = Depends(get_session)
):
    service = MealService(db)
    return await service.create_meal(meal_data)


@meals_router.get(
    '/categories/{category_id}/meals',
    response_model=list[MealRead]
)
async def get_meals(category_id: int, db: AsyncSession = Depends(get_session)):
    service = MealService(db)
    return await service.get_meals_by_category(category_id)


@meals_router.get(
    '/categories/{category_id}/meals/{meal_id}',
    response_model=MealRead
)
async def get_meal(
        category_id: int,
        meal_id: int,
        db: AsyncSession = Depends(get_session)
):
    service = MealService(db)
    return await service.get_meal(category_id, meal_id)


@meals_router.put(
    '/categories/{category_id}/meals/{meal_id}',
    response_model=MealRead
)
async def update_meal(
        category_id: int,
        meal_id: int,
        meal_data: MealPutUpdate,
        db: AsyncSession = Depends(get_session)
):
    service = MealService(db)
    return await service.update_meal(category_id, meal_id, meal_data)


@meals_router.patch(
    '/categories/{category_id}/meals/{meal_id}',
    response_model=MealRead
)
async def partial_update_meal(
        category_id: int,
        meal_id: int,
        meal_data: MealUpdate,
        db: AsyncSession = Depends(get_session)
):
    service = MealService(db)
    return await service.partial_update_meal(category_id, meal_id, meal_data)


@meals_router.delete(
    '/categories/{category_id}/meals/{meal_id}',
    response_model=MealRead
)
async def delete_meal(
        category_id: int,
        meal_id: int,
        db: AsyncSession = Depends(get_session)
):
    service = MealService(db)
    return await service.delete_meal(category_id, meal_id)
