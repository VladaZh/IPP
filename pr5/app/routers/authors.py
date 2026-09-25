from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.book_crud import get_all_authors
from app.db.session import get_db

router = APIRouter(tags=["authors"])


@router.get("/authors", response_model=list[str])
def get_authors(db: Session = Depends(get_db)):
    authors = get_all_authors(db)
    return authors
