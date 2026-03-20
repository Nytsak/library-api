from fastapi import FastAPI
from app.api.books import router as books_router
from app.db import engine, Base

app = FastAPI(title="Library API")

app.include_router(books_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Library API is running"}