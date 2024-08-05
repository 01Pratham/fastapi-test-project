from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_

from models import users as UserModel, posts as PostModel


def get_posts(db: Session, limit):

    db_posts = (
        db.query(PostModel.Posts)
        .filter(PostModel.Posts.is_deleted == False)
        .limit(limit)
        .all()
    )
    return db_posts


def get_posts_by_username(db: Session, username: str):
    db_posts = (
        db.query(PostModel.Posts, UserModel.User)
        .filter(
            UserModel.User.username == username,
            PostModel.Posts.user_id == UserModel.User.id,
        )
        .all()
    )
    return db_posts


def create_post(db: Session, post):
    pass
