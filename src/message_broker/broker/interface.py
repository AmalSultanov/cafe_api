from typing import Protocol, Any


class IMessageBroker(Protocol):
    async def publish(self, topic: str, message: dict[str, Any]): ...
