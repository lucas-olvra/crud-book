import logging
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def connection_db():
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    logger.info("Database connection established.")
    try:
        yield conn
    finally:
        conn.close()
        logger.info("Database connection closed.")          