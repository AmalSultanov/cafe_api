from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.user import UserPhoneError


def register_users_exception_handlers(app: FastAPI):
    @app.exception_handler(UserPhoneError)
    async def user_phone_number_error_handler(
        request: Request, exc: UserPhoneError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
