from src.schemas.common import PaginationParams
from src.schemas.meal import (
    MealCreate, MealUpdate, MealPutUpdate, MealRead, PaginatedMealResponse
)


class IMealService:
    async def create_meal(
        self, category_id: int, meal_data: MealCreate
    ) -> MealRead:
        ...

    async def get_meals_by_category_id(
        self, category_id: int, pagination_params: PaginationParams
    ) -> PaginatedMealResponse:
        ...

    async def get_meal(
        self, meal_id: int, category_id: int = None
    ) -> MealRead:
        ...

    async def update_meal(
        self,
        category_id: int,
        meal_id: int,
        meal_data: MealPutUpdate | MealUpdate,
        is_partial: bool = False,
    ) -> MealRead:
        ...

    async def delete_meal(self, category_id: int, meal_id: int) -> None:
        ...
