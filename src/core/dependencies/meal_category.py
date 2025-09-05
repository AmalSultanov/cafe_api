from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.interfaces.meal_category import IMealCategoryRepository
from src.repositories.sqlalchemy.meal_category import (
    SQLAlchemyMealCategoryRepository
)
from src.services.meal_category.interface import IMealCategoryService
from src.services.meal_category.service import MealCategoryService


def get_meal_category_repo(
    db: AsyncSession = Depends(get_session)
) -> IMealCategoryRepository:
    return SQLAlchemyMealCategoryRepository(db)


def get_meal_category_service(
    category_repo: IMealCategoryRepository = Depends(
        get_meal_category_repo
    )
) -> IMealCategoryService:
    return MealCategoryService(category_repo)
