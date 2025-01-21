[EN]
# Companies Repository

This project is a FastAPI-based application designed to manage company data using PostgreSQL for data storage. Below is a detailed guide for setting up and running the application.

---

## Project Setup

### Prerequisites
- **Python 3.10** or higher
- **PostgreSQL** installed and running
- **Git** installed on your system

---

## Steps to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eliseiv/companies-repository.git
   cd companies-repository
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Ensure PostgreSQL is running.
   - Create a new database.
   - Update the `DATABASE_URL` in `config.py` with your database credentials.

5. **Apply Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be accessible at `http://127.0.0.1:8000`.

---

## Project Overview

### Technologies Used
- **FastAPI** for building the web framework
- **SQLAlchemy** for ORM (Object Relational Mapping)
- **Alembic** for database migrations
- **PostgreSQL** as the database
- **Uvicorn** as the ASGI server

---

## Additional Notes

- All dependencies are listed in the `requirements.txt` file.
- The `Dockerfile` is included but not configured for full use in this version.
- Make sure to add `.env` support if required for secure database credentials.





[RU]
# Companies Repository

## Описание
Приложение “Companies Repository” — это API на базе FastAPI для управления данными компаний. В проекте используется PostgreSQL для хранения данных, SQLAlchemy для работы с базой данных и Alembic для управления миграциями.

---

## Использованные технологии
- **Python**: язык программирования.
- **FastAPI**: для разработки API.
- **SQLAlchemy**: для работы с базой данных.
- **Alembic**: для управления миграциями.
- **PostgreSQL**: база данных.
- **Uvicorn**: ASGI-сервер для запуска приложения.
- **Pydantic**: для валидации данных.
- **Docker**: для контейнеризации приложения.

---

## Установка и запуск приложения

### 1. Клонирование репозитория
Склонируйте репозиторий с GitHub:
```bash
git clone https://github.com/your-username/companies-repository.git
cd companies-repository
```

### 2. Создание виртуального окружения
Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для macOS/Linux:
source venv/bin/activate
```

### 3. Установка зависимостей
Установите зависимости из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных
Отредактируйте файл `alembic.ini`, указав URL вашей базы данных PostgreSQL:
```
[alembic]
sqlalchemy.url = postgresql+psycopg2://username:password@localhost/db_name
```

Примените миграции для создания необходимых таблиц:
```bash
alembic upgrade head
```

### 5. Запуск приложения
Запустите сервер разработки:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу:
```
http://127.0.0.1:8000
```

---

## Дополнительная информация

### Структура проекта:
```
.
├── app
│   ├── __init__.py
│   ├── main.py  # Точка входа приложения
│   ├── models.py  # Модели базы данных
│   ├── schemas.py  # Схемы данных
│   ├── database.py  # Подключение к базе данных
│   ├── deps.py  # Зависимости
│   └── config.py  # Конфигурация приложения
├── alembic.ini  # Настройки Alembic
├── requirements.txt  # Зависимости проекта
└── README.md  # Документация проекта
```

### Docker (опционально)
Если у вас установлен Docker, вы можете создать контейнер:
```bash
docker build -t companies-repository .
docker run -d -p 8000:8000 companies-repository
```
