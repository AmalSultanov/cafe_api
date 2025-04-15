from fastapi import FastAPI

from src.meals.router import meals_router
from src.users.router import users_router

app = FastAPI(
    title='CafeAPI',
    summary='A set of API endpoints designed for '
            'integration with external services.',
    docs_url='/docs',
    redoc_url='/redoc'
)
app.include_router(users_router)
app.include_router(meals_router)
