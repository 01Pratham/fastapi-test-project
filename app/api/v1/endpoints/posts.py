from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import users as UserModel
from schemas.posts import PostCreate, PostsResponse
from services import posts_services as PostServices
from services import auth_services as AuthServices

from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


@router.get("/", response_model=PostsResponse, status_code=status.HTTP_200_OK)
async def get_posts(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    users = PostServices.get_posts(db=db, limit=limit)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/@{username}", response_model=PostsResponse, status_code=status.HTTP_200_OK
)
async def get_posts_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    users = PostServices.get_posts_by_username(db=db, username=username)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )
