from uuid import uuid4, UUID
from typing import List, Optional
from app.models.book_model import books_db

async def get_all_books():
    return books_db

async def get_book_by_id(book_id: UUID):
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None

async def add_book(book_data: dict):
    book_data["id"] = uuid4()
    books_db.append(book_data)
    return book_data

async def delete_book(book_id: UUID):
    global books_db
    initial_len = len(books_db)
    books_db[:] = [b for b in books_db if b["id"] != book_id]
    return len(books_db) != initial_len  # True якщо видалили