from typing import Protocol

from src.schemas.common import PaginationParams
from src.schemas.meal_category import (
    MealCategoryPatchUpdate, MealCategoryCreate, MealCategoryRead,
    PaginatedMealCategoryResponse
)


class IMealCategoryService(Protocol):
    async def create_category(
        self, category_data: MealCategoryCreate
    ) -> MealCategoryRead:
        ...

    async def get_categories(
        self, pagination_params: PaginationParams
    ) -> PaginatedMealCategoryResponse:
        ...

    async def get_category(self, category_id: int) -> MealCategoryRead:
        ...

    async def update_category(
        self, category_id: int, category_data: MealCategoryPatchUpdate
    ) -> MealCategoryRead:
        ...

    async def delete_category(self, category_id: int) -> None:
        ...
