from src.exceptions.meal_category import (
    MealCategoryAlreadyExistsError, MealCategoryNotFoundError,
    NoMealCategoryUpdateDataError
)
from src.models.meal_category import MealCategoryModel
from src.repositories.meal_category.interface import IMealCategoryRepository
from src.schemas.meal_category import (
    MealCategoryPatchUpdate, MealCategoryCreate
)


class MealCategoryService:
    def __init__(self, category_repo: IMealCategoryRepository):
        self.category_repo = category_repo

    async def create_category(
        self, category_data: MealCategoryCreate
    ) -> MealCategoryModel:
        category_dict = category_data.model_dump()

        if await self.category_repo.get_by_name(category_dict["name"]):
            raise MealCategoryAlreadyExistsError(category_dict["name"])
        return await self.category_repo.create(category_dict)

    async def get_categories(self) -> list[MealCategoryModel]:
        return await self.category_repo.get_all()

    async def get_category(self, category_id: int) -> MealCategoryModel:
        category = await self.category_repo.get_by_id(category_id)

        if not category:
            raise MealCategoryNotFoundError(category_id)
        return category

    async def update_category(
        self, category_id: int, category_data: MealCategoryPatchUpdate
    ) -> MealCategoryModel:
        new_data = category_data.model_dump(exclude_unset=True)

        if not new_data:
            raise NoMealCategoryUpdateDataError()

        category = await self.category_repo.get_by_id(category_id)

        if not category:
            raise MealCategoryNotFoundError(category_id)
        if category.name == category_data.name:
            raise MealCategoryAlreadyExistsError(category_data.name)

        return await self.category_repo.update(category_id, new_data)

    async def delete_category(self, category_id: int) -> None:
        category = await self.category_repo.get_by_id(category_id)

        if not category:
            raise MealCategoryNotFoundError(category_id)

        return await self.category_repo.delete(category_id)
