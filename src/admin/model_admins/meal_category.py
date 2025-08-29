from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.meal_category import MealCategoryModel


@site.register_admin
class MealCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_filter = ["id", "name", "created_at"]
    list_per_page = 50
    enable_bulk_create = True
    search_fields = ["name"]
    page_schema = "MealCategoryModel"
    model = MealCategoryModel
    display_item_action_as_column = True
