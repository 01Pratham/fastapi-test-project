from pydantic import BaseModel
from typing import List, Optional, Union
from utils.helpers import Helpers
from .DefaultResponse_schemas import DefaultResponse
from datetime import datetime


class CommentsBase(BaseModel):
    post_id: int

    class Config:
        orm_mode = True


class Commentors(BaseModel):
    comment_desciption: str
    commentor_user_id: int
    username: str
    name: str
    updated_date: datetime
    profile_pic: Optional[str] = None


class ResponseBase(CommentsBase):
    commentors: Optional[List[Commentors]] = None


class CommentsResponse(DefaultResponse):
    data: Union[ResponseBase, List[ResponseBase]]
