import src.admin

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

from src.core.config import get_settings

settings = get_settings()

site = AdminSite(settings=Settings(
    host=settings.fastapi_host,
    port=settings.fastapi_port,
    debug=settings.fastapi_debug,
    version=settings.fastapi_version,
    site_title="Cafe API Admin Dashboard",
    database_url_async=settings.postgres_url,
    amis_theme="dark"
))
