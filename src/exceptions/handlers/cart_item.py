from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.cart_item import CartItemQuantityError


def register_cart_items_exception_handlers(app: FastAPI):
    @app.exception_handler(CartItemQuantityError)
    async def cart_item_quantity_error_handler(
        request: Request, exc: CartItemQuantityError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
