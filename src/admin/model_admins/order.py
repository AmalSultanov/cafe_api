from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.order import OrderModel


@site.register_admin
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user_id", "cart_id", "total_price", 
        "delivery_address", "created_at"
    ]
    list_filter = ["id", "user_id", "cart_id", "total_price", "created_at"]
    list_per_page = 50
    search_fields = ["image_url", "name", "category_id"]
    page_schema = "OrderModel"
    model = OrderModel
    display_item_action_as_column = True
