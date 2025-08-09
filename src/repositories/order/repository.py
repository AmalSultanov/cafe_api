from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload

from src.models.order import OrderModel
from src.models.order_item import OrderItemModel


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_with_items(
        self,
        user_id: int,
        order_data: dict[str, str | Decimal | datetime],
        items_data: list[dict[str, int | str]]
    ) -> OrderModel:
        order = OrderModel(user_id=user_id, **order_data)
        self.db.add(order)
        await self.db.flush()

        order_items = [
            OrderItemModel(
                order_id=order.id,
                meal_id=item_data["meal_id"],
                quantity=item_data["quantity"],
                meal_name=item_data["meal_name"],
                unit_price=item_data["unit_price"],
                total_price=item_data["total_price"]
            )
            for item_data in items_data
        ]

        self.db.add_all(order_items)
        await self.db.commit()
        await self.db.refresh(order)

        return await self.get_by_user_and_order_id(user_id, order.id)

    async def get_all(self, user_id: int) -> list[OrderModel]:
        result = await self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.user_id == user_id)
            .order_by(OrderModel.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_user_and_order_id(
        self, user_id: int, order_id: int
    ) -> OrderModel | None:
        result = await self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def delete_one(self, user_id: int, order_id: int) -> None:
        await self.db.execute(
            delete(OrderModel)
            .where(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        await self.db.commit()

    async def delete_all(self, user_id: int) -> None:
        await self.db.execute(
            delete(OrderModel).where(OrderModel.user_id == user_id)
        )
        await self.db.commit()
