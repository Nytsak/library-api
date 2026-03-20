from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional


class BookStatus(str, Enum):
    available = "available"
    issued = "issued"


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: BookStatus = BookStatus.available
    year: int = Field(..., ge=0)


class BookResponse(BookCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)