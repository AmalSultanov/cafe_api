from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
from src.exceptions.meal_category import (
    MealCategoryAlreadyExistsError, MealCategoryNotFoundError,
    NoMealCategoryUpdateDataError
)
from src.repositories.interfaces.meal_category import IMealCategoryRepository
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
        logger.info(
            f"Meal item service: Creating meal category: {category_data.name}"
        )
        category_dict = category_data.model_dump()

        try:
            category = await self.repository.create(category_dict)
            logger.info(
                f"Meal item service: Meal category was created with "
                f"ID: {category.id}"
            )
        except IntegrityError:
            logger.warning(
                f"Meal item service: Meal category '{category_dict['name']}' "
                f"already exists"
            )
            raise MealCategoryAlreadyExistsError(category_dict["name"])
        return MealCategoryRead.model_validate(category)

    async def get_categories(
        self, pagination_params: PaginationParams
    ) -> PaginatedMealCategoryResponse:
        logger.debug(
            f"Meal item service: Fetching meal categories - page: "
            f"{pagination_params.page}, per_page: {pagination_params.per_page}"
        )
        offset = (pagination_params.page - 1) * pagination_params.per_page
        categories = await self.repository.get_all(
            pagination_params.per_page, offset
        )
        total = await self.repository.get_total_count()
        total_pages = (
            (total + pagination_params.per_page - 1) // pagination_params.per_page
        )
        logger.info(
            f"Meal item service: Retrieved {len(categories)} meal categories "
            f"(page {pagination_params.page}/{total_pages})"
        )

        return PaginatedMealCategoryResponse(
            total=total,
            page=pagination_params.page,
            total_pages=total_pages,
            items=[MealCategoryRead.model_validate(c) for c in categories]
        )

    async def get_category(self, category_id: int) -> MealCategoryRead:
        logger.debug(f"Meal item service: Getting meal category {category_id}")
        category = await self.repository.get_by_id(category_id)

        if not category:
            logger.warning(
                f"Meal item service: Meal category {category_id} was not found"
            )
            raise MealCategoryNotFoundError(category_id)

        logger.debug(f"Meal item service: Found meal category {category_id}")
        return MealCategoryRead.model_validate(category)

    async def update_category(
        self, category_id: int, category_data: MealCategoryPatchUpdate
    ) -> MealCategoryRead:
        logger.debug(
            f"Meal item service: Updating meal category {category_id}"
        )
        new_data = category_data.model_dump(exclude_unset=True)

        if not new_data:
            logger.warning(
                f"Meal item service: Update meal category {category_id}"
            )
            raise NoMealCategoryUpdateDataError()

        logger.debug(
            f"Meal item service:: Update category {category_id}: {new_data}"
        )
        category = await self.repository.get_by_id(category_id)

        if not category:
            logger.warning(
                f"Meal item service: Meal category {category_id} was not "
                f"found for update"
            )
            raise MealCategoryNotFoundError(category_id)
        if category_data.name and category.name == category_data.name:
            logger.warning(
                f"Meal item service: Meal category name '{category_data.name}' "
                f"already exists"
            )
            raise MealCategoryAlreadyExistsError(category_data.name)

        try:
            upd_category = await self.repository.update(category_id, new_data)
            logger.info(
                f"Meal item service: Meal category {category_id} was updated"
            )

            return MealCategoryRead.model_validate(upd_category)
        except IntegrityError as e:
            logger.error(
                f"Meal item service: Failed to update meal category "
                f"{category_id} due to integrity error: {e}"
            )
            raise MealCategoryAlreadyExistsError(new_data["name"])

    async def delete_category(self, category_id: int) -> None:
        logger.debug(f"Meal item service: Deleting meal category {category_id}")
        category = await self.repository.get_by_id(category_id)

        if not category:
            logger.warning(
                f"Meal item service: Meal category {category_id} was not "
                f"found for deletion"
            )
            raise MealCategoryNotFoundError(category_id)

        await self.repository.delete(category_id)
        logger.info(
            f"Meal item service:: Meal category {category_id} was deleted"
        )
