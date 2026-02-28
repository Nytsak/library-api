# 📚 Library API (FastAPI)

Асинхронний REST API для управління бібліотекою.

## 🔹 Технології
- FastAPI
- Pydantic
- Async/Await
- Pytest
- In-memory storage (List[Dict])

## 🔹 Функціонал

- Отримання всіх книг
- Отримання книги по ID
- Додавання книги
- Видалення книги (ідемпотентний DELETE)
- Фільтрація по статусу та автору
- Сортування по назві та року
- Валідація через Pydantic
- Unit тести

## 🔹 Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger документація:
```
http://127.0.0.1:8000/docs
```

## 🔹 Тести

```bash
pytest
```

## 🔹 Статуси книг

- available
- issued