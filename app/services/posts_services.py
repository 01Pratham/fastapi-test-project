from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_

from models.users import UserModel
from models.posts import PostsModel


def get_posts(db: Session, limit):

    db_posts = (
        db.query(PostsModel).filter(PostsModel.is_deleted == False).limit(limit).all()
    )
    return db_posts


def get_posts_by_username(db: Session, username: str):
    db_posts = (
        db.query(PostsModel, UserModel)
        .filter(
            UserModel.username == username,
            PostsModel.user_id == UserModel.id,
        )
        .all()
    )
    return db_posts


def create_post(db: Session, post, current_user):
    return {"POST": post, "current_user": current_user}
