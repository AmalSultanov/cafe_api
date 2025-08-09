from typing import Protocol

from src.models.order_item import OrderItemModel


class IOrderItemService(Protocol):
    async def bulk_create_items(self, items: list[OrderItemModel]) -> None: ...

    async def get_items(self, order_id: int) -> list[OrderItemModel]: ...
