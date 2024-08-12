from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_
from typing import List
from app.models.users_model import UserModel
from app.models.posts_model import PostsModel
from app.models.likes_model import LikesModel
from .user_services import UserServices


class LikesServices:
    @classmethod
    def get_likers(cls, db: Session, post_id, limit):

        db_likes = (
            db.query(
                UserModel.username,
                UserModel.profile_pic,
                UserModel.name,
                LikesModel.user_id,
                LikesModel.updated_date,
            )
            .join(UserModel, UserModel.id == LikesModel.user_id)
            .filter(LikesModel.post_id == post_id)
            .limit(limit=limit)
            .all()
        )

        likers = [
            {
                **like._asdict(),
                "username": like.username,
                "name": like.name,
                "user_id": like.user_id,
                "profile_pic": like.profile_pic,
            }
            for like in db_likes
        ]

        return {"post_id": post_id, "likers": likers}

    @classmethod
    def add_like(cls, db: Session, obj):
        is_liked = (
            db.query(LikesModel)
            .filter(
                and_(
                    LikesModel.post_id == obj["post_id"],
                    LikesModel.user_id == obj["user_id"],
                )
            )
            .first()
        )
        if is_liked:
            return is_liked
        db_likes = LikesModel(post_id=obj["post_id"], user_id=obj["user_id"])
        db.add(db_likes)
        db.commit()
        db.refresh(db_likes)
        return db_likes
