from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_
from typing import List
from app.models.users_model import UserModel
from app.models.posts_model import PostsModel
from .user_services import UserServices


class PostServices:
    @classmethod
    def get_posts(cls, db: Session, limit):

        db_posts = (
            db.query(PostsModel)
            .filter(PostsModel.is_deleted == False)
            .limit(limit)
            .all()
        )
        return db_posts

    @classmethod
    def get_posts_by_username(cls, db: Session, username: str):
        results = (
            db.query(PostsModel, UserModel.username)
            .join(UserModel, PostsModel.user_id == UserModel.id)
            .filter(UserModel.username == username)
            .all()
        )
        return [
            {**post.__dict__, "username": username}  # Unpacking post attributes
            for post, username in results
        ]

    @classmethod
    def create_post(cls, db: Session, post, user: dict):
        db_posts = PostsModel(
            post=post.post,
            user_id=user["id"],
            post_description=post.post_description,
        )
        db.add(db_posts)
        db.commit()
        db.refresh(db_posts)
        result = db_posts.__dict__.copy()
        result["user_username"] = UserServices.get_user(db, result["user_id"]).username
        del result["user_id"]
        return result
