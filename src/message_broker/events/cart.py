from src.message_broker.events.base import BaseEvent
from src.schemas.cart import CartPatchUpdate


class CartUpdatedEvent(BaseEvent):
    user_id: int
    cart_data: CartPatchUpdate
