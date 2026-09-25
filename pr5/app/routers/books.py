from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.book_crud import (
    get_books,
    get_book_by_id,
    get_books_by_author,
    create_book,
    update_book,
    delete_book,
)
from app.db.models.book_update import BookUpdate
from app.db.models.orm_book import Book
from app.db.models.pydantic_book import PydanticBook
from app.db.session import get_db
from app.db.models.book_create import BookCreate

router = APIRouter(tags=["books"])


@router.get("/books", response_model=list[PydanticBook])
def get_all_books(db: Session = Depends(get_db)):
    books = get_books(db)
    return books


@router.get("/books/{book_id}", response_model=PydanticBook)
def getting_book_by_id(book_id: int, db: Session = Depends(get_db)) -> Book | None:
    book = get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books/by-author/{temp_author}", response_model=list[PydanticBook])
def getting_books_by_author(temp_author: str, db: Session = Depends(get_db)):
    books = get_books_by_author(db=db, author=temp_author)
    return books


@router.post("/books", response_model=PydanticBook, status_code=201)
def creating_book(book_data: BookCreate, db: Session = Depends(get_db)):
    book = BookCreate(name=book_data.name, author=book_data.author)
    result = create_book(db=db, book_data=book)
    return result


@router.put("/books/{book_id}", response_model=PydanticBook)
def put_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    result = update_book(db, book_id, book.name, book.author)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@router.patch("/books/{book_id}", response_model=PydanticBook)
def patch_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    result = update_book(db, book_id, book.name, book.author)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@router.delete("/books/{book_id}")
def deleting_book(book_id: int, db: Session = Depends(get_db)):
    delete_book(db, book_id)
    return {"message": f"Книга с ID {book_id} успешно удалена"}
