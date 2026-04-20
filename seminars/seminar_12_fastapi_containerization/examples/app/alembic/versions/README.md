"""Шаблон файла миграции Alembic.

Этот файл генерируется командой:
    alembic revision --autogenerate -m "описание изменений"

Alembic сравнивает текущее состояние БД с метаданными моделей
и генерирует функции upgrade() и downgrade().
"""

# Пример сгенерированной миграции для таблицы tasks:
#
# revision = '0001_create_tasks_table'
# down_revision = None  # первая миграция, нет предыдущей
# branch_labels = None
# depends_on = None
#
# from alembic import op
# import sqlalchemy as sa
#
#
# def upgrade() -> None:
#     op.create_table(
#         'tasks',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('title', sa.String(length=200), nullable=False),
#         sa.Column('description', sa.Text(), nullable=True),
#         sa.Column('is_done', sa.Boolean(), nullable=False),
#         sa.Column('created_at', sa.DateTime(timezone=True),
#                   server_default=sa.text('now()'), nullable=False),
#         sa.Column('updated_at', sa.DateTime(timezone=True),
#                   server_default=sa.text('now()'), nullable=False),
#         sa.PrimaryKeyConstraint('id'),
#     )
#     op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
#
#
# def downgrade() -> None:
#     op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
#     op.drop_table('tasks')
