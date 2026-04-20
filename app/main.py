from fastapi import FastAPI
from app.database import Base, engine
from app.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

app.include_router(books.router)


@app.get("/")
def root():
    return {"message": "Library API is running"}