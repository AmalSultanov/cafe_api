from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.user import UserModel, UserIdentityModel


@site.register_admin
class UserAdmin(admin.ModelAdmin):
    page_schema = "UserModel"
    model = UserModel


@site.register_admin
class UserIdentityAdmin(admin.ModelAdmin):
    page_schema = "UserIdentityModel"
    model = UserIdentityModel
