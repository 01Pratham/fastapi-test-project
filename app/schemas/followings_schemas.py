from pydantic import BaseModel
from typing import List, Optional, Union
from utils.helpers import Helpers
from .DefaultResponse_schemas import DefaultResponse
from datetime import datetime


class FollowingsBase(BaseModel):
    following_user_id: int


class Follows(BaseModel):
    id: int
    username: str
    name: str
    profile_pic: str
    updated_date: datetime


class ResponseBase(BaseModel):
    users: Optional[List[Follows]] = []


class FollowingsResponse(DefaultResponse):
    data: Union[ResponseBase, List[ResponseBase]]
