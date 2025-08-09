from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.order_item import OrderItemModel


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, items: list[OrderItemModel]) -> None:
        self.db.add_all(items)

    async def get_all(self, order_id: int) -> list[OrderItemModel]:
        result = await self.db.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        return result.scalars().all()
