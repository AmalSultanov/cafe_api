from decimal import Decimal
from typing import Protocol

from src.models.meal import MealModel


class IMealRepository(Protocol):
    async def create(
        self, category_data: dict[str, int | str | Decimal]
    ) -> MealModel: ...

    async def get_all_by_category_id(
        self, category_id: int, limit: int, offset: int
    ) -> list[MealModel]: ...

    async def get_by_id(self, meal_id: int) -> MealModel | None: ...

    async def get_by_name(self, meal_name: str) -> MealModel | None: ...

    async def get_total_count(self, category_id: int) -> int: ...

    async def update(
        self, meal_id: int, meal_data: dict[str, int | str | Decimal]
    ) -> MealModel: ...

    async def delete(self, meal_id: int) -> None: ...
