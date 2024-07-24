# defining the Pydantic schema models for request/response validation/verification
from pydantic import BaseModel, EmailStr
from datetime import datetime


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

    class Config:
        from_attributes = True


# user models
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
