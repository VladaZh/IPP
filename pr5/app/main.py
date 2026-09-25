from fastapi import FastAPI

from app.routers.authors import router as authors_router
from app.routers.books import router as books_router

app: FastAPI = FastAPI()
app.include_router(authors_router)
app.include_router(books_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
