"""
Простое FastAPI приложение

Демонстрирует основные возможности FastAPI:
- Определение эндпоинтов
- Валидация данных с Pydantic
- Документация API
- CRUD операции
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Создаем приложение FastAPI
app = FastAPI(
    title="Пример FastAPI приложения",
    description="Простое API для управления задачами",
    version="1.0.0"
)

# Pydantic модели
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass


# Хранилище данных (в реальном приложении используйте БД)
tasks_db: List[Task] = []
task_id_counter = 1


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в Task API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/tasks", response_model=List[Task])
async def get_tasks(completed: Optional[bool] = None):
    """
    Получить список всех задач
    
    - **completed**: фильтр по статусу (опционально)
    """
    if completed is None:
        return tasks_db
    return [task for task in tasks_db if task.completed == completed]


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Получить задачу по ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Создать новую задачу"""
    global task_id_counter
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate):
    """Обновить задачу"""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_task = Task(
                id=task_id,
                title=task_update.title,
                description=task_update.description,
                completed=task_update.completed
            )
            tasks_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Удалить задачу"""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    """Отметить задачу как выполненную"""
    for task in tasks_db:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
