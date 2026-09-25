from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, index=True)
