import logging
from fastapi import Depends
from config import connection_db
from service.book_service import BookService

logger = logging.getLogger(__name__)
async def get_book_service(connection = Depends(connection_db)) -> BookService:
    logger.info("Conexão foi estabelecida com sucesso. Criando BookService...")
    logger.info("[DEPENDENCY] Criando dependencia do BookService")
    return BookService(connection)