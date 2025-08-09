from faststream.kafka import KafkaBroker

from src.core.config import get_settings

settings = get_settings()
kafka_broker = KafkaBroker(settings.kafka_bootstrap_servers)


async def get_kafka_broker() -> KafkaBroker:
    return kafka_broker
