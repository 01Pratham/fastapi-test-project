from pydantic import BaseModel, validator
from typing import List, Optional, Union
from utils.helpers import Helpers
from .DefaultResponse_schemas import DefaultResponse
from datetime import datetime


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    profile_pic: Optional[str] = None
    bio: Optional[str] = None
    is_private: Optional[bool] = False

    class Config:
        orm_mode = True


class ResponseBase(UserBase):
    id: Optional[int] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None


class UserResponse(DefaultResponse):
    data: Union[ResponseBase, List[ResponseBase]]


class UserCreate(UserBase):
    password: str

    @validator("name", "email", "password", "username", pre=True, always=True)
    def validate_not_empty_fields(cls, v):
        return Helpers.validate_not_empty(v)

    @validator("email", pre=True, always=True)
    def validate_email_field(cls, v):
        return Helpers.validate_email(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return Helpers.validate_password(v)


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @validator("name", "email", "password", "username", pre=True, always=True)
    def validate_not_empty_fields(cls, v):
        return Helpers.validate_not_empty(v)

    @validator("email", pre=True, always=True)
    def validate_email_field(cls, v):
        return Helpers.validate_email(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return Helpers.validate_password(v)


class AuthUser(BaseModel):
    username: str
    password: str

    @validator("password", "username", pre=True, always=True)
    def validate_not_empty_fields(cls, v):
        return Helpers.validate_not_empty(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return Helpers.validate_password(v)
