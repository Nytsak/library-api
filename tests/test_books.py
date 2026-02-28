import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create
        resp = await ac.post(
            "/books/",
            json={
                "title": "Harry Potter",
                "author": "J. K. Rowling",
                "description": "Fantasy book",
                "year": 1997,
                "status": "available",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        book_id = data["id"]

        # get by id
        resp2 = await ac.get(f"/books/{book_id}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == book_id


@pytest.mark.asyncio
async def test_delete_book_idempotent():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create book
        resp = await ac.post(
            "/books/",
            json={
                "title": "Temp",
                "author": "Temp Author",
                "description": "Temp",
                "year": 2020,
                "status": "available",
            },
        )
        assert resp.status_code == 201
        book_id = resp.json()["id"]

        # delete first time
        resp_del1 = await ac.delete(f"/books/{book_id}")
        assert resp_del1.status_code == 204

        # delete second time (idempotent)
        resp_del2 = await ac.delete(f"/books/{book_id}")
        assert resp_del2.status_code == 204