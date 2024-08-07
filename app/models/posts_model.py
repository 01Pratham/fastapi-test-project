from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base
from services.auth_services import AuthServices
from .users_model import UserModel


class PostsModel(Base):
    __tablename__ = "tbl_posts_details"
    id = Column(Integer, primary_key=True, index=True)
    post = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("tbl_users_master.id"), nullable=False)
    post_description = Column(String(255))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
    is_user_deleted = Column(Boolean, default=False)
    # __table_args__ = {"extend_existing": True}  # Add this line

    user = relationship("UserModel", back_populates="post")
