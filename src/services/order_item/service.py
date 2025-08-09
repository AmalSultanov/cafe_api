from src.models.order_item import OrderItemModel
from src.repositories.order_item.interface import IOrderItemRepository


class OrderItemService:
    def __init__(self, repository: IOrderItemRepository):
        self.repository = repository

    async def bulk_create_items(self, items: list[OrderItemModel]) -> None:
        await self.repository.create_many(items)
        return items

    async def get_items(self, order_id: int) -> list[OrderItemModel]:
        return await self.repository.get_all(order_id)
