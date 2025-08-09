from src.exceptions.base import ValidationError


class OrderItemQuantityError(ValidationError):
    def __init__(self):
        super().__init__("Quantity must be greater than 0")
