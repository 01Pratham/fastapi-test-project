from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, event, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import bcrypt

from core.db import Base


class User(Base):
    __tablename__ = "tbl_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


@event.listens_for(User, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    if target.password:
        target.set_password(target.password)


@event.listens_for(User, "before_update")
def hash_password_before_update(mapper, connection, target):
    state = target.__dict__.get("_sa_instance_state")
    if "password" in state.attrs and state.attrs.password.history.has_changes():
        target.set_password(target.password)
