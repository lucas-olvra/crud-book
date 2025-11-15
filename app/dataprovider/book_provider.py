from fastapi import HTTPException
from config import connection_db
from domain.book import Book
from mapper.book_mapper import BookMapper
from psycopg2.extras import RealDictCursor
import logging

logger = logging.getLogger(__name__)

class BookDataProvider:
    @staticmethod
    async def create_book(conn: connection_db, book: Book) -> Book:
        logger.info("[DATAPROVIDER] Starting database operation")
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

    @staticmethod
    async def get_books(conn: connection_db, limit: int, offset: int) -> tuple[list[Book], int]:
        logger.info("💾 [DATAPROVIDER] Fetching list of books")
        
        query = "SELECT * FROM public.books ORDER BY id LIMIT %s OFFSET %s"
        count_query = "SELECT COUNT(*) FROM public.books"
        
        try:
            logger.info("[DATAPROVIDER] Executing COUNT query")
            cur = conn.cursor()
            cur.execute(count_query)
            total_count = cur.fetchone()[0]
            logger.info(f"[DATAPROVIDER] Total books count: {total_count}")
            
            logger.info("[DATAPROVIDER] Executing SELECT query for books list")
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (limit, offset))
            
            rows = cur.fetchall()
            logger.info(f"[DATAPROVIDER] {len(rows)} books fetched")
            cur.close()
            
            books = [BookMapper.to_domain(row) for row in rows]
            logger.info("[DATAPROVIDER] Books list retrieval completed successfully")
            return books, total_count
            
        except Exception as e:
            logger.error(f"[DATAPROVIDER] Database error: {str(e)}", exc_info=True)
            raise    