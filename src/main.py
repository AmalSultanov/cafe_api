from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream import FastStream
from fastapi.middleware.cors import CORSMiddleware

from src.admin.site import site
from src.controllers.v1 import api_v1_router
from src.core.config import get_settings
from src.core.constants import APP_SUMMARY, APP_DESCRIPTION
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_broker.start()
    yield
    await kafka_broker.stop()

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

app.include_router(api_v1_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
site.mount_app(app)

register_cart_items_exception_handlers(app)
register_users_exception_handlers(app)
register_meals_exception_handlers(app)
