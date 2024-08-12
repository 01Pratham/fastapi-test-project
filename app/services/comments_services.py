from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_
from typing import List
from app.models.users_model import UserModel
from app.models.posts_model import PostsModel
from app.models.comments_model import CommentsModel
from .user_services import UserServices


class CommentsServices:
    @classmethod
    def get_commentors(cls, db: Session, post_id, limit):

        db_comments = (
            db.query(
                UserModel.username,
                UserModel.profile_pic,
                UserModel.name,
                CommentsModel.commentor_user_id,
                CommentsModel.comment_desciption,
                CommentsModel.updated_date,
            )
            .join(UserModel, UserModel.id == CommentsModel.commentor_user_id)
            .filter(CommentsModel.post_id == post_id)
            .limit(limit=limit)
            .all()
        )

        commentors = [
            {
                **comment._asdict(),
                # "username": comment.username,
                # "name": comment.name,
                # "user_id": comment.user_id,
                # "profile_pic": comment.profile_pic,
            }
            for comment in db_comments
        ]

        return {"post_id": post_id, "commentors": commentors}

    @classmethod
    def add_comment(cls, db: Session, obj):
        db_comments = CommentsModel(
            post_id=obj["post_id"],
            commentor_user_id=obj["user_id"],
            comment_desciption=obj["comment_desciption"],
        )
        db.add(db_comments)
        db.commit()
        db.refresh(db_comments)
        return db_comments
