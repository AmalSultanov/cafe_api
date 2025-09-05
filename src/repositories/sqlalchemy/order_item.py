from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.order_item import OrderItemModel


class SQLAlchemyOrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, items: list[OrderItemModel]) -> None:
        logger.debug(
            f"SQLAlchemy Order Item repo: Creating {len(items)} items"
        )
        self.db.add_all(items)
        logger.debug(
            f"SQLAlchemy Order Item repo: {len(items)} items added to session"
        )

    async def get_all(self, order_id: int) -> list[OrderItemModel]:
        logger.debug(
            f"SQLAlchemy Order Item repo: Getting all order items "
            f"for order {order_id}"
        )
        result = await self.db.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        items = result.scalars().all()
        logger.debug(
            f"SQLAlchemy Order Item repo: {len(items)} items for order {order_id}"
        )

        return items
