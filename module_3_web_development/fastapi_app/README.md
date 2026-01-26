# Примеры FastAPI приложений

Эта директория содержит примеры приложений на FastAPI.

## Структура

- `main.py` - Простое FastAPI приложение
- `models.py` - Pydantic модели
- `routes.py` - Определение маршрутов
- `database.py` - Работа с базой данных

## Запуск приложения

```bash
# Установить зависимости
pip install fastapi uvicorn pydantic

# Запустить сервер
uvicorn main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

Документация API: http://localhost:8000/docs

## Примеры запросов

```bash
# GET запрос
curl http://localhost:8000/

# POST запрос
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "price": 10.5}'
```
