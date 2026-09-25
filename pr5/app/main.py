from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.authors import router as authors_router
from app.routers.books import router as books_router

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors_router)
app.include_router(books_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
