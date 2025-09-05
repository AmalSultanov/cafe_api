from decimal import Decimal

from sqlalchemy import update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.meal import MealModel


class SQLAlchemyMealRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        logger.debug(f"SQLAlchemy Meal repo: Creating meal, data: {meal_data}")
        meal = MealModel(**meal_data)
        self.db.add(meal)

        try:
            await self.db.commit()
            await self.db.refresh(meal)
            logger.info(
                f"SQLAlchemy Meal repo: Meal was created with "
                f"ID: {meal.id}, name: {meal.name}"
            )
            return meal
        except IntegrityError as e:
            logger.error(
                f"SQLAlchemy Meal repo: Failed to create meal "
                f"due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def get_all_by_category_id(
        self, category_id: int, limit: int, offset: int
    ) -> list[MealModel]:
        logger.debug(
            f"SQLAlchemy Meal repo: Getting meals for category {category_id}, "
            f"limit: {limit}, offset: {offset}"
        )
        result = await self.db.execute(
            select(MealModel)
            .where(MealModel.category_id == category_id)
            .limit(limit)
            .offset(offset)
        )
        meals = result.scalars().all()
        logger.debug(
            f"SQLAlchemy Meal repo: {len(meals)} meals from"
            f" category {category_id}"
        )

        return meals

    async def get_by_id(self, meal_id: int) -> MealModel | None:
        logger.debug(f"SQLAlchemy Meal repo: Getting meal by ID {meal_id}")
        result = await self.db.execute(
            select(MealModel).where(MealModel.id == meal_id)
        )
        meal = result.scalar_one_or_none()

        if meal:
            logger.debug(f"SQLAlchemy Meal repo: Meal {meal_id}: {meal.name}")
        else:
            logger.debug(f"SQLAlchemy Meal repo: Meal {meal_id} not found")

        return meal

    async def get_by_name(self, meal_name: str) -> MealModel | None:
        logger.debug(
            f"SQLAlchemy Meal repo: Getting meal by name: {meal_name}"
        )
        result = await self.db.execute(
            select(MealModel).where(MealModel.name == meal_name)
        )
        meal = result.scalar_one_or_none()

        if meal:
            logger.debug(
                f"SQLAlchemy Meal repo: Found meal '{meal_name}' "
                f"with ID: {meal.id}"
            )
        else:
            logger.debug(f"SQLAlchemy Meal repo: Meal '{meal_name}' not found")

        return meal

    async def get_total_count(self, category_id: int) -> int:
        logger.debug(
            f"SQLAlchemy Meal repo: Getting total meal count for "
            f"category {category_id}"
        )
        result = await self.db.execute(
            select(func.count())
            .where(MealModel.category_id == category_id)
            .select_from(MealModel)
        )
        count = result.scalar_one()
        logger.debug(
            f"SQLAlchemy Meal repo: Total meals in "
            f"category {category_id}: {count}"
        )

        return count

    async def update(
        self, meal_id: int, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        logger.debug(
            f"SQLAlchemy Meal repo: Updating meal {meal_id}, data: {meal_data}"
        )
        await self.db.execute(
            update(MealModel)
            .where(MealModel.id == meal_id)
            .values(**meal_data)
        )

        try:
            await self.db.commit()
            updated_meal = await self.get_by_id(meal_id)
            logger.info(f"SQLAlchemy Meal repo: Meal {meal_id} was updated")
            return updated_meal
        except IntegrityError as e:
            logger.error(
                f"SQLAlchemy Meal repo: Failed to update meal {meal_id} "
                f"due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def delete(self, meal_id: int) -> None:
        logger.debug(f"SQLAlchemy Meal repo: Deleting meal {meal_id}")
        await self.db.execute(delete(MealModel).where(MealModel.id == meal_id))
        await self.db.commit()
        logger.info(f"SQLAlchemy Meal repo: Meal {meal_id} was deleted")
