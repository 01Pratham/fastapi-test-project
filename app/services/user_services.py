from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_


from app.models.users_model import UserModel
from app.schemas import user_schemas as UserSchemas
from .auth_services import AuthServices


class UserServices:
    @classmethod
    def get_user(cls, db: Session, user_id: int):
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @classmethod
    def get_user_by_username(cls, db: Session, username: str):
        return db.query(UserModel).filter(UserModel.username == username).first()

    @classmethod
    def get_users(cls, db: Session, limit: int, deleted: bool):
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

    @classmethod
    def create_user(cls, db: Session, user: UserSchemas.UserCreate):
        user_dict = dict(user)
        db_user = UserModel(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def update_user(cls, db: Session, user: UserSchemas.UserUpdate, user_id: int):
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        for key, value in user.items():
            if key == "id":
                continue
            setattr(db_user, key, value)
        db_user.updated_date = func.now()
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def delete_user(cls, db: Session, user_id: int):
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        db_user.is_deleted = True
        db_user.updated_date = func.now()
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def authenticate_user(cls, db: Session, user):
        db_user = (
            db.query(UserModel).filter(UserModel.username == user.username).first()
        )
        if (
            not db_user
            or not AuthServices.verify_password(
                plain_password=user.password.encode("utf-8"),
                hashed_password=db_user.password.encode("utf-8"),
            )
            or db_user.is_deleted
            or not db_user.is_active
        ):
            return False

        return db_user
