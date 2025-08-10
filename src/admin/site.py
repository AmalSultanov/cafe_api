import src.admin

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()

logger.info("Initializing Admin Dashboard...")
logger.info(
    f"Admin Dashboard URL: {settings.fastapi_host}:{settings.fastapi_port}/admin"
)

try:
    site = AdminSite(settings=Settings(
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        debug=settings.fastapi_debug,
        version=settings.fastapi_version,
        site_title="Cafe API Admin Dashboard",
        database_url_async=settings.postgres_url,
        amis_theme="dark"
    ))
    logger.info("Admin Dashboard initialized successfully with dark theme")
except Exception as e:
    logger.error(f"Failed to initialize Admin Dashboard: {e}")
    raise
