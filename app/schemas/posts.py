from pydantic import BaseModel, validator
from typing import List, Optional, Union
from utils.helpers import Helpers
from .DefaultResponse import DefaultResponse
from datetime import datetime


class PostBase(BaseModel):

    id: int
    post: str
    post_description: Optional[str] = None

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class ResponseBase(PostBase):
    user_username: int
    likes_count: Optional[int] = 0
    likers: Optional[list] = []
    comments: Optional[list] = []
    created_date: Optional[datetime] = None


class PostsResponse(DefaultResponse):
    data: Union[ResponseBase, List[ResponseBase]]
