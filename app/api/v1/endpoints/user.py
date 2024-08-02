from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import List, Annotated
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import users as UserModel
from schemas import user as UserSchemas
from schemas import token as TokenSchema
from services import user_services as UserServices
from services import auth_services as AuthServices
from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


# @router.post("/")
@router.post(
    "/", response_model=UserSchemas.UserResponse, status_code=status.HTTP_201_CREATED
)
async def post_user(user: UserSchemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserServices.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
        )
    return Response(
        json_data=UserServices.create_user(db=db, user=user),
        message="Records Inserted Successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/", response_model=UserSchemas.UserResponse, status_code=status.HTTP_200_OK
)
async def get_users(
    limit: int = 100,
    deleted: bool = False,
    db: Session = Depends(get_db),
    current_user: UserSchemas.AuthUser = Depends(AuthServices.get_current_user),
):
    users = UserServices.get_users(db=db, limit=limit, deleted=deleted)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/id/{user_id}/",
    response_model=UserSchemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchemas.AuthUser = Depends(AuthServices.get_current_user),
):
    db_user = UserServices.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(
        json_data=db_user,
        message=f"Data for user {user_id}",
        status_code=status.HTTP_200_OK,
    )


# @router.put("/update/{user_id}")
@router.put(
    "/update/{user_id}",
    response_model=UserSchemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_user(
    user_id: int,
    user: UserSchemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchemas.AuthUser = Depends(AuthServices.get_current_user),
):
    db_user = UserServices.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(
        json_data=UserServices.update_user(db, user.dict(exclude_unset=True), user_id),
        message="Records updated Successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.delete(
    "/delete/{user_id}",
    response_model=UserSchemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchemas.AuthUser = Depends(AuthServices.get_current_user),
):
    db_user = UserServices.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(
        json_data=UserServices.delete_user(db, user_id),
        message="Records Deleted Successfully",
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/auth",
    response_model=TokenSchema.TokenResponse,
    status_code=status.HTTP_202_ACCEPTED,
    name="auth",
)
async def login_for_access_token(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    db_user = UserServices.authenticate_user(db, user)
    if not db_user or db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    token: str = await AuthServices.create_access_token(
        user.username, db_user.id, timedelta(minutes=20)
    )

    return Response(
        json_data={"access_token": token, "token_type": "bearer"},
        message="Access Token Created Successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/verify-token",
)
async def verify_token(
    token: Annotated[
        str,
        Depends(AuthServices.oauth2_bearer),
    ]
):
    res = await AuthServices.get_current_user(token=token)
    return res
