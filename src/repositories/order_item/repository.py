from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.order_item import OrderItemModel


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, items: list[OrderItemModel]) -> None:
        logger.debug(f"Order item repo: Creating {len(items)} order items")
        self.db.add_all(items)
        logger.debug(
            f"Order item repo: {len(items)} order items added to session"
        )

    async def get_all(self, order_id: int) -> list[OrderItemModel]:
        logger.debug(f"Order item repo: Getting all order items for order {order_id}")
        result = await self.db.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        items = result.scalars().all()
        logger.debug(
            f"Order item repo: Retrieved {len(items)} order items for order {order_id}"
        )

        return items
