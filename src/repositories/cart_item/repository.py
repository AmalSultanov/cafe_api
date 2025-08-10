from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logging import logger
from src.models.cart_item import CartItemModel


class CartItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, cart_data: dict[str, int | float]) -> CartItemModel:
        logger.debug(f"Cart item repo: Creating cart item with data: {cart_data}")
        item = CartItemModel(**cart_data)
        self.db.add(item)

        await self.db.commit()
        await self.db.refresh(item)
        logger.info(
            f"Cart item repo: Cart item created successfully with "
            f"ID: {item.id}, meal_id: {item.meal_id}, quantity: {item.quantity}"
        )

        return item

    async def get_all_by_cart_id(self, cart_id: int) -> list[CartItemModel]:
        logger.debug(f"Cart item repo: Getting all cart items for cart {cart_id}")
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        items = result.scalars().all()
        logger.debug(f"Cart item repo: Got {len(items)} cart items for cart {cart_id}")

        return items

    async def get_by_id(self, item_id: int) -> CartItemModel | None:
        logger.debug(f"Cart item repo: Getting cart item by ID: {item_id}")
        result = await self.db.execute(
            select(CartItemModel).where(CartItemModel.id == item_id)
        )
        item = result.scalar_one_or_none()

        if item:
            logger.debug(
                f"Cart item repo: Found cart item {item_id}: "
                f"meal_id={item.meal_id}, quantity={item.quantity}"
            )
        else:
            logger.debug(f"Cart item repo: Cart item {item_id} not found")

        return item

    async def get_by_cart_and_item_id(
        self, cart_id: int, item_id: int
    ) -> CartItemModel | None:
        logger.debug(f"Cart item repo: Getting cart item {item_id} from cart {cart_id}")
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
                f"Cart item repo: Found cart item {item_id} in cart {cart_id}"
            )
        else:
            logger.debug(
                f"Cart item repo: Cart item {item_id} was not found in cart {cart_id}"
            )
        return item

    async def get_by_cart_and_meal_id(
        self, cart_id: int, meal_id: int
    ) -> CartItemModel | None:
        logger.debug(
            f"Cart item repo: Getting cart item for meal {meal_id} in cart {cart_id}"
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
                f"Cart item repo: Found cart item for meal {meal_id} in cart {cart_id}"
            )
        else:
            logger.debug(
                f"Cart item repo: No cart item was found for "
                f"meal {meal_id} in cart {cart_id}"
            )
        return item

    async def update(
        self, item_id: int, cart_data: dict[str, int | str]
    ) -> CartItemModel:
        logger.debug(
            f"Cart item repo: Updating cart item {item_id} with data: {cart_data}"
        )
        await self.db.execute(
            update(CartItemModel)
            .where(CartItemModel.id == item_id)
            .values(**cart_data)
        )
        await self.db.commit()
        updated_item = await self.get_by_id(item_id)
        logger.info(f"Cart item repo: Cart item {item_id} was updated")

        return updated_item

    async def delete_by_id(self, item_id: int) -> None:
        logger.debug(f"Cart item repo: Deleting cart item {item_id}")
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.id == item_id)
        )
        await self.db.commit()
        logger.info(f"Cart item repo: Cart item {item_id} was deleted")

    async def delete_all_by_cart_id(self, cart_id: int) -> None:
        logger.debug(
            f"Cart item repo: Deleting all cart items for cart {cart_id}"
        )
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        await self.db.commit()
        logger.info(
            f"Cart item repo: All cart items were deleted for cart {cart_id}"
        )
