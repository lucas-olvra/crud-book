from domain.book import Book
from schema.book_schema import CreateBookRequest, BookResponse
import datetime
import logging

logger = logging.getLogger(__name__)

class BookMapper:
    @staticmethod
    def to_domain(row) -> Book:
        """Converte uma row do banco para o objeto Book"""
        logger.debug(f"[MAPPER] Converting row to domain: {row}")
        book = Book(
            id=row['id'],
            title=row['title'],
            author=row['author'],
            publisher=row['publisher'],
            publication_year=row['publication_year'],
            gender=row['gender'],
            quantity_copies=row['quantity_copies'],
            available=row['available'],
            updated_in=row['updated_in']
        )
        logger.debug(f"[MAPPER] Domain object created: {book}")
        return book
    
    @staticmethod
    def to_dict(book: Book) -> dict:
        """Converte Book para dict para inserção no banco"""
        logger.debug(f"[MAPPER] Converting domain to dict: {book}")
        data = {
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'publication_year': book.publication_year,
            'gender': book.gender,
            'quantity_copies': book.quantity_copies,
            'available': book.available,
            'updated_in': book.updated_in
        }
        logger.debug(f"[MAPPER] Dict created: {data}")
        return data

    @staticmethod
    def to_request(request: CreateBookRequest) -> Book:
        """Converte CreateBookRequest para Book"""
        logger.debug(f"[MAPPER] Converting request to domain: {request}")
        book = Book(
            id=None,
            title=request.title,
            author=request.author,
            publisher=request.publisher,
            publication_year=request.publication_year,
            gender=request.gender,
            quantity_copies=request.quantity_copies,
            available=request.available,
            updated_in=datetime.datetime.now()
        )
        logger.debug(f"[MAPPER] Domain object created from request: {book}")
        return book
    
    @staticmethod
    def to_response(book: Book) -> BookResponse:
        """Converte Book para BookResponse"""
        logger.debug(f"[MAPPER] Converting domain to response: {book}")
        response = BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            publication_year=book.publication_year,
            gender=book.gender,
            quantity_copies=book.quantity_copies,
            available=book.available,
            updated_in=book.updated_in
        )
        logger.debug(f"[MAPPER] Response object created: {response}")
        return response