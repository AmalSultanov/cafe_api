from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream import FastStream
from fastapi.middleware.cors import CORSMiddleware

from src.admin.cusotm_controllers.admin import admin_router
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
from src.message_broker.subscriber import cart, user
from src.message_broker.config import kafka_broker

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
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
logger.info("API v1 router included")
app.include_router(admin_router)
logger.info("Admin router included")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
logger.info("CORS middleware configured")

site.mount_app(app)
logger.info("Admin site mounted")

register_cart_items_exception_handlers(app)
register_users_exception_handlers(app)
register_meals_exception_handlers(app)

logger.info("Exception handlers registered")
logger.info("CafeAPI application configured successfully")
