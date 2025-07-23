from fastapi import FastAPI

from src.admin.site import site
from src.controllers.v1 import api_v1_router
from src.core.config import FASTAPI_VERSION
from src.core.constants import APP_SUMMARY, APP_DESCRIPTION
from src.exceptions.handlers.cart_item import (
    register_cart_items_exception_handlers
)

app = FastAPI(
    title="CafeAPI",
    summary=APP_SUMMARY,
    description=APP_DESCRIPTION,
    version=FASTAPI_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(api_v1_router, prefix="/api")
site.mount_app(app)

register_cart_items_exception_handlers(app)
