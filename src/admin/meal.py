from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.meal import MealModel


@site.register_admin
class MealAdmin(admin.ModelAdmin):
    page_schema = "MealModel"
    model = MealModel
