import logging
from fastapi import FastAPI
from app.resource.book_resource import router as book_router

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Library Management System", 
    version="1.0.0"
)

app.include_router(book_router)

@app.get("/health", tags=["Health"])
async def root():
    logger.info("Health check endpoint called")
    return {"message": "Welcome to the Library Management System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)