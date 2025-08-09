from typing import Protocol


class IEventPublisher(Protocol):
    async def publish(self, topic: str, data: dict) -> None: ...
