from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from core.db import Base
from services.auth_services import bcrypt_context, oauth2_bearer


class User(Base):
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

    def set_password(self, password: str):
        self.password = bcrypt_context.hash(password.encode("utf-8"))


@event.listens_for(User, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    if target.password:
        target.set_password(target.password)


@event.listens_for(User, "before_update")
def hash_password_before_update(mapper, connection, target):
    state = target.__dict__.get("_sa_instance_state")
    if "password" in state.attrs and state.attrs.password.history.has_changes():
        target.set_password(target.password)
