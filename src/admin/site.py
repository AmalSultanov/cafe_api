import src.admin

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

from src.core.config import (
    POSTGRES_DATABASE_URL, FASTAPI_HOST, FASTAPI_PORT, FASTAPI_DEBUG,
    FASTAPI_VERSION
)

site = AdminSite(settings=Settings(
    host=FASTAPI_HOST,
    port=FASTAPI_PORT,
    debug=FASTAPI_DEBUG,
    version=FASTAPI_VERSION,
    site_title="Cafe API Admin Dashboard",
    database_url_async=POSTGRES_DATABASE_URL,
    amis_theme="dark"
))
