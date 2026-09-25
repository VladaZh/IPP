from typing import Optional

from pydantic import BaseModel


class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
