from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@router.get("/", response_model=schemas.BookCursorPage)
def read_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_books_cursor(db=db, limit=limit, cursor=cursor)


@router.get("/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book