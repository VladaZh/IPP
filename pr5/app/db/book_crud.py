from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.orm_book import Book
from app.db.models.book_create import BookCreate


def create_book(book_data: BookCreate, db: Session) -> Book:
    book = Book(name=book_data.name, author=book_data.author)

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_book_by_id(book_id: int, db: Session) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result = db.execute(stmt)
    book = result.scalar_one_or_none()
    return book


def get_book_by_name(book_name: str, db: Session) -> Book | None:
    stmt = select(Book).where(Book.name == book_name)
    result = db.execute(stmt)
    book = result.scalar_one_or_none()
    return book


def get_books(db: Session) -> list[Book]:
    stmt = select(Book)
    result = db.execute(stmt)
    books = result.scalars().all()
    return list(books)


def update_book(
    db: Session, id: int, name: str | None = None, author: str | None = None
) -> Book | None:
    book = get_book_by_id(id, db)
    if book is None:
        return None

    if name is not None:
        book.name = name

    if author is not None:
        book.author = author

    db.commit()
    db.refresh(book)

    return book


def delete_book(db: Session, id: int) -> bool:
    book = get_book_by_id(id, db)
    if book is None:
        return False
    db.delete(book)
    db.commit()
    return True


def get_all_authors(db: Session) -> list[str]:
    stmt = select(Book.author).distinct().order_by(Book.author)

    result = db.execute(stmt)
    authors = result.scalars().all()
    return list(authors)


def get_books_by_author(db: Session, author: str) -> list[Book]:
    stmt = select(Book).where(Book.author == author)
    result = db.execute(stmt)
    books = result.scalars().all()
    return list(books)
