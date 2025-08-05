from src.message_broker.events.base import BaseEvent
from src.schemas.user import IdentityCreate


class UserCreatedEvent(BaseEvent):
    user_id: int
    identity_data: IdentityCreate | None = None
