from fastapi import Depends
from faststream.kafka import KafkaBroker

from src.message_broker.broker.interface import IMessageBroker
from src.message_broker.broker.kafka import KafkaMessageBroker
from src.message_broker.config import get_kafka_broker
from src.message_broker.publisher.event_publisher import EventPublisher
from src.message_broker.publisher.interface import IEventPublisher


async def get_message_broker(
    broker: KafkaBroker = Depends(get_kafka_broker)
) -> IMessageBroker:
    return KafkaMessageBroker(broker)


async def get_event_publisher(
    broker: IMessageBroker = Depends(get_message_broker)
) -> IEventPublisher:
    return EventPublisher(broker)
