from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.meal_category import MealCategoryModel


@site.register_admin
class MealCategoryModelAdmin(admin.ModelAdmin):
    page_schema = "MealCategoryModel"
    model = MealCategoryModel
