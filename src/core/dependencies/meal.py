from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.dependencies.meal_category import get_meal_category_service
from src.repositories.interfaces.meal import IMealRepository
from src.repositories.sqlalchemy.meal import SQLAlchemyMealRepository
from src.services.meal.interface import IMealService
from src.services.meal.service import MealService
from src.services.meal_category.interface import IMealCategoryService


def get_meal_repo(
    db: AsyncSession = Depends(get_session)
) -> IMealRepository:
    return SQLAlchemyMealRepository(db)


def get_meal_service(
    repository: IMealRepository = Depends(get_meal_repo),
    category_service: IMealCategoryService = Depends(
        get_meal_category_service
    )
) -> IMealService:
    return MealService(repository, category_service)
