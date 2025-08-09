from typing import Any

from faststream.kafka import KafkaBroker


class KafkaMessageBroker:
    def __init__(self, broker: KafkaBroker):
        self._broker = broker

    async def publish(self, topic: str, message: dict[str, Any]):
        await self._broker.publish(message, topic)
