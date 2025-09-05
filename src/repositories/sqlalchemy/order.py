from datetime import datetime
from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.core.logging import logger
from src.models.order import OrderModel
from src.models.order_item import OrderItemModel


class SQLAlchemyOrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_with_items(
        self,
        user_id: int,
        order_data: dict[str, str | Decimal | datetime],
        items_data: list[dict[str, int | str]]
    ) -> OrderModel:
        logger.debug(
            f"SQLAlchemy Order repo: Creating order for user {user_id} "
            f"with {len(items_data)} items"
        )
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
        logger.info(
            f"SQLAlchemy Order repo: Order was created for user "
            f"{user_id} with ID: {order.id}"
        )

        return await self.get_by_user_and_order_id(user_id, order.id)

    async def get_all(self, user_id: int) -> list[OrderModel]:
        logger.debug(
            f"SQLAlchemy Order repo: Getting all orders for user {user_id}"
        )
        result = await self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.user_id == user_id)
            .order_by(OrderModel.created_at.desc())
        )
        orders = result.scalars().all()
        logger.debug(
            f"SQLAlchemy Order repo: {len(orders)} orders for user {user_id}"
        )

        return orders

    async def get_by_user_and_order_id(
        self, user_id: int, order_id: int
    ) -> OrderModel | None:
        logger.debug(
            f"SQLAlchemy Order repo: Getting order {order_id} for user {user_id}"
        )
        result = await self.db.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        order = result.scalar_one_or_none()

        if order:
            logger.debug(
                f"SQLAlchemy Order repo: Found order {order_id} for user "
                f"{user_id} with {len(order.items)} items"
            )
        else:
            logger.debug(
                f"SQLAlchemy Order repo: Order {order_id} not found "
                f"for user {user_id}"
            )

        return order

    async def delete_one(self, user_id: int, order_id: int) -> None:
        logger.debug(
            f"SQLAlchemy Order repo: Deleting order {order_id} "
            f"for user {user_id}"
        )
        await self.db.execute(
            delete(OrderModel)
            .where(OrderModel.id == order_id, OrderModel.user_id == user_id)
        )
        await self.db.commit()
        logger.info(
            f"SQLAlchemy Order repo: Order {order_id} deleted for user {user_id}"
        )

    async def delete_all(self, user_id: int) -> None:
        logger.debug(
            f"SQLAlchemy Order repo: Deleting all orders for user {user_id}"
        )
        await self.db.execute(
            delete(OrderModel).where(OrderModel.user_id == user_id)
        )
        await self.db.commit()
        logger.info(
            f"SQLAlchemy Order repo: All orders were deleted for user {user_id}"
        )
