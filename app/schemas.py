# defining the Pydantic schema models for request/response validation/verification
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# user models
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    # email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# response models
class Post(PostBase):
    # extends PostBase defined above
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


# login token models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# vote models
class Vote(BaseModel):
    post_id: int
    direction: bool
