from fastapi import HTTPException
from app.config import connection_db
from app.domain.book import Book
from app.mapper.book_mapper import BookMapper
from psycopg2.extras import RealDictCursor
import logging

logger = logging.getLogger(__name__)

class BookDataProvider:
    @staticmethod
    async def create_book(conn: connection_db, book: Book) -> Book:
        logger.info("💾 [DATAPROVIDER] Starting database operation")
        logger.debug(f"[DATAPROVIDER] Book to insert: {book}")
        
        query = """
        INSERT INTO public.books (
        title, author, publisher, publication_year, gender, 
        quantity_copies, available, updated_in)
        VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING *
        """
        
        try:
            data = BookMapper.to_dict(book)
            logger.debug(f"[DATAPROVIDER] Data prepared for insertion: {data}")
            
            logger.info("[DATAPROVIDER] Executing INSERT query")
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, tuple(data.values()))
            
            row = cur.fetchone()
            logger.info(f"[DATAPROVIDER] Row inserted with ID: {row['id']}")
            
            conn.commit()
            logger.info("[DATAPROVIDER] Transaction committed")
            
            cur.close()
            
            result = BookMapper.to_domain(row)
            logger.info("✅ [DATAPROVIDER] Database operation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ [DATAPROVIDER] Database error: {str(e)}", exc_info=True)
            conn.rollback()
            logger.warning("[DATAPROVIDER] Transaction rolled back")
            raise


    @staticmethod
    async def get_book_by_id(conn: connection_db, book_id: int) -> Book:
        logger.info(f"💾 [DATAPROVIDER] Fetching book with ID: {book_id}")

        query = "SELECT * FROM public.books WHERE id = %s"
        
        try:
            logger.info("[DATAPROVIDER] Executing SELECT query")
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (book_id,))
            
            row = cur.fetchone()
            if row is None:
                error_msg = f"Book with ID {book_id} not found"
                error_msg = f"Book with ID {book_id} does not exist"
                raise HTTPException(status_code=404, detail=error_msg)
            
            logger.info(f"[DATAPROVIDER] Book fetched: ID={row['id']}, Title={row['title']}")
            cur.close()
            
            result = BookMapper.to_domain(row)
            logger.info("✅ [DATAPROVIDER] Book retrieval completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ [DATAPROVIDER] Database error: {str(e)}", exc_info=True)
            raise    