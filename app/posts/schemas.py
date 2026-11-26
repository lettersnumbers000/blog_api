from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
