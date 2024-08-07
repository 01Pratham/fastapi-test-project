from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from typing import Annotated, Optional
from starlette import status
from jose import JWTError, jwt


class AuthServices:

    _SECRET_KEY = "PC123456"
    _ALGORITHM = "HS256"
    _bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")
    _token_type = "Bearer"

    @classmethod
    async def create_access_token(
        cls, username: str, user_id: int, expires_delta: timedelta
    ) -> str:
        encode = {"username": username, "id": user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
        return (
            cls._token_type
            + " "
            + jwt.encode(encode, cls._SECRET_KEY, algorithm=cls._ALGORITHM)
        )

    @classmethod
    async def verify_token(cls, token: str):
        try:
            payload = dict(
                jwt.decode(token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
            )
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

    @classmethod
    async def get_current_user(
        cls, authorization: Annotated[Optional[str], Header()]
    ) -> dict:
        if authorization is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )
        try:
            AuthSplit = authorization.split(" ")
            if AuthSplit[0].lower() != cls._token_type.lower():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token Contains unexpected values",
                )

            token = AuthSplit[1]
            payload = dict(
                jwt.decode(token, cls._SECRET_KEY, algorithms=[cls._ALGORITHM])
            )
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

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._bcrypt_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._bcrypt_context.verify(plain_password, hashed_password)
