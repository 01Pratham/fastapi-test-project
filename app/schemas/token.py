from pydantic import BaseModel
from .DefaultResponse import DefaultResponse
from typing import Union, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenResponse(DefaultResponse):
    data: Union[Token, List[Token]]
