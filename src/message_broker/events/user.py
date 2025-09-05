from src.message_broker.events.base import BaseEvent


class UserCreatedEvent(BaseEvent):
    user_id: int
