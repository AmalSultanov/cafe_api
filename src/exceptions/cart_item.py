from src.exceptions.base import NotFoundError, ConflictError, ValidationError


class CartItemAlreadyExistsError(ConflictError):
    def __init__(self, meal_id: int):
        super().__init__(f"Meal with ID={meal_id} is already in the cart")


class CartItemNotFoundError(NotFoundError):
    def __init__(self, item_id: int):
        super().__init__(f"Cart item with ID={item_id} was not found")


class CartItemsNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__(
            f"Cart items of user with ID={user_id} were not found"
        )


class NoCartItemUpdateDataError(ValidationError):
    def __init__(self):
        super().__init__("No data provided for update")


class CartItemQuantityError(ValidationError):
    def __init__(self):
        super().__init__("Quantity must be greater than 0")
