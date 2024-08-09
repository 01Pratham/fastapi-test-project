from pydantic import BaseModel
from typing import List, Optional, Union
from utils.helpers import Helpers
from .DefaultResponse_schemas import DefaultResponse
from datetime import datetime


class LikesBase(BaseModel):

    post_id: int
    is_deleted: Optional[bool] = False

    class Config:
        orm_mode = True


class Likers(BaseModel):
    user_id: int
    username: str
    name: str
    updated_date: datetime
    profile_pic: Optional[str] = None


class ResponseBase(LikesBase):
    likers: Optional[List[Likers]] = None


class LikesResponse(DefaultResponse):
    data: Union[ResponseBase, List[ResponseBase]]
