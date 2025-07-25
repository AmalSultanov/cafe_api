from typing import Protocol

from src.schemas.common import PaginationParams
from src.schemas.meal_category import (
    MealCategoryPatchUpdate, MealCategoryCreate, MealCategoryRead
)


class IMealCategoryService(Protocol):
    async def create_category(
        self, category_data: MealCategoryCreate
    ) -> MealCategoryRead:
        ...

    async def get_categories(
        self, paginated_data: PaginationParams
    ) -> list[MealCategoryRead]:
        ...

    async def get_category(self, category_id: int) -> MealCategoryRead:
        ...

    async def update_category(
        self, category_id: int, category_data: MealCategoryPatchUpdate
    ) -> MealCategoryRead:
        ...

    async def delete_category(self, category_id: int) -> None:
        ...
