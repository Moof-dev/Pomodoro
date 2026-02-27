import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine # Добавлено для асинхронности

from alembic import context

# Импорт твоих настроек и базы
from app.settings import Setting
from app.infrastructure.database import Base
# Импорт всех моделей для autogenerate
settings = Setting()
config = context.config

# Устанавливаем URL базы данных из твоих настроек
config.set_main_option("sqlalchemy.url", settings.db_url)

# 2. Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Метаданные моделей
target_metadata = Base.metadata

def do_run_migrations(connection):
    """
    Вспомогательная синхронная функция для выполнения миграций.
    Именно здесь настраивается контекст Alembic.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True, # Позволяет Alembic видеть изменения типов полей
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_offline() -> None:
    """Запуск миграций в offline режиме (генерация SQL скрипта)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """
    Запуск миграций в online режиме.
    Создает асинхронный движок и использует run_sync для запуска Alembic.
    """
    # Создаем асинхронный движок
    connectable = create_async_engine(
        settings.db_url,
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        # Выполняем синхронную функцию do_run_migrations в асинхронном контексте
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

# 4. Логика запуска
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Запускаем асинхронную функцию через asyncio
    asyncio.run(run_migrations_online())