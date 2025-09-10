import logging
import secrets

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jwt import InvalidTokenError

logging.basicConfig(level=logging.DEBUG)
from app.schema import schemas
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
secrete_key = secrets.token_hex(32)
logging.debug(f"auto generated secrete key {secrete_key} ")
ALGORITHM = "HS256"  # Hashing method HMAC-SHA256
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Defines how long a token should stay valid
REFRESH_TOKEN_EXPIRY_DAYS = 10


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    data_copy = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    data_copy.update({
        "exp": expire,
        "type": "refresh"
    })
    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception=None):
    try:
        logging.debug(f"token = {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.debug(f"payload data = {payload}")
        user_id = payload.get(
            "sub")  # JWT payload is just a dictionary after decoding, e.g.: Like{"sub":username,"exp":11212}
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=F"Invalid Token")
        return schemas.TokenData(userID=user_id)  # Returns string TokenData(email="alice@example.com")
    except InvalidTokenError:
        raise credentials_exception


def verify_refresh_token(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decode_token.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return decode_token

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")
