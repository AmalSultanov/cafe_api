from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.order import OrderModel


@site.register_admin
class OrderModelAdmin(admin.ModelAdmin):
    page_schema = "OrderModel"
    model = OrderModel
