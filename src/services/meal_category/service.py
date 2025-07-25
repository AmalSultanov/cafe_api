from sqlalchemy.exc import IntegrityError

from src.exceptions.meal_category import (
    MealCategoryAlreadyExistsError, MealCategoryNotFoundError,
    NoMealCategoryUpdateDataError
)
from src.repositories.meal_category.interface import IMealCategoryRepository
from src.schemas.common import PaginationParams
from src.schemas.meal_category import (
    MealCategoryPatchUpdate, MealCategoryCreate, MealCategoryRead,
    PaginatedMealCategoryResponse
)


class MealCategoryService:
    def __init__(self, repository: IMealCategoryRepository) -> None:
        self.repository = repository

    async def create_category(
        self, category_data: MealCategoryCreate
    ) -> MealCategoryRead:
        category_dict = category_data.model_dump()

        try:
            category = await self.repository.create(category_dict)
        except IntegrityError:
            raise MealCategoryAlreadyExistsError(category_dict["name"])
        return MealCategoryRead.model_validate(category)

    async def get_categories(
        self, pagination_params: PaginationParams
    ) -> PaginatedMealCategoryResponse:
        offset = (pagination_params.page - 1) * pagination_params.per_page
        categories = await self.repository.get_all(
            pagination_params.per_page, offset
        )
        total = await self.repository.get_total_count()
        total_pages = (
            (total + pagination_params.per_page - 1) // pagination_params.per_page
        )

        return PaginatedMealCategoryResponse(
            total=total,
            page=pagination_params.page,
            total_pages=total_pages,
            items=[MealCategoryRead.model_validate(c) for c in categories]
        )

    async def get_category(self, category_id: int) -> MealCategoryRead:
        category = await self.repository.get_by_id(category_id)

        if not category:
            raise MealCategoryNotFoundError(category_id)
        return MealCategoryRead.model_validate(category)

    async def update_category(
        self, category_id: int, category_data: MealCategoryPatchUpdate
    ) -> MealCategoryRead:
        new_data = category_data.model_dump(exclude_unset=True)

        if not new_data:
            raise NoMealCategoryUpdateDataError()

        category = await self.repository.get_by_id(category_id)
        if not category:
            raise MealCategoryNotFoundError(category_id)
        if category_data.name and category.name == category_data.name:
            raise MealCategoryAlreadyExistsError(category_data.name)

        try:
            upd_category = await self.repository.update(category_id, new_data)
        except IntegrityError:
            raise MealCategoryAlreadyExistsError(new_data["name"])
        return MealCategoryRead.model_validate(upd_category)

    async def delete_category(self, category_id: int) -> None:
        category = await self.repository.get_by_id(category_id)

        if not category:
            raise MealCategoryNotFoundError(category_id)
        await self.repository.delete(category_id)
