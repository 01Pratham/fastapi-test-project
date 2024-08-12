from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_
from typing import List
from app.models.users_model import UserModel
from app.models.followings_model import FollowingsModel
from .user_services import UserServices


class FollowingServices:
    @classmethod
    def get_data(
        cls,
        db: Session,
        user_id: int,
        Followings: bool = False,
        Followers: bool = False,
    ):
        if Followings:
            db_users = (
                db.query(
                    UserModel.id,
                    UserModel.name,
                    UserModel.username,
                    UserModel.profile_pic,
                    FollowingsModel.following_user_id,
                    FollowingsModel.updated_date,
                )
                .join(
                    FollowingsModel, UserModel.id == FollowingsModel.following_user_id
                )
                .filter(
                    FollowingsModel.user_id == user_id,
                    UserModel.is_deleted == False,
                )
                .all()
            )
        elif Followers:
            db_users = (
                db.query(
                    UserModel.id,
                    UserModel.name,
                    UserModel.username,
                    UserModel.profile_pic,
                    FollowingsModel.user_id,
                    FollowingsModel.updated_date,
                )
                .join(FollowingsModel, UserModel.id == FollowingsModel.user_id)
                .filter(
                    and_(
                        FollowingsModel.following_user_id == user_id,
                        UserModel.is_deleted == False,
                    )
                )
                .all()
            )
        else:
            return None

        followers = [
            {
                **user._asdict(),
            }
            for user in db_users
        ]

        return {"user_id": user_id, "users": followers}

    @classmethod
    def create_follower(cls, db: Session, user: int, followed_user: int):
        data = (
            db.query(FollowingsModel)
            .filter(
                and_(
                    FollowingsModel.user_id == user,
                    FollowingsModel.following_user_id == followed_user,
                )
            )
            .first()
        )
        if data:
            return data
        db_followers = FollowingsModel(
            user_id=user,
            following_user_id=followed_user,
        )
        db.add(db_followers)
        db.commit()
        db.refresh(db_followers)
        return db_followers

    @classmethod
    def remove_follower(cls, db: Session, user: int, followed_user: int):
        db_followers = (
            db.query(FollowingsModel)
            .filter(
                and_(
                    FollowingsModel.user_id == user,
                    FollowingsModel.following_user_id == followed_user,
                )
            )
            .first()
        )
        db.delete(db_followers)
        return True
