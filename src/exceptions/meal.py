from src.exceptions.base import NotFoundError, ConflictError


class MealAlreadyExistsError(ConflictError):
    def __init__(self, name: str):
        super().__init__(f"Meal with name '{name}' already exists")


class MealNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        super().__init__(f"Meal with ID={category_id} was not found")
