from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.meal.interface import IMealRepository
from src.repositories.meal.meal import MealRepository
from src.repositories.meal_category.interface import IMealCategoryRepository
from src.repositories.meal_category.meal_category import MealCategoryRepository
from src.repositories.user.identity_interface import IUserIdentityRepository
from src.repositories.user.interface import IUserRepository
from src.repositories.user.user import UserRepository
from src.repositories.user.user_identity import UserIdentityRepository
from src.services.meal import MealService
from src.services.meal_category import MealCategoryService
from src.services.user import UserService
from src.services.user_identity import UserIdentityService


def get_meal_category_repo(
    db: AsyncSession = Depends(get_session)
) -> IMealCategoryRepository:
    return MealCategoryRepository(db)


def get_meal_category_service(
    category_repo: IMealCategoryRepository = Depends(get_meal_category_repo)
) -> MealCategoryService:
    return MealCategoryService(category_repo)


def get_meal_repo(
    db: AsyncSession = Depends(get_session)
) -> IMealRepository:
    return MealRepository(db)


def get_meal_service(
    meal_repo: IMealRepository = Depends(get_meal_repo),
    category_repo: IMealCategoryRepository = Depends(get_meal_category_repo)
) -> MealService:
    return MealService(meal_repo, category_repo)


def get_user_identity_repo(
    db: AsyncSession = Depends(get_session)
) -> IUserIdentityRepository:
    return UserIdentityRepository(db)


def get_user_identity_service(
    user_identity_repo: IUserIdentityRepository = Depends(
        get_user_identity_repo
    ),
) -> UserIdentityService:
    return UserIdentityService(user_identity_repo)


def get_user_repo(
    db: AsyncSession = Depends(get_session)
) -> IUserRepository:
    return UserRepository(db)


def get_user_service(
    user_repo: IUserRepository = Depends(get_user_repo),
    user_identity_repo: IUserIdentityRepository = Depends(
        get_user_identity_repo
    ),
) -> UserService:
    return UserService(user_repo, user_identity_repo)
