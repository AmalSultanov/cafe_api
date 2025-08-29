from fastapi import FastAPI
from faststream import FastStream

from src.admin.custom_controllers.admin import admin_router
from src.admin.site import site
from src.controllers.v1 import api_v1_router
from src.core.config import get_settings
from src.core.constants import APP_SUMMARY, APP_DESCRIPTION
from src.core.exceptions_setup import setup_exception_handlers
from src.core.logging import setup_logging, logger
from src.core.lifespan import lifespan
from src.message_broker.config import kafka_broker
from src.middlewares.cors import setup_cors
from src.middlewares.profiler import setup_profiler
from src.monitoring.prometheus import setup_instrumentator

settings = get_settings()
setup_logging()
logger.info("Logging was configured")

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
logger.info("FastStream was configured")
logger.info("Configuring FastAPI application...")

app.include_router(api_v1_router, prefix="/api")
logger.info("API v1 router was included")
app.include_router(admin_router)
logger.info("Admin router was included")

site.mount_app(app)
logger.info("Admin site was mounted")

setup_cors(app, settings)
logger.info("CORS middleware was configured")

setup_profiler(app)
logger.info("Profile middleware was configured")

setup_exception_handlers(app)
logger.info("Exception handlers were registered")

setup_instrumentator(app)
logger.info("Prometheus Instrumentator was configured")
logger.info("CafeAPI application was configured")
