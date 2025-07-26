from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.meal import MealPriceError


def register_meals_exception_handlers(app: FastAPI):
    @app.exception_handler(MealPriceError)
    async def meal_unit_price_error_handler(
        request: Request, exc: MealPriceError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
