from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True


class BookCursorPage(BaseModel):
    items: list[BookResponse]
    next_cursor: Optional[int] = None
    has_next: bool