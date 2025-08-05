from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET_KEY = "7894372312d62e90fbc201ef22b0c38f73e25d935ceaa560a5b729617419eb2f"
JWT_REFRESH_SECRET_KEY = "21c884c0a500459df27ca0865256ca462700e91bd89a8559ad59a9faa0a74b3d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(subject: int) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: int) -> str:
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }

    return jwt.encode(payload, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])


def decode_refresh_token(token: str) -> dict:
    return jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
