from schema.book_schema import CreateBookRequest, BookResponse, ListBooksResponse, UpdateBookRequest
from dataprovider.book_provider import BookDataProvider
from mapper.book_mapper import BookMapper
import logging

logger = logging.getLogger(__name__)

class BookService:
    def __init__(self, connection_db):
        self.connection_db = connection_db
        logger.debug("[SERVICE] BookService initialized")

    async def create_book(self, request: CreateBookRequest) -> BookResponse:
        logger.info("[SERVICE] Starting book creation process")
        logger.debug(f"[SERVICE] Request data: {request}")
        
        logger.info("[SERVICE] Mapping request to domain object")
        book = BookMapper.to_request(request)
        logger.debug(f"[SERVICE] Domain object created: {book}")
        
        logger.info("[SERVICE] Calling DataProvider to persist book")
        created_book = await BookDataProvider.create_book(self.connection_db, book)
        logger.info(f"[SERVICE] Book persisted with ID: {created_book.id}")
        
        logger.info("[SERVICE] Mapping domain object to response")
        response = BookMapper.to_response(created_book)
        logger.info("[SERVICE] Book creation completed successfully")
        
        return response
    
    async def get_book_by_id(self, book_id: int) -> BookResponse:
        logger.info(f"[SERVICE] Fetching book with ID: {book_id}")
        
        try:
            book = await BookDataProvider.get_book_by_id(self.connection_db, book_id)
            logger.info(f"[SERVICE] Book fetched: ID={book.id}, Title={book.title}")
            
            response = BookMapper.to_response(book)
            logger.info("[SERVICE] Book retrieval completed successfully")
            
            return response
        except Exception as e:
            logger.error(f"[SERVICE] Error fetching book: {str(e)}", exc_info=True)
            raise


    async def get_books(self, limit: int, offset: int) -> ListBooksResponse:
        try:
            logger.info("[SERVICE] Fetching list of books")

            books, total_count = await BookDataProvider.get_books(self.connection_db, limit, offset)
            logger.info(f"[SERVICE] {len(books)} books fetched, Total count: {total_count}")
            
            book_responses = [BookMapper.to_response(book) for book in books]
            response = ListBooksResponse(
                books=book_responses,
                totalCount=total_count,
                limit=limit,
                offset=offset
            )
            logger.info("[SERVICE] Book list retrieval completed successfully")
            return response
        except Exception as e:
            logger.error(f"[SERVICE] Error fetching book list: {str(e)}", exc_info=True)
            raise

    async def update_book(self, book_id: int, request: UpdateBookRequest) -> BookResponse:
        logger.info(f"[SERVICE] Starting update process for book ID: {book_id}")
        logger.debug(f"[SERVICE] Update request data: {request}")
        
        try:
            logger.info("[SERVICE] Fetching existing book from DataProvider")
            existing_book = await BookDataProvider.get_book_by_id(self.connection_db, book_id)
            logger.info(f"[SERVICE] Existing book fetched: ID={existing_book.id}, Title={existing_book.title}")
            
            logger.info("[SERVICE] Updating book fields")
            for field, value in request.model_dump(exclude_unset=True).items():
                setattr(existing_book, field, value)
            logger.debug(f"[SERVICE] Updated domain object: {existing_book}")
            
            logger.info("[SERVICE] Persisting updated book via DataProvider")
            updated_book = await BookDataProvider.update_book(self.connection_db, existing_book)
            logger.info(f"[SERVICE] Book updated successfully: ID={updated_book.id}")
            
            response = BookMapper.to_response(updated_book)
            logger.info("[SERVICE] Book update process completed successfully")
            return response
        except Exception as e:
            logger.error(f"[SERVICE] Error updating book: {str(e)}", exc_info=True)
            raise  

    async def delete_book(self, book_id: int) -> None:
        logger.info(f"[SERVICE] Starting deletion process for book ID: {book_id}")
        
        try:
            await BookDataProvider.delete_book(self.connection_db, book_id)
            logger.info(f"[SERVICE] Book with ID: {book_id} deleted successfully")
        except Exception as e:
            logger.error(f"[SERVICE] Error deleting book: {str(e)}", exc_info=True)
            raise    