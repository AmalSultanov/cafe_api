from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.cart_item import CartItemModel


@site.register_admin
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = [
        "id", "cart_id", "meal_id", "meal_name", "quantity", 
        "unit_price", "total_price", "created_at"]
    list_filter = [
        "id", "cart_id", "meal_name", "unit_price", "total_price", "created_at"
    ]
    list_per_page = 50
    search_fields = ["cart_id", "meal_name", "quantity"]
    page_schema = "CartItemModel"
    model = CartItemModel
    display_item_action_as_column = True
