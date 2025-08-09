from src.exceptions.base import NotFoundError


class OrderNotFound(NotFoundError):
    def __init__(self, user_id: int, order_id: int) -> None:
        super().__init__(
            f"Order with id={order_id} for user with ID={user_id} was not found"
        )


class OrdersNotFound(NotFoundError):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"Orders for user with ID={user_id} were not found")
