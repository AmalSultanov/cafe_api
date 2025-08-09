from typing import Any

from src.message_broker.broker.interface import IMessageBroker


class EventPublisher:
    def __init__(self, broker: IMessageBroker):
        self.broker = broker

    async def publish(self, topic: str, message: dict[str, Any]):
        await self.broker.publish(topic, message)
