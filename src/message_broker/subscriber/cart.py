from src.core.database import async_session
from src.core.logging import logger
from src.exceptions.cart import CartNotFoundError
from src.message_broker.config import kafka_broker
from src.message_broker.events.cart import CartUpdatedEvent
from src.message_broker.topics import TOPIC_CART_UPDATED
from src.repositories.cart.repository import CartRepository
from src.services.cart.service import CartService


@kafka_broker.subscriber(TOPIC_CART_UPDATED, group_id="cart-update-service")
async def update_cart_on_cart_updated(event: CartUpdatedEvent):
    logger.info(
        f"CART_SUBSCRIBER: Received CartUpdatedEvent for user {event.user_id}"
    )
    user_id = event.user_id
    cart_data = event.cart_data

    async with async_session() as session:
        try:
            repo = CartRepository(session)
            cart_service = CartService(repo)

            logger.info(f"CART_SUBSCRIBER: Updating cart for user {user_id}")
            upd_cart = await cart_service.update_cart(user_id, cart_data)

            logger.info(
                f"CART_SUBSCRIBER: Cart was updated for user "
                f"{user_id} - new total: {upd_cart.total_price}"
            )
            logger.debug(
                f"CART_SUBSCRIBER: Updated cart details: ID={upd_cart.id}, "
                f"total_price={upd_cart.total_price}"
            )

        except CartNotFoundError as e:
            logger.error(
                f"CART_SUBSCRIBER: Cart was not found for user {user_id}: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"CART_SUBSCRIBER: Failed to update cart for user {user_id}: {e}"
            )
            raise
