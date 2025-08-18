from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    status: str
