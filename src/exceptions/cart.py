from src.exceptions.base import NotFoundError, ConflictError


class CartAlreadyExistsError(ConflictError):
    def __init__(self, user_id: int):
        super().__init__(f"Cart for user with ID={user_id} already exists")


class CartNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__(f"Cart for user with ID={user_id} was not found")
