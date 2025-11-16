from pydantic import BaseModel
from typing import Optional

class CreateBookRequest(BaseModel):
    title: str
    author: str
    publisher: str
    publication_year: int
    gender: str
    quantity_copies: int
    available: bool

class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    gender: Optional[str] = None
    quantity_copies: Optional[int] = None
    available: Optional[bool] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publication_year: int
    gender: str
    quantity_copies: int
    available: bool

class ListBooksResponse(BaseModel):
    books: list[BookResponse]
    totalCount: int
    limit: int
    offset: int        