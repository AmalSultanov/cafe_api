from sqlalchemy.exc import IntegrityError

from src.core.utils import url_to_str
from src.exceptions.meal import (
    MealNotFoundError, MealAlreadyExistsError, NoMealUpdateDataError
)
from src.exceptions.meal_category import MealCategoryNotFoundError
from src.repositories.meal.interface import IMealRepository
from src.schemas.meal import MealCreate, MealUpdate, MealPutUpdate, MealRead
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
        if not await self.category_service.get_category(category_id):
            raise MealCategoryNotFoundError(category_id)

        if await self.repository.get_by_name(meal_data.name):
            raise MealAlreadyExistsError(meal_data.name)

        if meal_data.image_url:
            meal_data.image_url = url_to_str(meal_data.image_url)

        meal_dict = meal_data.model_dump()
        meal_dict["category_id"] = category_id

        try:
            meal = await self.repository.create(meal_dict)
        except IntegrityError:
            raise MealAlreadyExistsError(meal_dict["name"])
        return MealRead.model_validate(meal)

    async def get_meals_by_category_id(
        self, category_id: int
    ) -> list[MealRead]:
        if not await self.category_service.get_category(category_id):
            raise MealCategoryNotFoundError(category_id)

        meals = await self.repository.get_all_by_category_id(category_id)
        return [MealRead.model_validate(meal) for meal in meals]

    async def get_meal(
        self, meal_id: int, category_id: int = None
    ) -> MealRead:
        meal = await self.repository.get_by_id(meal_id)

        if not meal:
            raise MealNotFoundError(meal_id)

        if category_id is not None and meal.category_id != category_id:
            if not await self.category_service.get_category(category_id):
                raise MealCategoryNotFoundError(category_id)
            raise MealNotFoundError(meal_id)

        return MealRead.model_validate(meal)

    async def update_meal(
        self,
        category_id: int,
        meal_id: int,
        meal_data: MealPutUpdate | MealUpdate,
        is_partial: bool = False
    ) -> MealRead:
        new_data = (
            meal_data.model_dump(exclude_unset=True) if is_partial
            else meal_data.model_dump()
        )

        if not new_data:
            raise NoMealUpdateDataError()
        if not await self.category_service.get_category(category_id):
            raise MealCategoryNotFoundError(category_id)

        meal = await self.repository.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise MealNotFoundError(meal_id)

        if hasattr(meal_data, "image_url") and meal_data.image_url is not None:
            meal_data.image_url = url_to_str(meal_data.image_url)

        if "name" in new_data:
            existing = await self.repository.get_by_name(new_data["name"])

            if existing and existing.id != meal_id:
                raise MealAlreadyExistsError(new_data["name"])

        try:
            upd_meal = await self.repository.update(meal_id, new_data)
        except IntegrityError:
            raise MealAlreadyExistsError(new_data["name"])
        return MealRead.model_validate(upd_meal)

    async def delete_meal(self, category_id: int, meal_id: int) -> None:
        if not await self.category_service.get_category(category_id):
            raise MealCategoryNotFoundError(category_id)

        meal = await self.repository.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise MealNotFoundError(meal_id)

        return await self.repository.delete(meal_id)
