from pydantic import HttpUrl

from src.exceptions.meal import MealNotFoundError, MealAlreadyExistsError
from src.exceptions.meal_category import MealCategoryNotFoundError
from src.models.meal import MealModel
from src.repositories.meal.interface import IMealRepository
from src.repositories.meal_category.interface import IMealCategoryRepository
from src.schemas.meal import MealCreate, MealUpdate, MealPutUpdate


class MealService:
    def __init__(
        self,
        meal_repo: IMealRepository,
        category_repo: IMealCategoryRepository
    ):
        self.meal_repo = meal_repo
        self.category_repo = category_repo

    async def create_meal(
        self, category_id: int, meal_data: MealCreate
    ) -> MealModel:
        if not await self.category_repo.get_by_id(category_id):
            raise MealCategoryNotFoundError(category_id)

        if await self.meal_repo.get_by_name(meal_data.name):
            raise MealAlreadyExistsError(meal_data.name)

        if meal_data.image_url:
            meal_data.image_url = await self.url_to_str(meal_data.image_url)

        meal_dict = meal_data.model_dump()
        meal_dict["category_id"] = category_id

        return await self.meal_repo.create(meal_dict)

    async def get_meals_by_category_id(
        self, category_id: int
    ) -> list[MealModel]:
        if not await self.category_repo.get_by_id(category_id):
            raise MealCategoryNotFoundError(category_id)

        return await self.meal_repo.get_all_by_category_id(category_id)

    async def get_meal(self, category_id: int, meal_id: int) -> MealModel:
        if not await self.category_repo.get_by_id(category_id):
            raise MealCategoryNotFoundError(category_id)

        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise MealNotFoundError(meal_id)
        return meal

    async def update_meal(
        self,
        category_id: int,
        meal_id: int,
        meal_data: MealPutUpdate | MealUpdate,
        is_partial: bool = False,
    ) -> MealModel:
        if not await self.category_repo.get_by_id(category_id):
            raise MealCategoryNotFoundError(category_id)

        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise MealNotFoundError(meal_id)

        if hasattr(meal_data, "image_url") and meal_data.image_url is not None:
            meal_data.image_url = await self.url_to_str(meal_data.image_url)

        data = (
            meal_data.model_dump(exclude_unset=True)
            if is_partial
            else meal_data.model_dump()
        )

        return await self.meal_repo.update(meal_id, data)

    @staticmethod
    async def url_to_str(image_url: HttpUrl) -> str:
        return str(image_url)

    async def delete_meal(self, category_id: int, meal_id: int) -> None:
        if not await self.category_repo.get_by_id(category_id):
            raise MealCategoryNotFoundError(category_id)

        meal = await self.meal_repo.get_by_id(meal_id)

        if not meal or meal.category_id != category_id:
            raise MealNotFoundError(meal_id)

        return await self.meal_repo.delete(meal_id)
