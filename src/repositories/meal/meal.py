from decimal import Decimal

from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions.meal import MealAlreadyExistsError
from src.models.meal import MealModel
from src.repositories.meal.interface import IMealRepository


class MealRepository(IMealRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        try:
            meal = MealModel(**meal_data)
            self.db.add(meal)

            await self.db.commit()
            await self.db.refresh(meal)

            return meal
        except IntegrityError:
            await self.db.rollback()
            raise MealAlreadyExistsError(meal_data["name"])

    async def get_all_by_category_id(
        self, category_id: int
    ) -> list[MealModel]:
        result = await self.db.execute(
            select(MealModel).where(MealModel.category_id == category_id)
        )
        return result.scalars().all()

    async def get_by_id(self, meal_id: int) -> MealModel | None:
        result = await self.db.execute(
            select(MealModel).where(MealModel.id == meal_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, meal_name: int) -> MealModel | None:
        result = await self.db.execute(
            select(MealModel).where(MealModel.name == meal_name)
        )
        return result.scalar_one_or_none()

    async def update(
        self, meal_id: int, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        await self.db.execute(
            update(MealModel)
            .where(MealModel.id == meal_id).values(**meal_data)
        )
        await self.db.commit()

        return await self.get_by_id(meal_id)

    async def delete(self, meal_id: int) -> None:
        await self.db.execute(delete(MealModel).where(MealModel.id == meal_id))
        await self.db.commit()
