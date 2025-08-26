from contextlib import asynccontextmanager

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from prometheus_fastapi_instrumentator import Instrumentator

from src.admin.custom_controllers.admin import admin_router
from src.admin.site import site
from src.controllers.v1 import api_v1_router
from src.core.config import get_settings
from src.core.constants import APP_SUMMARY, APP_DESCRIPTION
from src.core.logging import setup_logging, logger
from src.exceptions.handlers.cart_item import (
    register_cart_items_exception_handlers
)
from src.exceptions.handlers.meal import register_meals_exception_handlers
from src.exceptions.handlers.user import register_users_exception_handlers
from src.message_broker.config import kafka_broker
from src.message_broker.subscriber import cart, user
from src.metrics import CPU_USAGE, MEMORY_USAGE

settings = get_settings()
setup_logging()


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


app = FastAPI(
    title="CafeAPI",
    summary=APP_SUMMARY,
    description=APP_DESCRIPTION,
    version=settings.fastapi_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)
faststream = FastStream(kafka_broker)

logger.info("Configuring FastAPI application...")

app.include_router(api_v1_router, prefix="/api")
logger.info("API v1 router was included")
app.include_router(admin_router)
logger.info("Admin router was included")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
logger.info("CORS middleware was configured")

site.mount_app(app)
logger.info("Admin site was mounted")

register_cart_items_exception_handlers(app)
register_users_exception_handlers(app)
register_meals_exception_handlers(app)

logger.info("Exception handlers were registered")
logger.info("CafeAPI application was configured successfully")


def update_system_metrics(info):
    try:
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.Process().memory_info().rss)
    except Exception as e:
        logger.warning(f"Failed to update system metrics: {e}")


instrumentator = Instrumentator()
instrumentator.add(update_system_metrics)
instrumentator.instrument(app).expose(app)
logger.info("Prometheus FastAPI Instrumentator was configured successfully")
