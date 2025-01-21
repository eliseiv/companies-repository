import os

# Указываем ваш URL для PostgreSQL (Neon), включая sslmode=require
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://my_local_db_owner:oj3d8avXleSB@ep-wild-bread-a2pqs7wm.eu-central-1.aws.neon.tech/my_local_db?sslmode=require"
)

# API ключ для проверки в заголовке X-API-Key
API_KEY = os.getenv("API_KEY", "mysecretkey")
