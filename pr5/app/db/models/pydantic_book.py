from pydantic import BaseModel, ConfigDict


class PydanticBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    author: str
