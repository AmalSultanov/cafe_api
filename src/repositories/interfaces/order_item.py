from typing import Protocol

from src.models.order_item import OrderItemModel


class IOrderItemRepository(Protocol):
    async def create_many(self, items: list[OrderItemModel]) -> None: ...

    async def get_all(self, order_id: int) -> list[OrderItemModel]: ...
