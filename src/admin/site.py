from sqladmin import Admin

from src.admin.model_admins.cart import CartModelAdmin
from src.admin.model_admins.cart_item import CartItemModelAdmin
from src.admin.model_admins.meal_category import MealCategoryModelAdmin
from src.admin.model_admins.order import OrderModelAdmin
from src.admin.model_admins.order_item import OrderItemModelAdmin
from src.admin.model_admins.user import UserModelAdmin, UserIdentityModelAdmin
from src.admin.services import authentication_backend
from src.core.database import async_engine
from src.core.logging import logger

logger.info("Preparing SQLAdmin factory...")


def setup_admin(app):
    admin = Admin(
        app,
        async_engine,
        authentication_backend=authentication_backend
    )

    admin.add_view(CartModelAdmin)
    admin.add_view(CartItemModelAdmin)
    admin.add_view(MealCategoryModelAdmin)
    admin.add_view(OrderModelAdmin)
    admin.add_view(OrderItemModelAdmin)
    admin.add_view(UserModelAdmin)
    admin.add_view(UserIdentityModelAdmin)

    return admin
