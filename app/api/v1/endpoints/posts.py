from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.users_model import UserModel
from app.schemas import posts_schemas as PostsSchemas
from services.posts_services import PostServices
from services.auth_services import AuthServices

from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


@router.post(
    "/create",
    response_model=PostsSchemas.PostsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_post(
    post: PostsSchemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    posts = PostServices.create_post(db, post, current_user)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Post Cannot be created"
        )
    return Response(
        json_data=posts,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/", response_model=PostsSchemas.PostsResponse, status_code=status.HTTP_200_OK
)
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
    "/@{username}",
    response_model=PostsSchemas.PostsResponse,
    status_code=status.HTTP_200_OK,
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
