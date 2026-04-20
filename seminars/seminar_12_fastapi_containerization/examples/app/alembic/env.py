"""Конфигурационный модуль Alembic — env.py.

Этот файл запускается Alembic при выполнении команд migrate/revision.
Он отвечает за:
1. Чтение DATABASE_URL из переменной окружения
2. Подключение к БД
3. Запуск миграций (online mode) или генерацию SQL (offline mode)
"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ============================================================
# Добавляем корень проекта в sys.path
# ============================================================
# env.py находится в app/alembic/env.py.
# Чтобы `from app.database import Base` работало,
# нужно чтобы директория /app (родитель пакета app/) была в sys.path.
# При запуске через alembic CLI это не гарантировано.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# ============================================================
# Импортируем Base и все модели, чтобы Alembic знал о таблицах
# ============================================================
# ВАЖНО: все модели должны быть импортированы ДО вызова
# Base.metadata — иначе Alembic не увидит их таблицы
# при автогенерации миграций (--autogenerate).
from app.database import Base  # noqa: E402
from app.models import Task  # noqa: E402, F401

# ============================================================
# Конфигурация логирования из alembic.ini
# ============================================================
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ============================================================
# Метаданные моделей — для автогенерации миграций
# ============================================================
target_metadata = Base.metadata

# ============================================================
# Читаем DATABASE_URL из переменной окружения
# ============================================================
# В Docker Compose переменная задаётся в блоке environment:
#   DATABASE_URL=postgresql://user:password@db:5432/tasks_db
#
# Это позволяет использовать один alembic.ini для разных окружений
# (dev, staging, production) без изменения файла конфигурации.
database_url = os.environ.get("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (генерация SQL без подключения к БД).

    Используется для генерации SQL-скриптов, которые можно применить вручную.
    Запуск: alembic upgrade head --sql
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


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме (прямое подключение к БД).

    Стандартный режим при запуске: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Выбор режима запуска
# ============================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
