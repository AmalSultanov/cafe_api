from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update

from src.models.cart import CartModel


class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int) -> CartModel:
        cart = CartModel(user_id=user_id)
        self.db.add(cart)

        await self.db.commit()
        await self.db.refresh(cart)

        return cart

    async def get_by_user_id(self, user_id: int) -> CartModel | None:
        result = await self.db.execute(
            select(CartModel).where(CartModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, user_id: int, cart_data: dict[str, str]
    ) -> CartModel | None:
        await self.db.execute(
            update(CartModel)
            .where(CartModel.user_id == user_id)
            .values(**cart_data)
        )
        await self.db.commit()
        return await self.get_by_user_id(user_id)

    async def delete(self, user_id: int) -> None:
        await self.db.execute(
            delete(CartModel).where(CartModel.user_id == user_id)
        )
        await self.db.commit()
