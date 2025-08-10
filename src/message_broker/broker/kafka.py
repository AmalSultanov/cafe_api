from typing import Any

from faststream.kafka import KafkaBroker
from src.core.logging import logger


class KafkaMessageBroker:
    def __init__(self, broker: KafkaBroker):
        self._broker = broker

    async def publish(self, topic: str, message: dict[str, Any]):
        logger.debug(f"Kafka broker publishing message to topic '{topic}'")
        try:
            await self._broker.publish(message, topic)
            logger.debug(
                f"Kafka message published successfully to topic '{topic}'"
            )
        except Exception as e:
            logger.error(f"Kafka publish failed for topic '{topic}': {e}")
            raise
