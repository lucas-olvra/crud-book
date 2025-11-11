from app.schema.book_schema import CreateBookRequest, BookResponse
from app.dataprovider.book_provider import BookDataProvider
from app.mapper.book_mapper import BookMapper
import logging

logger = logging.getLogger(__name__)

class BookService:
    def __init__(self, connection_db):
        self.connection_db = connection_db
        logger.debug("[SERVICE] BookService initialized")

    async def create_book(self, request: CreateBookRequest) -> BookResponse:
        logger.info("🔧 [SERVICE] Starting book creation process")
        logger.debug(f"[SERVICE] Request data: {request}")
        
        # Converte request para domain
        logger.info("[SERVICE] Mapping request to domain object")
        book = BookMapper.to_request(request)
        logger.debug(f"[SERVICE] Domain object created: {book}")
        
        # Chama o DataProvider
        logger.info("[SERVICE] Calling DataProvider to persist book")
        created_book = await BookDataProvider.create_book(self.connection_db, book)
        logger.info(f"[SERVICE] Book persisted with ID: {created_book.id}")
        
        # Converte para response
        logger.info("[SERVICE] Mapping domain object to response")
        response = BookMapper.to_response(created_book)
        logger.info("✅ [SERVICE] Book creation completed successfully")
        
        return response
    
    async def get_book_by_id(self, book_id: int) -> BookResponse:
        logger.info(f"🔧 [SERVICE] Fetching book with ID: {book_id}")
        
        try:
            # Chama o DataProvider
            book = await BookDataProvider.get_book_by_id(self.connection_db, book_id)
            logger.info(f"[SERVICE] Book fetched: ID={book.id}, Title={book.title}")
            
            # Converte para response
            response = BookMapper.to_response(book)
            logger.info("✅ [SERVICE] Book retrieval completed successfully")
            
            return response
        except Exception as e:
            logger.error(f"❌ [SERVICE] Error fetching book: {str(e)}", exc_info=True)
            raise