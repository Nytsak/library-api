from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/",
        json={"title": "1984", "author": "George Orwell", "year": 1949}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["year"] == 1949
    assert "id" in data


def test_get_books_cursor_pagination():
    for i in range(1, 6):
        client.post(
            "/books/",
            json={
                "title": f"Book {i}",
                "author": f"Author {i}",
                "year": 2000 + i
            }
        )

    response = client.get("/books/?limit=2")
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) == 2
    assert data["items"][0]["id"] == 1
    assert data["items"][1]["id"] == 2
    assert data["has_next"] is True
    assert data["next_cursor"] == 2

    response2 = client.get(f"/books/?limit=2&cursor={data['next_cursor']}")
    assert response2.status_code == 200
    data2 = response2.json()

    assert len(data2["items"]) == 2
    assert data2["items"][0]["id"] == 3
    assert data2["items"][1]["id"] == 4
    assert data2["has_next"] is True
    assert data2["next_cursor"] == 4