from sqlalchemy import update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.meal_category import MealCategoryModel


class SQLAlchemyMealCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: dict[str, str]) -> MealCategoryModel:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Creating category, "
            f"data: {category_data}"
        )
        category = MealCategoryModel(**category_data)
        self.db.add(category)

        try:
            await self.db.commit()
            await self.db.refresh(category)
            logger.info(
                f"SQLAlchemy Meal Category repo: Category created with "
                f"ID: {category.id}, name: {category.name}"
            )

            return category
        except IntegrityError as e:
            logger.error(
                f"SQLAlchemy Meal Category repo: Failed to create category "
                f"due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def get_all(
        self, limit: int, offset: int
    ) -> list[MealCategoryModel]:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Getting categories, "
            f"limit: {limit}, offset: {offset}"
        )
        result = await self.db.execute(
            select(MealCategoryModel).limit(limit).offset(offset)
        )
        categories = result.scalars().all()
        logger.debug(
            f"SQLAlchemy Meal Category repo: {len(categories)} categories"
        )

        return categories

    async def get_by_id(self, category_id: int) -> MealCategoryModel | None:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Getting category by "
            f"ID: {category_id}"
        )
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        category = result.scalar_one_or_none()

        if category:
            logger.debug(
                f"SQLAlchemy Meal Category repo: Found meal category "
                f"{category_id}: {category.name}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Meal Category repo: Category {category_id} "
                f"not found"
            )

        return category

    async def get_by_name(
        self, category_name: str
    ) -> MealCategoryModel | None:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Getting category by "
            f"name: {category_name}"
        )
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.name == category_name)
        )
        category = result.scalar_one_or_none()

        if category:
            logger.debug(
                f"SQLAlchemy Meal Category repo: Found category "
                f"'{category_name}' with ID: {category.id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Meal Category repo: Category "
                f"'{category_name}' not found"
            )

        return category

    async def get_total_count(self) -> int:
        logger.debug(
            "SQLAlchemy Meal Category repo: Getting total meal category count"
        )
        result = await self.db.execute(
            select(func.count()).select_from(MealCategoryModel)
        )
        count = result.scalar_one()
        logger.debug(
            f"SQLAlchemy Meal Category repo: Total meal categories: {count}"
        )

        return count

    async def update(
        self, category_id: int, category_data: dict[str, str]
    ) -> MealCategoryModel:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Updating meal category "
            f"{category_id}, data: {category_data}"
        )
        await self.db.execute(
            update(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
            .values(**category_data)
        )

        try:
            await self.db.commit()
            updated_category = await self.get_by_id(category_id)
            logger.info(
                f"SQLAlchemy Meal Category repo: Category {category_id} "
                f"was updated"
            )

            return updated_category
        except IntegrityError as e:
            logger.error(
                f"SQLAlchemy Meal Category repo: Failed to update category "
                f"{category_id} due to integrity error: {e}"
            )
            await self.db.rollback()
            raise

    async def delete(self, category_id: int) -> None:
        logger.debug(
            f"SQLAlchemy Meal Category repo: Deleting category {category_id}"
        )
        await self.db.execute(
            delete(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        await self.db.commit()
        logger.info(
            f"SQLAlchemy Meal Category repo: Category {category_id} was deleted"
        )
