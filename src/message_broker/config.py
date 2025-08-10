from faststream.kafka import KafkaBroker

from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()
logger.info(
    f"Initializing Kafka broker with servers: {settings.kafka_bootstrap_servers}"
)
kafka_broker = KafkaBroker(settings.kafka_bootstrap_servers)


async def get_kafka_broker() -> KafkaBroker:
    logger.debug("Returning Kafka broker instance")
    return kafka_broker
