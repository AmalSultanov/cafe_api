from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.order_item import OrderItemModel


@site.register_admin
class OrderItemModelAdmin(admin.ModelAdmin):
    page_schema = "OrderItemModel"
    model = OrderItemModel
