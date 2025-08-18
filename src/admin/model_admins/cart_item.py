from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.cart_item import CartItemModel


@site.register_admin
class CartItemModelAdmin(admin.ModelAdmin):
    page_schema = "CartItemModel"
    model = CartItemModel
