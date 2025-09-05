from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
from src.core.utils.type_converters import url_to_str
from src.exceptions.meal import (
    MealNotFoundError, MealAlreadyExistsError, NoMealUpdateDataError
)
from src.exceptions.meal_category import MealCategoryNotFoundError
from src.repositories.interfaces.meal import IMealRepository
from src.schemas.common import PaginationParams
from src.schemas.meal import (
    MealCreate, MealPatchUpdate, MealPutUpdate, MealRead, PaginatedMealResponse
)
from src.services.meal_category.interface import IMealCategoryService


class MealService:
    def __init__(
        self,
        repository: IMealRepository,
        category_service: IMealCategoryService
    ) -> None:
        self.repository = repository
        self.category_service = category_service

    async def create_meal(
        self, category_id: int, meal_data: MealCreate
    ) -> MealRead:
        logger.info(
            f"Meal service: Creating meal '{meal_data.name}' "
            f"in category {category_id}"
        )

        if not await self.category_service.get_category(category_id):
            logger.warning(
                f"Meal service: Category {category_id} was not "
                f"found for meal creation"
            )
            raise MealCategoryNotFoundError(category_id)

        if await self.repository.get_by_name(meal_data.name):
            logger.warning(
                f"Meal service: Meal '{meal_data.name}' already exists"
            )
            raise MealAlreadyExistsError(meal_data.name)

        if meal_data.image_url:
            meal_data.image_url = url_to_str(meal_data.image_url)

        meal_dict = meal_data.model_dump()
        meal_dict["category_id"] = category_id

        try:
            meal = await self.repository.create(meal_dict)
            logger.info(
                f"Meal service: Meal '{meal_data.name}' was created "
                f"with ID: {meal.id}"
            )
            return MealRead.model_validate(meal)
        except IntegrityError as e:
            logger.error(
                f"Meal service: Failed to create meal '{meal_dict['name']}' "
                f"due to integrity error: {e}"
            )
            raise MealAlreadyExistsError(meal_dict["name"])

    async def get_meals_by_category_id(
        self, category_id: int, pagination_params: PaginationParams
    ) -> PaginatedMealResponse:
        logger.debug(
            f"Meal service:: Getting meals for category {category_id}, page: "
            f"{pagination_params.page}, per_page: {pagination_params.per_page}"
        )

        if not await self.category_service.get_category(category_id):
            logger.warning(
                f"Meal service: Category {category_id} was not "
                f"found for meal retrieval"
            )
            raise MealCategoryNotFoundError(category_id)

        offset = (pagination_params.page - 1) * pagination_params.per_page
        meals = await self.repository.get_all_by_category_id(
            category_id, pagination_params.per_page, offset
        )
        total = await self.repository.get_total_count(category_id)
        total_pages = (
            (total + pagination_params.per_page - 1) // pagination_params.per_page
        )

        logger.info(
            f"Meal service:: Retrieved {len(meals)} meals from category "
            f"{category_id} (page {pagination_params.page}/{total_pages})"
        )
        return PaginatedMealResponse(
            total=total,
            page=pagination_params.page,
            total_pages=total_pages,
            items=[MealRead.model_validate(meal) for meal in meals]
        )

    async def get_meal(
        self, meal_id: int, category_id: int = None
    ) -> MealRead:
        logger.debug(
            f"Meal service:: Getting meal {meal_id}" +
            (f" from category {category_id}" if category_id else "")
        )
        meal = await self.repository.get_by_id(meal_id)

        if not meal:
            logger.warning(f"Meal service: Meal {meal_id} was not found")
            raise MealNotFoundError(meal_id)

        if category_id is not None and meal.category_id != category_id:
            logger.warning(
                f"Meal service: Meal {meal_id} was not found in category "
                f"{category_id} (actual category: {meal.category_id})"
            )
            if not await self.category_service.get_category(category_id):
                raise MealCategoryNotFoundError(category_id)
            raise MealNotFoundError(meal_id)

        logger.debug(
            f"Meal service: Found meal {meal_id}, '{meal.name}' "
            f"in category {meal.category_id}"
        )
        return MealRead.model_validate(meal)

    async def update_meal(
        self,
        category_id: int,
        meal_id: int,
        meal_data: MealPutUpdate | MealPatchUpdate,
        is_partial: bool = False
    ) -> MealRead:
        update_type = "partial" if is_partial else "full"
        logger.debug(
            f"Meal service: {update_type} update for meal "
            f"{meal_id} in category {category_id}"
        )
        new_data = (
            meal_data.model_dump(exclude_unset=True) if is_partial
            else meal_data.model_dump()
        )

        if not new_data:
            logger.warning(
                f"Meal service: No update data provided for meal {meal_id}"
            )
            raise NoMealUpdateDataError()

        if not await self.category_service.get_category(category_id):
            logger.warning(
                f"Meal service: Category {category_id} was not found "
                f"for meal update"
            )
            raise MealCategoryNotFoundError(category_id)

        meal = await self.repository.get_by_id(meal_id)
        if not meal or meal.category_id != category_id:
            logger.warning(
                f"Meal service: Meal {meal_id} was not found in "
                f"category {category_id}"
            )
            raise MealNotFoundError(meal_id)

        if "image_url" in new_data and new_data["image_url"] is not None:
            new_data["image_url"] = url_to_str(new_data["image_url"])

        if "name" in new_data:
            existing = await self.repository.get_by_name(new_data["name"])

            if existing and existing.id != meal_id:
                logger.warning(
                    f"Meal service: Meal name '{new_data['name']}'"
                    f" already exists (ID: {existing.id})"
                )
                raise MealAlreadyExistsError(new_data["name"])

        try:
            upd_meal = await self.repository.update(meal_id, new_data)
            logger.info(f"Meal service: Meal {meal_id} was updated")
            return MealRead.model_validate(upd_meal)
        except IntegrityError as e:
            logger.error(
                f"Meal service: Failed to update meal {meal_id} "
                f"due to integrity error: {e}"
            )
            raise MealAlreadyExistsError(new_data.get("name", "unknown"))

    async def delete_meal(self, category_id: int, meal_id: int) -> None:
        logger.debug(
            f"Meal service: Deleting meal {meal_id} from category {category_id}"
        )

        if not await self.category_service.get_category(category_id):
            logger.warning(
                f"Meal service: Category {category_id} was not found"
            )
            raise MealCategoryNotFoundError(category_id)

        meal = await self.repository.get_by_id(meal_id)
        if not meal or meal.category_id != category_id:
            logger.warning(
                f"Meal service: Meal {meal_id} was not found in "
                f"category {category_id}"
            )
            raise MealNotFoundError(meal_id)

        await self.repository.delete(meal_id)
        logger.info(
            f"Meal service: Meal {meal_id} was deleted from "
            f"category {category_id}"
        )
