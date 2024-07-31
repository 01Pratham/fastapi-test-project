from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_

from models import user as UserModel
from schemas import user as UserSchemas

import bcrypt


def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def get_users(db: Session, limit: int, deleted: bool):
    if deleted:
        db_users = db.query(UserModel.User).limit(limit).all()
    else:
        db_users = (
            db.query(UserModel.User)
            .filter(UserModel.User.is_deleted == False)
            .limit(limit)
            .all()
        )
    return db_users


def create_user(db: Session, user: UserSchemas.UserCreate):
    db_user = UserModel.User(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserSchemas.UserUpdate, user_id: int):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    for key, value in user.items():
        if key == "id":
            continue
        setattr(db_user, key, value)
    db_user.updated_date = func.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    db_user.is_deleted = True
    db_user.updated_date = func.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user):
    # Retrieve the user by email
    db_user =  db.query(UserModel.User).filter(UserModel.User.email == user.email).first()
    

    if not db_user:
        return None
    if not bcrypt.checkpw(
        user.password.encode("utf-8"), db_user.password.encode("utf-8")
    ):
        return None

    return db_user
