from abc import ABC, abstractmethod
from decimal import Decimal

from src.models.meal import MealModel


class IMealRepository(ABC):
    @abstractmethod
    async def create(
        self, category_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        pass

    @abstractmethod
    async def get_all_by_category_id(
        self, category_id: int
    ) -> list[MealModel]:
        pass

    @abstractmethod
    async def get_by_id(self, meal_id: int) -> MealModel:
        pass

    @abstractmethod
    async def get_by_name(self, meal_name: str) -> MealModel:
        pass

    @abstractmethod
    async def update(
        self, meal_id: int, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel:
        pass

    @abstractmethod
    async def delete(self, meal_id: int) -> None:
        pass
