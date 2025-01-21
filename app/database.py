from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import DATABASE_URL

# Создаем движок PostgreSQL
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Декларативная база для моделей
Base = declarative_base()
