from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.users_model import UserModel
from app.schemas import comments_schemas as CommentsSchemas
from app.schemas.user_schemas import AuthUser as AuthSchema
from services.comments_services import CommentsServices
from services.auth_services import AuthServices


from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


@router.post(
    "/add",
    response_model=CommentsSchemas.CommentsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_comments_to_post(
    obj: CommentsSchemas.CommentsBase,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    posts = CommentsServices.add_comment(
        db=db,
        obj={
            **obj.__dict__,
            "user_id": current_user["id"],
        },
    )
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Comment Cannot be created",
        )
    return Response(
        json_data=posts,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/{post_id}",
    response_model=CommentsSchemas.CommentsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_commentors(
    post_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    users = CommentsServices.get_commentors(db=db, post_id=post_id, limit=limit)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=status.HTTP_200_OK,
    )
