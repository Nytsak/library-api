from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from typing import Optional

class BookStatus(str, Enum):
    available = "available"
    issued = "issued"

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: int = Field(..., ge=0)
    status: BookStatus = BookStatus.available

class BookResponse(BookCreate):
    id: UUID