from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.db import Base
from .users_model import UserModel


class FollowingsModel(Base):
    __tablename__ = "tbl_followings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_users_master.id"), nullable=False)
    following_user_id = Column(
        Integer, ForeignKey("tbl_users_master.id"), nullable=False
    )
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_following_user_deleted = Column(Boolean, default=False)
    is_follower_user_deleted = Column(Boolean, default=False)

    user = relationship(
        "UserModel", foreign_keys=[user_id], back_populates="followings"
    )
    following_user = relationship(
        "UserModel", foreign_keys=[following_user_id], back_populates="followers"
    )
