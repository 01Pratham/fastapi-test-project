from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base
from .posts_model import PostsModel
from .users_model import UserModel


class CommentsModel(Base):
    __tablename__ = "tbl_comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("tbl_posts_details.id"), nullable=False)
    commentor_user_id = Column(
        Integer, ForeignKey("tbl_users_master.id"), nullable=False
    )
    comment_desciption = Column(String(255))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_commenter_user_deleted = Column(Boolean, default=False)

    user = relationship("UserModel", back_populates="comments")
    post = relationship("PostsModel", back_populates="comments")
