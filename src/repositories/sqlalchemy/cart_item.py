from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.cart_item import CartItemModel


class SQLAlchemyCartItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, cart_data: dict[str, int | float]) -> CartItemModel:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Creating cart item, data: {cart_data}"
        )
        item = CartItemModel(**cart_data)
        self.db.add(item)

        await self.db.commit()
        await self.db.refresh(item)
        logger.info(
            f"SQLAlchemy Cart Item repo: Cart item created with ID: "
            f"{item.id}, meal_id: {item.meal_id}, quantity: {item.quantity}"
        )

        return item

    async def get_all_by_cart_id(self, cart_id: int) -> list[CartItemModel]:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Getting cart items for cart {cart_id}"
        )
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        items = result.scalars().all()
        logger.debug(
            f"SQLAlchemy Cart Item repo: {len(items)} items for cart {cart_id}"
        )

        return items

    async def get_by_id(self, item_id: int) -> CartItemModel | None:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Getting item by ID: {item_id}"
        )
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.id == item_id)
        )
        item = result.scalar_one_or_none()

        if item:
            logger.debug(
                f"SQLAlchemy Cart Item repo: Found cart item {item_id}: "
                f"meal_id={item.meal_id}, quantity={item.quantity}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Cart Item repo: Item {item_id} was not found"
            )

        return item

    async def get_by_cart_and_item_id(
        self, cart_id: int, item_id: int
    ) -> CartItemModel | None:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Getting item {item_id} "
            f"from cart {cart_id}"
        )
        result = await self.db.execute(
            select(CartItemModel)
            .where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.id == item_id
            )
        )
        item = result.scalar_one_or_none()

        if item:
            logger.debug(
                f"SQLAlchemy Cart Item repo: Found item {item_id} "
                f"in cart {cart_id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Cart Item repo: Item {item_id} was not "
                f"found in cart {cart_id}"
            )
        return item

    async def get_by_cart_and_meal_id(
        self, cart_id: int, meal_id: int
    ) -> CartItemModel | None:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Getting item for meal {meal_id} "
            f"in cart {cart_id}"
        )
        result = await self.db.execute(
            select(CartItemModel)
            .where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.meal_id == meal_id
            )
        )
        item = result.scalar_one_or_none()

        if item:
            logger.debug(
                f"SQLAlchemy Cart Item repo: Found item for meal "
                f"{meal_id} in cart {cart_id}"
            )
        else:
            logger.debug(
                f"SQLAlchemy Cart Item repo: No item was found for "
                f"meal {meal_id} in cart {cart_id}"
            )
        return item

    async def update(
        self, item_id: int, cart_data: dict[str, int | str]
    ) -> CartItemModel:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Updating item {item_id}, "
            f"data: {cart_data}"
        )
        await self.db.execute(
            update(CartItemModel)
            .where(CartItemModel.id == item_id)
            .values(**cart_data)
        )
        await self.db.commit()
        updated_item = await self.get_by_id(item_id)
        logger.info(f"SQLAlchemy Cart Item repo: Item {item_id} was updated")

        return updated_item

    async def delete_by_id(self, item_id: int) -> None:
        logger.debug(f"SQLAlchemy Cart Item repo: Deleting item {item_id}")
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.id == item_id)
        )
        await self.db.commit()
        logger.info(f"SQLAlchemy Cart Item repo: Item {item_id} was deleted")

    async def delete_all_by_cart_id(self, cart_id: int) -> None:
        logger.debug(
            f"SQLAlchemy Cart Item repo: Deleting all items for cart {cart_id}"
        )
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        await self.db.commit()
        logger.info(
            f"SQLAlchemy Cart Item repo: All items were "
            f"deleted from cart {cart_id}"
        )
