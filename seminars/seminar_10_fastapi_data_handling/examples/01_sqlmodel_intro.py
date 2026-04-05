"""
Семинар 10, Блок 1: Введение в SQLModel.

Демонстрирует:
- Определение таблицы через SQLModel (table=True)
- Pydantic-схемы для Create / Response (без table=True)
- Создание in-memory SQLite движка (без Docker — для локального запуска)
- Создание таблиц (create_all)
- CRUD: INSERT, SELECT, SELECT by id, UPDATE, DELETE через SQLModel + SQLAlchemy

Запуск (из корня репозитория):
    python seminars/seminar_10_fastapi_data_handling/examples/01_sqlmodel_intro.py
"""

from datetime import datetime, timezone

from sqlmodel import Field, Session, SQLModel, create_engine, select

# ============================================================
# 1. Определение моделей
# ============================================================
# SQLModel объединяет SQLAlchemy ORM и Pydantic.
#   - table=True  → это реальная таблица в БД (SQLAlchemy ORM-модель)
#   - без table   → это Pydantic-схема (для валидации запроса/ответа)


class NoteBase(SQLModel):
    """Общие поля для Note: используются в Create и Table."""

    title: str = Field(min_length=1, max_length=200, description="Заголовок заметки")
    content: str = Field(default="", description="Содержимое заметки")


class Note(NoteBase, table=True):
    """Таблица notes в базе данных.

    Наследует NoteBase и добавляет поля, генерируемые БД.
    table=True → SQLModel создаёт реальную таблицу через SQLAlchemy.
    """

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NoteCreate(NoteBase):
    """Pydantic-схема для создания заметки.

    Клиент отправляет только title и content.
    id и created_at генерирует сервер.
    """


class NoteResponse(NoteBase):
    """Pydantic-схема ответа — включает серверные поля."""

    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# 2. Движок базы данных (SQLite in-memory для демо)
# ============================================================
# В реальном проекте: postgresql+asyncpg://user:pass@host/db
# Здесь: sqlite:// (in-memory) — работает без Docker

ENGINE = create_engine(
    "sqlite:///:memory:",
    # echo=True выводит все SQL-запросы — полезно при отладке
    echo=False,
)


def create_tables() -> None:
    """Создать все таблицы (аналог CREATE TABLE IF NOT EXISTS)."""
    SQLModel.metadata.create_all(ENGINE)


# ============================================================
# 3. CRUD-операции через SQLModel
# ============================================================


def create_note(data: NoteCreate) -> Note:
    """Создать заметку в базе данных.

    Args:
        data: валидированные данные из NoteCreate

    Returns:
        созданная заметка с заполненным id и created_at
    """
    # Note(**data.model_dump()) → создаём ORM-объект из Pydantic-схемы
    note = Note(**data.model_dump())
    with Session(ENGINE) as session:
        session.add(note)
        session.commit()
        session.refresh(note)  # обновляем объект данными из БД (id, created_at)
    return note


def get_all_notes() -> list[Note]:
    """Получить все заметки."""
    with Session(ENGINE) as session:
        # select(Note) → SELECT * FROM note
        statement = select(Note)
        return list(session.exec(statement).all())


def get_note_by_id(note_id: int) -> Note | None:
    """Получить заметку по ID.

    Returns:
        заметку или None если не найдена
    """
    with Session(ENGINE) as session:
        return session.get(Note, note_id)


def update_note(note_id: int, title: str | None, content: str | None) -> Note | None:
    """Обновить заметку.

    Args:
        note_id: идентификатор заметки
        title: новый заголовок (None → не менять)
        content: новое содержимое (None → не менять)

    Returns:
        обновлённую заметку или None если не найдена
    """
    with Session(ENGINE) as session:
        note = session.get(Note, note_id)
        if note is None:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        session.add(note)
        session.commit()
        session.refresh(note)
    return note


def delete_note(note_id: int) -> bool:
    """Удалить заметку.

    Returns:
        True если удалена, False если не найдена
    """
    with Session(ENGINE) as session:
        note = session.get(Note, note_id)
        if note is None:
            return False
        session.delete(note)
        session.commit()
    return True


# ============================================================
# 4. Демонстрация
# ============================================================


def demo() -> None:
    """Демонстрация работы SQLModel с SQLite."""
    print("=" * 60)
    print("СЕМИНАР 10, БЛОК 1: SQLModel — введение")
    print("=" * 60)
    print()

    # Создаём таблицы
    create_tables()
    print("✓ Таблицы созданы (CREATE TABLE IF NOT EXISTS)")
    print()

    # CREATE
    print("--- INSERT ---")
    note1 = create_note(NoteCreate(title="Первая заметка", content="Привет, SQLModel!"))
    note2 = create_note(
        NoteCreate(title="Вторая заметка", content="FastAPI + SQLModel = ♥")
    )
    note3 = create_note(NoteCreate(title="Пустая заметка"))
    print(
        f"  Создана: id={note1.id}, title={note1.title!r}, created_at={note1.created_at}"
    )
    print(f"  Создана: id={note2.id}, title={note2.title!r}")
    print(f"  Создана: id={note3.id}, title={note3.title!r}, content={note3.content!r}")
    print()

    # READ ALL
    print("--- SELECT ALL ---")
    notes = get_all_notes()
    for n in notes:
        print(f"  [{n.id}] {n.title!r}")
    print()

    # READ ONE
    print("--- SELECT BY ID ---")
    found = get_note_by_id(1)
    not_found = get_note_by_id(999)
    found_title = repr(found.title) if found else None
    print(f"  get_note_by_id(1)   → {found_title}")
    print(f"  get_note_by_id(999) → {not_found}")
    print()

    # UPDATE
    print("--- UPDATE ---")
    updated = update_note(1, title="Обновлённая заметка", content=None)
    print(f"  После update: title={updated.title!r}" if updated else "  Не найдена")
    print()

    # DELETE
    print("--- DELETE ---")
    deleted = delete_note(2)
    not_deleted = delete_note(999)
    print(f"  delete_note(2)   → {deleted}")
    print(f"  delete_note(999) → {not_deleted}")
    remaining = get_all_notes()
    print(f"  Осталось заметок: {len(remaining)}")
    print()

    # Pydantic-схема ответа
    print("--- NoteResponse из ORM-объекта ---")
    if remaining:
        response = NoteResponse.model_validate(remaining[0])
        print(f"  {response.model_dump()}")
    print()

    print("Ключевые выводы:")
    print("  - Note(table=True) = таблица в БД (SQLAlchemy ORM)")
    print("  - NoteCreate / NoteResponse = Pydantic-схемы (без table=True)")
    print("  - Session() — контекстный менеджер для транзакции")
    print("  - session.exec(select(Note)) — типизированный SELECT")
    print("  - session.refresh(obj) — обновить объект данными из БД")


def main() -> None:
    """Точка входа."""
    demo()


if __name__ == "__main__":
    main()
