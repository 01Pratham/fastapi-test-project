from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.users_model import UserModel
from app.schemas import likes_schemas as LikesSchemas
from services.likes_services import LikesServices
from services.auth_services import AuthServices

from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


@router.post(
    "/add",
    response_model=LikesSchemas.LikesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_likes_to_post(
    obj: LikesSchemas.LikesBase,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    posts = LikesServices.add_like(
        db=db,
        obj={
            "post_id": obj.post_id,
            "user_id": current_user["id"],
        },
    )
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
    "/{post_id}",
    response_model=LikesSchemas.LikesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_likers(
    post_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    users = LikesServices.get_likers(db=db, post_id=post_id, limit=limit)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )
