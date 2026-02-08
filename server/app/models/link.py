from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LinkCreate(BaseModel):
    url: str


class LinkResponse(BaseModel):
    id: str
    url: str
    title: str
    thumbnail: Optional[str] = None
    summary: str
    tags: list[str]
    category: Optional[str] = None
    user_id: str
    created_at: datetime


class LinkListResponse(BaseModel):
    links: list[LinkResponse]
    total: int
