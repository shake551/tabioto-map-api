from typing import Optional, List

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: Optional[str]


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: int
