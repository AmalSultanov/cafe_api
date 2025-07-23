from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.cart_item import CartItemModel


class CartItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, cart_data: dict[str, int | float]) -> CartItemModel:
        item = CartItemModel(**cart_data)
        self.db.add(item)

        await self.db.commit()
        await self.db.refresh(item)

        return item

    async def get_all_by_cart_id(self, cart_id: int) -> list[CartItemModel]:
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        return result.scalars().all()

    async def get_by_id(self, item_id: int) -> CartItemModel | None:
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_by_cart_and_item_id(
        self, cart_id: int, item_id: int
    ) -> CartItemModel | None:
        result = await self.db.execute(
            select(CartItemModel)
            .where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.id == item_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_cart_and_meal_id(
        self, cart_id: int, meal_id: int
    ) -> CartItemModel | None:
        result = await self.db.execute(
            select(CartItemModel)
            .where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.meal_id == meal_id
            )
        )
        return result.scalar_one_or_none()

    async def update(
        self, item_id: int, cart_data: dict[str, int]
    ) -> CartItemModel:
        await self.db.execute(
            update(CartItemModel)
            .where(CartItemModel.id == item_id)
            .values(**cart_data)
        )
        await self.db.commit()
        return await self.get_by_id(item_id)

    async def delete_by_id(self, item_id: int) -> None:
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.id == item_id)
        )
        await self.db.commit()

    async def delete_all_by_cart_id(self, cart_id: int) -> None:
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        await self.db.commit()
