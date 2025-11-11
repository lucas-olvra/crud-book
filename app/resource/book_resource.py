from fastapi import APIRouter, HTTPException, Depends
from app.config import connection_db
from app.service.book_service import BookService
from app.schema.book_schema import CreateBookRequest, BookResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse)
async def create_book(request: CreateBookRequest, connection_db = Depends(connection_db)):
    logger.info("=" * 60)
    logger.info("📥 [RESOURCE] Received request to create book")
    logger.info(f"[RESOURCE] Book data: title={request.title}, author={request.author}")
    
    try:
        book_service = BookService(connection_db)
        created_book = await book_service.create_book(request)
        
        logger.info(f"✅ [RESOURCE] Book created successfully with ID: {created_book.id}")
        logger.info("=" * 60)
        return created_book
    except Exception as e:
        logger.error(f"❌ [RESOURCE] Error creating book: {str(e)}", exc_info=True)
        logger.info("=" * 60)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get(
    path="/{book_id}",
    description="Get a book by its ID",
    summary="Get Book by ID",
    status_code=200
)
async def get_book(book_id: int, connection_db = Depends(connection_db)) -> BookResponse:
    try: 
        book_service = BookService(connection_db)
        book = await book_service.get_book_by_id(book_id)
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

