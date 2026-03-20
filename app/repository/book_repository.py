from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book_model import Book


async def get_all_books(
    db: AsyncSession,
    status: str | None = None,
    author: str | None = None,
    sort_by: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = select(Book)

    if status:
        query = query.where(Book.status == status)

    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))

    if sort_by == "title":
        query = query.order_by(Book.title)
    elif sort_by == "year":
        query = query.order_by(Book.year)
    else:
        query = query.order_by(Book.id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: str):
    result = await db.execute(
        select(Book).where(Book.id == book_id)
    )
    return result.scalar_one_or_none()


async def add_book(db: AsyncSession, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: str):
    book = await get_book_by_id(db, book_id)
    if book:
        await db.delete(book)
        await db.commit()