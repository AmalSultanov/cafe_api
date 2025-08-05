from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
