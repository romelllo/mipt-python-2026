"""
Семинар 10, Блок 3: Async CRUD эндпоинты с SQLModel + PostgreSQL.

Роутер для заметок. Все операции асинхронные.
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..db import SessionDep  # type: ignore[import]
from ..models import Note, NoteCreate, NoteResponse, NoteUpdate  # type: ignore[import]

router = APIRouter(prefix="/notes", tags=["notes"])


# ============================================================
# CREATE: POST /notes → 201
# ============================================================


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=201,
    summary="Создать заметку",
)
async def create_note(note_in: NoteCreate, session: SessionDep) -> Note:
    """Создать новую заметку и сохранить в PostgreSQL.

    Возвращает созданную заметку с id и created_at.
    """
    note = Note(**note_in.model_dump())
    session.add(note)
    await session.commit()
    await session.refresh(note)  # подгрузить id и created_at из БД
    return note


# ============================================================
# READ ALL: GET /notes → 200
# ============================================================


@router.get(
    "/",
    response_model=list[NoteResponse],
    summary="Список заметок",
)
async def list_notes(
    session: SessionDep, offset: int = 0, limit: int = 100
) -> list[Note]:
    """Получить список всех заметок с пагинацией.

    - `offset` — пропустить N первых записей
    - `limit` — максимальное количество в ответе
    """
    result = await session.exec(select(Note).offset(offset).limit(limit))
    return list(result.all())


# ============================================================
# READ ONE: GET /notes/{note_id} → 200 / 404
# ============================================================


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Получить заметку по ID",
    responses={404: {"description": "Заметка не найдена"}},
)
async def get_note(note_id: int, session: SessionDep) -> Note:
    """Получить заметку по ID.

    Возвращает 404 если заметка не существует.
    """
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(
            status_code=404, detail=f"Заметка с id={note_id} не найдена"
        )
    return note


# ============================================================
# UPDATE: PATCH /notes/{note_id} → 200 / 404
# ============================================================


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Обновить заметку",
    responses={404: {"description": "Заметка не найдена"}},
)
async def update_note(
    note_id: int, note_update: NoteUpdate, session: SessionDep
) -> Note:
    """Частично обновить заметку.

    Передайте только поля, которые нужно изменить.
    """
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(
            status_code=404, detail=f"Заметка с id={note_id} не найдена"
        )
    # exclude_unset=True → обновляем только переданные поля
    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


# ============================================================
# DELETE: DELETE /notes/{note_id} → 204 / 404
# ============================================================


@router.delete(
    "/{note_id}",
    status_code=204,
    summary="Удалить заметку",
    responses={404: {"description": "Заметка не найдена"}},
)
async def delete_note(note_id: int, session: SessionDep) -> None:
    """Удалить заметку по ID.

    Возвращает 204 No Content при успехе.
    """
    note = await session.get(Note, note_id)
    if note is None:
        raise HTTPException(
            status_code=404, detail=f"Заметка с id={note_id} не найдена"
        )
    await session.delete(note)
    await session.commit()
