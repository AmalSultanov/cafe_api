from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import HomeAdmin, APIDocsApp
from fastapi_amis_admin.admin import admin
from src.core.config import get_settings
from src.core.logging import logger
from fastapi import FastAPI
from fastapi_amis_admin.crud.utils import SqlalchemyDatabase

settings = get_settings()


class NoFileAdminSite(admin.BaseAdminSite):
    def __init__(
        self,
        settings: Settings,
        *,
        fastapi: FastAPI = None,
        engine: SqlalchemyDatabase = None
    ):
        super().__init__(settings, fastapi=fastapi, engine=engine)
        self.register_admin(HomeAdmin, APIDocsApp)


logger.info("Initializing Admin Dashboard...")
try:
    site = NoFileAdminSite(
        settings=Settings(
            host=settings.fastapi_host,
            port=settings.fastapi_port,
            debug=settings.fastapi_debug,
            version=settings.fastapi_version,
            site_title="Cafe API Admin Dashboard",
            database_url_async=settings.postgres_url,
            language="en_US",
            amis_theme="dark"
        )
    )
    logger.info("Admin Dashboard initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Admin Dashboard: {e}")
    raise
