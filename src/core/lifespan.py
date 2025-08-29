from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logging import logger
from src.message_broker.config import kafka_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CafeAPI application...")
    logger.info("Initializing Kafka broker...")
    await kafka_broker.start()
    logger.info("Kafka broker started successfully")

    yield

    logger.info("Shutting down CafeAPI application...")
    logger.info("Stopping Kafka broker...")
    await kafka_broker.stop()
    logger.info("Kafka broker stopped successfully")
