from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routes import book_router
from src.db.main import init_db

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app")
    await init_db()
    yield
    print("Stopping app")


app = FastAPI(
    version=version,
    title="Bookly",
    description="Super simple book api",
    lifespan=lifespan,
)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])


# 2h 57m
