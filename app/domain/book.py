from dataclasses import dataclass
import datetime

@dataclass
class Book:
    id: int
    title: str
    author: str
    publisher: str
    publication_year: int
    gender: str
    quantity_copies: int
    available: bool
    updated_in: datetime