from fastapi import APIRouter
from src.controllers.v1 import users, meals, meal_categories, cart, cart_items

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(meal_categories.router)
api_v1_router.include_router(meals.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(cart.router)
api_v1_router.include_router(cart_items.router)
