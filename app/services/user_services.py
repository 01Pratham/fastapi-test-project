from sqlalchemy.orm import Session

from models import user as UserModel
from schemas import user as UserSchemas


def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def get_users(db: Session, limit: int = 100):
    return db.query(UserModel.User).limit(limit).all()


def create_user(db: Session, user: UserSchemas.UserCreate):
    db_user = UserModel.User(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserSchemas.UserUpdate, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.User.id == user_id).first()
    for key in user.keys():
        if key in db_user.keys():
            db_user[key] = user[key]

    db.commit()
    db.refresh()
    return db_user
