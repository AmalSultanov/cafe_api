from src.exceptions.base import ConflictError, NotFoundError, ValidationError


class MealCategoryAlreadyExistsError(ConflictError):
    def __init__(self, name: str):
        super().__init__(f"Meal category with name '{name}' already exists")


class MealCategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        super().__init__(f"Meal category with ID={category_id} was not found")


class NoMealCategoryUpdateDataError(ValidationError):
    def __init__(self):
        super().__init__("No data provided for update")
