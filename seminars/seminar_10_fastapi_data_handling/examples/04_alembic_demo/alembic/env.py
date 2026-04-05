"""
Alembic env.py — настройка для асинхронного движка (asyncpg).

Этот файл запускается Alembic при генерации и применении миграций.
Настроен для работы с async engine (postgresql+asyncpg).

Документация: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
"""

import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ============================================================
# Добавляем корень проекта в sys.path для импорта моделей
# ============================================================
# Путь: .../04_alembic_demo/alembic/env.py
# Нам нужно добавить .../04_alembic_demo/ чтобы импортировать models.py
_demo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_demo_dir))

# ============================================================
# Импортируем метаданные моделей
# ============================================================
# ВАЖНО: импортировать все модели до использования target_metadata.
# Alembic использует SQLModel.metadata для autogenerate.
import models  # type: ignore[import]  # noqa: E402, F401 — нужен для регистрации таблиц в метаданных
from sqlmodel import SQLModel  # noqa: E402

target_metadata = SQLModel.metadata

# ============================================================
# Конфигурация Alembic
# ============================================================
config = context.config

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ============================================================
# DATABASE_URL из переменной окружения
# ============================================================
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db",
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# ============================================================
# Синхронные миграции (offline mode: --sql)
# ============================================================
def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (генерация SQL-файла).

    Используется для генерации SQL без подключения к БД:
        alembic upgrade head --sql > migrations.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Асинхронные миграции (online mode — основной)
# ============================================================
def do_run_migrations(connection: Connection) -> None:
    """Выполнить миграции в контексте синхронного соединения."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Создать async engine и выполнить миграции.

    Alembic вызывает этот корутин при online-миграции.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # не использовать connection pool для миграций
    )
    async with connectable.connect() as connection:
        # run_sync запускает синхронную функцию внутри async контекста
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Точка входа для online-миграций."""
    asyncio.run(run_async_migrations())


# ============================================================
# Выбор режима
# ============================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
