from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.db import Base
from .users_model import UserModel
from .posts_model import PostsModel


class LikesModel(Base):
    __tablename__ = "tbl_likes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("tbl_posts_details.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("tbl_users_master.id"), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_user_deleted = Column(Boolean, default=False)

    __table_args__ = {"extend_existing": True}  # Add this line
    user = relationship("UserModel", back_populates="likes")
    post = relationship("PostsModel", back_populates="likes")
