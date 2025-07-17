from fastapi import APIRouter
from src.controllers.v1 import users, meals, meal_categories

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(users.router)
api_v1_router.include_router(meals.router)
api_v1_router.include_router(meal_categories.router)
