from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions.meal_category import MealCategoryAlreadyExistsError
from src.models.meal_category import MealCategoryModel
from src.repositories.meal_category.interface import IMealCategoryRepository


class MealCategoryRepository(IMealCategoryRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: dict[str, str]) -> MealCategoryModel:
        try:
            category = MealCategoryModel(**category_data)
            self.db.add(category)

            await self.db.commit()
            await self.db.refresh(category)

            return category
        except IntegrityError:
            await self.db.rollback()
            raise MealCategoryAlreadyExistsError(category_data["name"])

    async def get_all(self) -> list[MealCategoryModel]:
        result = await self.db.execute(select(MealCategoryModel))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> MealCategoryModel | None:
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(
        self, category_name: str
    ) -> MealCategoryModel | None:
        result = await self.db.execute(
            select(MealCategoryModel)
            .where(MealCategoryModel.name == category_name)
        )
        return result.scalar_one_or_none()

    async def update(
        self, category_id: int, category_data: dict[str, str]
    ) -> MealCategoryModel:
        try:
            await self.db.execute(
                update(MealCategoryModel)
                .where(MealCategoryModel.id == category_id)
                .values(**category_data)
            )
            await self.db.commit()

            return await self.get_by_id(category_id)
        except IntegrityError:
            await self.db.rollback()
            raise MealCategoryAlreadyExistsError(category_data["name"])

    async def delete(self, category_id: int) -> None:
        await self.db.execute(
            delete(MealCategoryModel)
            .where(MealCategoryModel.id == category_id)
        )
        await self.db.commit()
