from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.cart import CartModel


@site.register_admin
class CartModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "total_price", "created_at"]
    list_filter = ["id", "user_id", "total_price", "created_at"]
    list_per_page = 50
    search_fields = ["user_id", "total_price", "category_id"]
    page_schema = "CartModel"
    model = CartModel
    display_item_action_as_column = True
