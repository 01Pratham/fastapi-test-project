from pydantic import BaseModel, validator
from typing import List, Optional, Any, Union

from schemas.DefaultResponse import DefaultResponse


class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ResBase(UserBase):
    id: Optional[int] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None


class UserResponse(DefaultResponse):
    data: Union[ResBase, List[ResBase]]


class UserCreate(UserBase):
    password: str

    @validator("name", "email", "password", pre=True, always=True)
    def validate_not_empty(cls, v):
        v = " ".join(v.split())
        if not v:
            raise ValueError("All fields should be filled with keywords")
        return v


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @validator("name", "email", "password", pre=True, always=True)
    def validate_not_empty(cls, v):
        if v is None:
            return v
        v = " ".join(v.split())
        if not v:
            raise ValueError("All fields should be filled with keywords")
        return v
