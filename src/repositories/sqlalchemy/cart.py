from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update

from src.core.logging import logger
from src.models.cart import CartModel


class SQLAlchemyCartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int) -> CartModel:
        logger.debug(f"SQLAlchemy Cart repo: Creating cart for user {user_id}")
        cart = CartModel(user_id=user_id)
        self.db.add(cart)

        await self.db.commit()
        await self.db.refresh(cart)
        logger.info(
            f"SQLAlchemy Cart repo: New cart {cart.id} for user {user_id}"
        )

        return cart

    async def get_by_user_id(self, user_id: int) -> CartModel | None:
        logger.debug(f"SQLAlchemy Cart repo: Getting cart for user {user_id}")
        result = await self.db.execute(
            select(CartModel).where(CartModel.user_id == user_id)
        )
        cart = result.scalar_one_or_none()

        if cart:
            logger.debug(
                f"SQLAlchemy Cart repo: Found cart {cart.id} "
                f"for user {user_id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Cart repo: No cart found for "
                f"user {user_id}"
            )

        return cart

    async def update(
        self, user_id: int, cart_data: dict[str, str]
    ) -> CartModel | None:
        logger.debug(
            f"SQLAlchemy Cart repo: Updating cart for user {user_id}, "
            f"data: {cart_data}"
        )
        await self.db.execute(
            update(CartModel)
            .where(CartModel.user_id == user_id)
            .values(**cart_data)
        )
        await self.db.commit()

        updated_cart = await self.get_by_user_id(user_id)
        logger.info(f"SQLAlchemy Cart repo: Cart updated for user {user_id}")

        return updated_cart

    async def delete(self, user_id: int) -> None:
        logger.debug(f"SQLAlchemy Cart repo: Deleting cart for user {user_id}")
        await self.db.execute(
            delete(CartModel).where(CartModel.user_id == user_id)
        )
        await self.db.commit()
        logger.info(f"SQLAlchemy Cart repo: Cart deleted for user {user_id}")
