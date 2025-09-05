from src.core.database import async_session
from src.core.logging import logger
from src.exceptions.cart import CartAlreadyExistsError
from src.message_broker.config import kafka_broker
from src.message_broker.events.user import UserCreatedEvent
from src.message_broker.topics import (
    TOPIC_USER_CREATED
)
from src.repositories.sqlalchemy.cart import SQLAlchemyCartRepository
from src.services.cart.service import CartService


@kafka_broker.subscriber(TOPIC_USER_CREATED, group_id="cart-create-service")
async def create_cart_on_user_created(event: UserCreatedEvent):
    logger.info(
        f"User subscriber: Received UserCreatedEvent for user {event.user_id}"
    )
    user_id = event.user_id

    async with async_session() as session:
        try:
            logger.debug(
                f"User subscriber: Initializing cart repo and service for user {user_id}"
            )
            repo = SQLAlchemyCartRepository(session)
            cart_service = CartService(repo)

            logger.info(f"User subscriber: Creating cart for user {user_id}")
            cart = await cart_service.create_cart(user_id)

            logger.info(
                f"User subscriber: Cart was created for user "
                f"{user_id} with cart ID: {cart.id}"
            )

        except CartAlreadyExistsError as e:
            logger.warning(
                f"User subscriber: Cart already exists for user {user_id}: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"User subscriber: Failed to create cart for user {user_id}: {e}"
            )
            raise
