from src.core.logging import logger
from src.models.order_item import OrderItemModel
from src.repositories.order_item.interface import IOrderItemRepository


class OrderItemService:
    def __init__(self, repository: IOrderItemRepository):
        self.repository = repository

    async def bulk_create_items(self, items: list[OrderItemModel]) -> None:
        logger.info(f"Order item service: Creating {len(items)} order items")
        await self.repository.create_many(items)
        logger.info(
            f"Order item service: Created {len(items)} order items"
        )

        return items

    async def get_items(self, order_id: int) -> list[OrderItemModel]:
        logger.debug(
            f"Order item service: Fetching order items for order {order_id}"
        )
        items = await self.repository.get_all(order_id)
        logger.debug(
            f"Order item service: Found {len(items)} items for order {order_id}"
        )

        return items
