from pydantic import BaseModel, validator
from typing import List, Optional, Union
import re
from .DefaultResponse import DefaultResponse
from datetime import datetime


def validate_not_empty(v):
    if v is None:
        return v
    v = " ".join(v.split())
    if not v:
        raise ValueError("All fields should be filled with keywords")
    return v


def validate_email(v):
    if v is None:
        return v

    if "@" not in v:
        raise ValueError("Email must contain '@'")
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    if not re.match(email_regex, v):
        raise ValueError("Email must contain a valid domain (e.g., '.com', '.net')")

    return v


def validate_password(v: str) -> str:
    if v is None:
        return v
    has_digit = re.search(r"\d", v)
    has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', v)
    if not (has_digit and has_special_char):
        raise ValueError(
            "Password must contain at least one number and one special character."
        )
    return v


class UserBase(BaseModel):
    name: str
    email: str

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

    @validator("name", "email", "password", pre=True, always=True)
    def validate_not_empty_fields(cls, v):
        return validate_not_empty(v)

    @validator("email", pre=True, always=True)
    def validate_email_field(cls, v):
        return validate_email(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return validate_password(v)


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @validator("name", "email", "password", pre=True, always=True)
    def validate_not_empty_fields(cls, v):
        return validate_not_empty(v)

    @validator("email", pre=True, always=True)
    def validate_email_field(cls, v):
        return validate_email(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return validate_password(v)


class AuthUser(BaseModel):
    email: str
    password: str

    @validator("email", pre=True, always=True)
    def validate_email_field(cls, v):
        return validate_email(v)

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, v):
        return validate_password(v)
