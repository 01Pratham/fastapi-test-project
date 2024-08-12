from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from app.models.users_model import UserModel
from app.models.posts_model import PostsModel
from app.models.comments_model import CommentsModel
from app.models.likes_model import LikesModel
from .user_services import UserServices


class PostServices:
    @classmethod
    def get_likes_count_subquery(cls, db: Session):
        """Creates a subquery to count likes for each post."""
        return (
            db.query(LikesModel.post_id, func.count(LikesModel.id).label("likes_count"))
            .filter(LikesModel.is_user_deleted == False)
            .group_by(LikesModel.post_id)
            .subquery()
        )

    @classmethod
    def get_comments_count_subquery(cls, db: Session):
        """Creates a subquery to count comments for each post."""
        return (
            db.query(
                CommentsModel.post_id,
                func.count(CommentsModel.id).label("comments_count"),
            )
            .filter(CommentsModel.is_user_deleted == False)
            .group_by(CommentsModel.post_id)
            .subquery()
        )

    @classmethod
    def get_posts(cls, db: Session, limit: int):
        likes_count_subquery = cls.get_likes_count_subquery(db)
        comments_count_subquery = cls.get_comments_count_subquery(db)

        db_posts = (
            db.query(
                PostsModel.id,
                PostsModel.post,
                PostsModel.post_description,
                PostsModel.created_date,
                UserModel.username,
                UserModel.name,
                UserModel.profile_pic,
                func.coalesce(likes_count_subquery.c.likes_count, 0).label(
                    "likes_count"
                ),
                func.coalesce(comments_count_subquery.c.comments_count, 0).label(
                    "comments_count"
                ),
            )
            .join(UserModel, PostsModel.user_id == UserModel.id)
            .outerjoin(
                likes_count_subquery, PostsModel.id == likes_count_subquery.c.post_id
            )
            .outerjoin(
                comments_count_subquery,
                PostsModel.id == comments_count_subquery.c.post_id,
            )
            .filter(PostsModel.is_deleted == False)
            .group_by(
                PostsModel.id,
                PostsModel.post,
                PostsModel.post_description,
                PostsModel.created_date,
                UserModel.username,
                UserModel.name,
                UserModel.profile_pic,
                likes_count_subquery.c.likes_count,
                comments_count_subquery.c.comments_count,
            )
            .limit(limit)
            .all()
        )

        return [post._asdict() for post in db_posts]

    @classmethod
    def get_posts_by_username(cls, db: Session, username: str) -> List[dict]:
        likes_count_subquery = cls.get_likes_count_subquery(db)
        comments_count_subquery = cls.get_comments_count_subquery(db)

        results = (
            db.query(
                PostsModel.id,
                PostsModel.post,
                PostsModel.post_description,
                PostsModel.created_date,
                UserModel.username,
                UserModel.name,
                UserModel.profile_pic,
                func.coalesce(likes_count_subquery.c.likes_count, 0).label(
                    "likes_count"
                ),
                func.coalesce(comments_count_subquery.c.comments_count, 0).label(
                    "comments_count"
                ),
            )
            .join(UserModel, PostsModel.user_id == UserModel.id)
            .outerjoin(
                likes_count_subquery, PostsModel.id == likes_count_subquery.c.post_id
            )
            .outerjoin(
                comments_count_subquery,
                PostsModel.id == comments_count_subquery.c.post_id,
            )
            .filter(UserModel.username == username, PostsModel.is_deleted == False)
            .group_by(
                PostsModel.id,
                PostsModel.post,
                PostsModel.post_description,
                PostsModel.created_date,
                UserModel.username,
                UserModel.name,
                UserModel.profile_pic,
                likes_count_subquery.c.likes_count,
                comments_count_subquery.c.comments_count,
            )
            .all()
        )

        return [post._asdict() for post in results]

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
