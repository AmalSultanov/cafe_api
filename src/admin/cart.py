from fastapi_amis_admin.admin import admin

from src.admin.site import site
from src.models.cart import CartModel


@site.register_admin
class CartAdmin(admin.ModelAdmin):
    page_schema = "CartModel"
    model = CartModel
