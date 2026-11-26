from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    post_id: int
    author_id: int
    created_at: datetime
