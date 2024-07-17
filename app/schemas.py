# defining the Pydantic schema models for request/response validation/verification
from pydantic import BaseModel
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
