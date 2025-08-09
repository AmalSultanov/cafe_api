from src.core.database import async_session
from src.exceptions.cart import CartNotFoundError
from src.message_broker.config import kafka_broker
from src.message_broker.events.cart import CartUpdatedEvent
from src.message_broker.topics import (
    TOPIC_CART_UPDATED
)
from src.repositories.cart.repository import CartRepository
from src.services.cart.service import CartService


@kafka_broker.subscriber(TOPIC_CART_UPDATED, group_id="cart-update-service")
async def update_cart_on_cart_updated(event: CartUpdatedEvent):
    print("Received cart updated event for cart service")
    user_id = event.user_id
    cart_data = event.cart_data

    async with async_session() as session:
        try:
            repo = CartRepository(session)
            cart_service = CartService(repo)
            upd_cart = await cart_service.update_cart(user_id, cart_data)
            print(upd_cart)
        except CartNotFoundError as e:
            print(f"Cart not found: {e}")
        except Exception as e:
            print(f"Unhandled exception in cart handler: {e}")
