import logging
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def connection_db():
    logger.info("Estabelecendo conexão com o banco de dados...")
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    logger.info("Conexão com o banco de dados estabelecida.")
    try:
        yield conn
    finally:
        conn.close()
        logger.info("Conexão com o banco de dados fechada.")          