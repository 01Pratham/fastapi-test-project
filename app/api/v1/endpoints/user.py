from fastapi import APIRouter, Depends, HTTPException

from models import user as UserModel
from schemas import user as UserSchemas
from services import user_services as UserServices
from services.response import Response

from typing import List
from sqlalchemy.orm import Session
from core.db import SessionLocal, engine, get_db

router = APIRouter()


# @router.post("/")
@router.post("/", response_model=UserSchemas.UserResponse)
async def post_user(user: UserSchemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserServices.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return Response(
        json_data=UserServices.create_user(db=db, user=user),
        message="Records Inserted Successfully",
        status_code=200,
    )


@router.get("/", response_model=List[UserSchemas.UserResponse])
async def get_users(limit: int = 100, db: Session = Depends(get_db)):
    users = UserServices.get_users(db=db, limit=limit)
    return Response(
        json_data=users,
        message="Data for all Users",
        status_code=200,
    )


@router.get("/id/{user_id}/", response_model=UserSchemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserServices.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(
        json_data=db_user,
        message=f"Data for user {user_id}",
        status_code=200,
    )


@router.put("/update/{user_id}")
async def update_user(
    user_id: int, user: UserSchemas.UserUpdate, db: Session = Depends(get_db)
):
    db_user = UserServices.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(
        json_data=UserServices.update_user(db, db_user, user_id),
        message="Records updated Successfully",
        status_code=200,
    )
