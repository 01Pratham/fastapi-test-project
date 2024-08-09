from fastapi import APIRouter, Depends, HTTPException, Header
from starlette import status
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from services.auth_services import AuthServices
from services.followings_services import FollowingServices
from app.schemas import followings_schemas as FollowingsSchema


from app.utils.response import Response
from core.db import SessionLocal, engine, get_db


router = APIRouter()


@router.get(
    "/followers/{user_id}",
    response_model=FollowingsSchema.FollowingsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_followers(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    followers = FollowingServices.get_data(db, user_id, Followers=True)
    if not followers:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No Followers Found"
        )
    return Response(
        message="Followed User",
        json_data=followers,
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/followings/{user_id}",
    response_model=FollowingsSchema.FollowingsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_followings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    followers = FollowingServices.get_data(db, user_id, Followings=True)
    if not followers:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No Followings Found"
        )
    return Response(
        message="Followings User",
        json_data=followers,
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/add",
    response_model=FollowingsSchema.FollowingsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_follower(
    obj: FollowingsSchema.FollowingsBase,
    db: Session = Depends(get_db),
    current_user: Annotated[
        Optional[dict], Depends(AuthServices.get_current_user)
    ] = None,
):
    followed_data = FollowingServices.create_follower(
        db=db, user=current_user.get("id"), followed_user=obj.following_user_id
    )
    if not followed_data:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Post Cannot be created"
        )
    return Response(
        json_data=followed_data,
        message="Followed User",
        status_code=status.HTTP_200_OK,
    )


# @router.post(
#     "/add",
#     response_model=FollowingsSchema.FollowingsResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def add_follower(
#     obj: FollowingsSchema.FollowingsBase,
#     db: Session = Depends(get_db),
#     current_user: Annotated[
#         Optional[dict], Depends(AuthServices.get_current_user)
#     ] = None,
# ):
#     followed_data = FollowingServices.remove_follower(
#         db=db, user=current_user.get("id"), followed_user=obj.following_user_id
#     )
#     if not followed_data:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Post Cannot be created"
#         )

#     print(followed_data)
#     return Response(
#         json_data=followed_data,
#         message="Unfollowed user",
#         status_code=status.HTTP_200_OK,
#     )
