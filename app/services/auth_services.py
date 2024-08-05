from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from typing import Annotated, Optional
from starlette import status
from jose import JWTError, jwt

SECRET_KEY = "PC123456"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")


async def create_access_token(
    username: str, user_id: int, expires_delta: timedelta
) -> str:
    encode = {"username": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(token: str):
    try:
        payload = dict(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
        username = payload["username"]
        user_id = payload["id"]
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )


async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None
) -> dict:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    try:
        token = authorization.split(" ")[1]  # Assuming "Bearer <token>"
        payload = dict(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
        username = payload["username"]
        user_id = payload["id"]
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
