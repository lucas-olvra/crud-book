from pydantic import BaseModel

class CreateBookRequest(BaseModel):
    title: str
    author: str
    publisher: str
    publication_year: int
    gender: str
    quantity_copies: int
    available: bool

class BookResponse(BaseModel):
    id: int
    title: str    