from datetime import datetime
from decimal import Decimal
from typing import Protocol

from src.models.order import OrderModel


class IOrderRepository(Protocol):
    async def create_with_items(
        self,
        user_id: int,
        order_data: dict[str, str | Decimal | datetime],
        items_data: list[dict[str, int | str]],
    ) -> OrderModel: ...

    async def get_all(self, user_id: int) -> list[OrderModel]: ...

    async def get_by_user_and_order_id(
        self, user_id: int, order_id: int
    ) -> OrderModel | None: ...

    async def delete_one(self, user_id: int, order_id: int) -> None: ...

    async def delete_all(self, user_id: int) -> None: ...
