from app.models import (Activity, Building, Organization,
                        OrganizationPhone, organization_activity)
from app.database import Base
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Добавим путь к нашему коду:
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")


config = context.config

# Прочитаем настройки логгера
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    # Либо читаем из переменной окружения, либо из alembic.ini
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    return url


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = get_url()
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # Переопределим connectable.url
    connectable.url = url

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
