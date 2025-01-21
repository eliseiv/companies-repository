Companies Repository

Приложение “Companies Repository” — это API на базе FastAPI для управления данными компаний. В проекте используется PostgreSQL для хранения данных, SQLAlchemy для работы с базой данных и Alembic для управления миграциями.


Использованные технологии
- Python: язык программирования.
- FastAPI: для разработки API.
- SQLAlchemy: для работы с базой данных.
- Alembic: для управления миграциями.
- PostgreSQL: база данных.
- Uvicorn: ASGI-сервер для запуска приложения.
- Pydantic: для валидации данных.
- Docker: для контейнеризации приложения.

---

Установка и запуск приложения

1. Клонирование репозитория
Склонируйте репозиторий с GitHub:
git clone https://github.com/your-username/companies-repository.git
cd companies-repository


2. Создание виртуального окружения
Создайте и активируйте виртуальное окружение:

python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для macOS/Linux:
source venv/bin/activate


3. Установка зависимостей
Установите зависимости из файла `requirements.txt`:
pip install -r requirements.txt


### 4. Настройка базы данных
Отредактируйте файл `alembic.ini`, указав URL вашей базы данных PostgreSQL:
[alembic]
sqlalchemy.url = postgresql+psycopg2://username:password@localhost/db_name

Примените миграции для создания необходимых таблиц:
alembic upgrade head

5. Запуск приложения
Запустите сервер разработки:
uvicorn app.main:app --reload

Приложение будет доступно по адресу:
http://127.0.0.1:8000


### Структура проекта:

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


Docker (опционально)
Если у вас установлен Docker, вы можете создать контейнер:
docker build -t companies-repository .
docker run -d -p 8000:8000 companies-repository
