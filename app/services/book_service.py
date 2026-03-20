from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import book_repository


async def list_books(
    db: AsyncSession,
    status: str | None = None,
    author: str | None = None,
    sort_by: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    return await book_repository.get_all_books(
        db=db,
        status=status,
        author=author,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
    )


async def get_book(db: AsyncSession, book_id: str):
    return await book_repository.get_book_by_id(db, book_id)


async def create_book(db: AsyncSession, book_data: dict):
    return await book_repository.add_book(db, book_data)


async def remove_book(db: AsyncSession, book_id: str):
    await book_repository.delete_book(db, book_id)