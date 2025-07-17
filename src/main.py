from fastapi import FastAPI

from src.core.constants import APP_SUMMARY, APP_DESCRIPTION, APP_VERSION
from src.controllers.v1 import api_v1_router

app = FastAPI(
    title="CafeAPI",
    summary=APP_SUMMARY,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(api_v1_router, prefix="/api")
