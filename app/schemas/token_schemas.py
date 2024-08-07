from pydantic import BaseModel
from .DefaultResponse_schemas import DefaultResponse
from typing import Union, List


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str | None = None


class TokenResponse(DefaultResponse):
    data: Union[Token, List[Token]]
