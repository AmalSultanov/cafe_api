from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.order_item import OrderItemModel


@site.register_admin
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = [
        "id", "order_id", "meal_id", "meal_name", "quantity", 
        "unit_price", "total_price", "created_at"
    ]
    list_filter = [
        "id", "order_id", "meal_id", "meal_name", "quantity", 
        "unit_price", "total_price", "created_at"
    ]
    list_per_page = 50
    search_fields = ["order_id", "meal_id", "meal_name"]
    page_schema = "OrderItemModel"
    model = OrderItemModel
    display_item_action_as_column = True
