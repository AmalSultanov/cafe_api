from typing import Any

from src.core.logging import logger
from src.message_broker.broker.interface import IMessageBroker


class EventPublisher:
    def __init__(self, broker: IMessageBroker):
        self.broker = broker

    async def publish(self, topic: str, message: dict[str, Any]):
        logger.info(f"Publishing event to topic '{topic}': {message}")
        try:
            await self.broker.publish(topic, message)
            logger.info(f"Event published successfully to topic '{topic}'")
        except Exception as e:
            logger.error(f"Failed to publish event to topic '{topic}': {e}")
            raise
