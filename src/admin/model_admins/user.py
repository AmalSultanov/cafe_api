from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.user import UserModel, UserIdentityModel


@site.register_admin
class UserModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "surname", "phone_number", "created_at"]
    list_filter = ["id", "name", "surname", "phone_number", "created_at"]
    list_per_page = 50
    search_fields = ["name", "surname", "phone_number"]
    page_schema = "UserModel"
    model = UserModel
    display_item_action_as_column = True


@site.register_admin
class UserIdentityModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "provider_id", "username", "created_at"]
    list_filter = ["id", "user_id", "provider_id", "username", "created_at"]
    list_per_page = 50
    search_fields = ["user_id", "provider_id", "username"]
    page_schema = "UserIdentityModel"
    model = UserIdentityModel
    display_item_action_as_column = True
