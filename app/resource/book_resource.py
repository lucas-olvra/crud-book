from fastapi import APIRouter, HTTPException, Depends
from service.book_service import BookService
from schema.book_schema import CreateBookRequest, BookResponse, ListBooksResponse, UpdateBookRequest
from dependencies.get_book_service import get_book_service
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse)
async def create_book(request: CreateBookRequest, book_service: BookService = Depends(get_book_service)):
    logger.info("[RESOURCE] Received request to create book")
    logger.info(f"[RESOURCE] Book data: title={request.title}, author={request.author}")
    
    try:
        created_book = await book_service.create_book(request)
        
        logger.info(f"[RESOURCE] Book created successfully with ID: {created_book.id}")
        return created_book
    except Exception as e:
        logger.error(f"[RESOURCE] Error creating book: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get(
    path="/{book_id}",
    description="Get a book by its ID",
    summary="Get Book by ID",
    status_code=200
)
async def get_book(book_id: int, book_service: BookService = Depends(get_book_service)) -> BookResponse:
    try: 
        book = await book_service.get_book_by_id(book_id)
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get(
    path="/",
    description="Get a list of books with pagination",
    summary="List Books",
    status_code=200
)    
async def get_books(
    limit: int | None = 10,
    offset: int | None = 0,
    book_service: BookService = Depends(get_book_service)
) -> ListBooksResponse:
    try:
        books_response = await book_service.get_books(limit, offset)
        return books_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.patch(
    path="/{book_id}",
    description="Update a book by its ID",
    summary="Update Book by ID",
    status_code=200
)
async def update_book(book_id: int, 
                      request: UpdateBookRequest, 
                      book_service: BookService = Depends(get_book_service)) -> BookResponse:
    logger.info(f"[RESOURCE] Received request to update book with ID: {book_id}")
    try:
        updated_book = await book_service.update_book(book_id, request)
        logger.info(f"[RESOURCE] Book with ID: {book_id} updated successfully")
        return updated_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    path="/{book_id}",
    description="Delete a book by its ID",
    summary="Delete Book by ID",
    status_code=204
)
async def delete_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    logger.info(f"[RESOURCE] Received request to delete book with ID: {book_id}")
    try:
        await book_service.delete_book(book_id)
        logger.info(f"[RESOURCE] Book with ID: {book_id} deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        

