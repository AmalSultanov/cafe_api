from src.exceptions.base import ConflictError, NotFoundError


class UserAlreadyExistsError(ConflictError):
    def __init__(self, name: str):
        super().__init__(f"User with name '{name}' already exists")


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID={user_id} was not found")
