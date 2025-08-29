from src.exceptions.handlers.cart_item import (
    register_cart_items_exception_handlers
)
from src.exceptions.handlers.meal import register_meals_exception_handlers
from src.exceptions.handlers.user import register_users_exception_handlers


def setup_exception_handlers(app):
    register_cart_items_exception_handlers(app)
    register_users_exception_handlers(app)
    register_meals_exception_handlers(app)
