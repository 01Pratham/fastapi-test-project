from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_


from app.models.users import UserModel
from schemas import user as UserSchemas
from .auth_services import bcrypt_context, oauth2_bearer


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_users(db: Session, limit: int, deleted: bool):
    if deleted:
        db_users = db.query(UserModel).limit(limit).all()
    else:
        db_users = (
            db.query(UserModel)
            .filter(UserModel.is_deleted == False)
            .limit(limit)
            .all()
        )
    return db_users


def create_user(db: Session, user: UserSchemas.UserCreate):
    user_dict = dict(user)
    db_user = UserModel(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserSchemas.UserUpdate, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    for key, value in user.items():
        if key == "id":
            continue
        setattr(db_user, key, value)
    db_user.updated_date = func.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db_user.is_deleted = True
    db_user.updated_date = func.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.username == user.username)
        .first()
    )

    if not db_user:
        return False
    if (
        not bcrypt_context.verify(
            user.password.encode("utf-8"), db_user.password.encode("utf-8")
        )
        or db_user.is_deleted
        or not db_user.is_active
    ):
        return False

    return db_user
