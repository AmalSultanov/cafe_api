from abc import ABC, abstractmethod
from src.models.meal_category import MealCategoryModel


class IMealCategoryRepository(ABC):
    @abstractmethod
    async def create(
        self, category_data: dict[str, int | str]
    ) -> MealCategoryModel:
        pass

    @abstractmethod
    async def get_all(self) -> list[MealCategoryModel]:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> MealCategoryModel:
        pass

    @abstractmethod
    async def get_by_name(self, category_name: str) -> MealCategoryModel:
        pass

    @abstractmethod
    async def update(
        self, category_id: int, category_data: dict[str, int | str]
    ) -> MealCategoryModel:
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> None:
        pass
