from typing import Protocol

from src.models.meal_category import MealCategoryModel


class IMealCategoryRepository(Protocol):
    async def create(
        self, category_data: dict[str, int | str]
    ) -> MealCategoryModel:
        ...

    async def get_all(self) -> list[MealCategoryModel]:
        ...

    async def get_by_id(self, category_id: int) -> MealCategoryModel | None:
        ...

    async def get_by_name(
        self, category_name: str
    ) -> MealCategoryModel | None:
        ...

    async def update(
        self, category_id: int, category_data: dict[str, int | str]
    ) -> MealCategoryModel:
        ...

    async def delete(self, category_id: int) -> None:
        ...
