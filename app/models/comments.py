from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base
from services.auth_services import bcrypt_context, oauth2_bearer


class Posts(Base):
    __tablename__ = "tbl_likes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("tbl_posts_details.id"), nullable=False)
    commenter_user_id = Column(
        Integer, ForeignKey("tbl_users_master.id"), nullable=False
    )
    comment_desciption = Column(String(255))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_commenter_user_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_details")
    posts = relationship("Posts", back_populates="tbl_posts_details")

    __table_args__ = {"extend_existing": True}
