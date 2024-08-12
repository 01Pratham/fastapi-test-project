from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from core.db import Base
from services.auth_services import AuthServices


class UserModel(Base):
    __tablename__ = "tbl_users_master"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    profile_pic = Column(String(255))
    bio = Column(String(255))
    is_private = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    post = relationship("PostsModel", back_populates="user")
    likes = relationship("LikesModel", back_populates="user")
    followings = relationship(
        "FollowingsModel",
        foreign_keys="[FollowingsModel.user_id]",
        back_populates="user",
    )
    followers = relationship(
        "FollowingsModel",
        foreign_keys="[FollowingsModel.following_user_id]",
        back_populates="following_user",
    )
    comments = relationship("CommentsModel", back_populates="user")

    def set_password(self, password: str):
        self.password = AuthServices.hash_password(password.encode("utf-8"))

    def username_to_lower(self, username: str):
        self.username = username.lower()


# Import FollowingsModel here to avoid circular import
from .followings_model import FollowingsModel


@event.listens_for(UserModel, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    if target.password:
        target.set_password(target.password)
    if target.username:
        target.username_to_lower(target.username)


@event.listens_for(UserModel, "before_update")
def hash_password_before_update(mapper, connection, target):
    state = target.__dict__.get("_sa_instance_state")
    if "password" in state.attrs and state.attrs.password.history.has_changes():
        target.set_password(target.password)
    if "username" in state.attrs and state.attrs.password.history.has_changes():
        target.username_to_lower(target.username)
