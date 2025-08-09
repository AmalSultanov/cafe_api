from src.core.database import async_session
from src.exceptions.cart import CartAlreadyExistsError
from src.message_broker.config import kafka_broker
from src.message_broker.events.user import UserCreatedEvent
from src.message_broker.topics import (
    TOPIC_USER_CREATED
)
from src.repositories.cart.repository import CartRepository
from src.services.cart.service import CartService


@kafka_broker.subscriber(TOPIC_USER_CREATED, group_id="cart-create-service")
async def create_cart_on_user_created(event: UserCreatedEvent):
    print("Received user created event for cart service")
    user_id = event.user_id
    async with async_session() as session:
        try:
            repo = CartRepository(session)
            cart_service = CartService(repo)
            cart = await cart_service.create_cart(user_id)
            print(cart)
        except CartAlreadyExistsError as e:
            print(f"Cart already exists: {e}")
        except Exception as e:
            print(f"Unhandled exception in cart handler: {e}")
