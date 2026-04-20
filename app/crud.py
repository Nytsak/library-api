from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate


def create_book(db: Session, book: BookCreate):
    db_book = Book(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_id(db: Session, book_id: int):
    stmt = select(Book).where(Book.id == book_id)
    return db.execute(stmt).scalar_one_or_none()


def get_books_cursor(db: Session, limit: int = 10, cursor: int | None = None):
    stmt = select(Book).order_by(Book.id.asc())

    if cursor is not None:
        stmt = stmt.where(Book.id > cursor)

    stmt = stmt.limit(limit + 1)

    books = db.execute(stmt).scalars().all()

    has_next = len(books) > limit
    items = books[:limit]

    next_cursor = items[-1].id if has_next and items else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_next": has_next,
    }