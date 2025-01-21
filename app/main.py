from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal
from . import models, schemas, crud
from .deps import verify_api_key
from .config import DATABASE_URL

import os

API_KEY_NAME = "x-api-key"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

REAL_API_KEY = "mysecretkey"


def get_api_key(api_key: str = API_KEY_HEADER):
    if api_key != REAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


app = FastAPI(
    title="Test App with Alembic + Automatic Migrations", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 1. Событие, которое срабатывает при старте приложения
# ---------------------------------------------------------


@app.on_event("startup")
def on_startup():
    apply_migrations()  # alembic upgrade head
    with SessionLocal() as db:
        init_test_data(db)  # Тестовые данные создадутся только если их нет


def apply_migrations():
    """Программно вызываем alembic upgrade head."""
    from alembic.config import Config
    from alembic import command

    # Путь к нашему alembic.ini (если он в корне проекта, то "../alembic.ini")
    alembic_cfg = Config("alembic.ini")

    # Можно принудительно задать url, если нужно:
    # alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    # Применяем все миграции вплоть до "head"
    command.upgrade(alembic_cfg, "head")


def init_test_data(db: Session):

    from .models import OrganizationPhone, Organization, Activity, Building
    building_count = db.query(models.Building).count()
    if building_count > 0:
        # Если нашли хотя бы одно здание, предполагаем, что тестовые данные уже созданы
        print("Test data already exist, skipping creation.")
        return

    # Если дошли сюда, значит building_count == 0 и таблица пустая
    # Создаём тестовые данные (однократно)

    b1 = crud.create_building(db, schemas.BuildingCreate(
        address="г. Москва, ул. Ленина, 1",
        latitude=55.7558,
        longitude=37.6173
    ))
    b2 = crud.create_building(db, schemas.BuildingCreate(
        address="г. Москва, ул. Тверская, 5",
        latitude=55.7577,
        longitude=37.6139
    ))

    # Создаём дерево деятельностей
    food = crud.create_activity(db, schemas.ActivityCreate(name="Еда"))
    meat = crud.create_activity(db, schemas.ActivityCreate(
        name="Мясная продукция", parent_id=food.id))
    milk = crud.create_activity(db, schemas.ActivityCreate(
        name="Молочная продукция", parent_id=food.id))
    # ... и т. д.

    # Создаём организации
    crud.create_organization(db, schemas.OrganizationCreate(
        name="ООО Рога и Копыта",
        building_id=b1.id,
        activity_ids=[food.id, meat.id],
        phone_numbers=["2-222-222", "8-923-666-13-13"],
    ))
    crud.create_organization(db, schemas.OrganizationCreate(
        name="ООО Молоко",
        building_id=b1.id,
        activity_ids=[milk.id],
        phone_numbers=["3-333-333"],
    ))

# ---------------------------------------------------------
# 2. Эндпоинты приложения
# ---------------------------------------------------------


@app.get("/buildings", response_model=List[schemas.BuildingRead], dependencies=[Depends(verify_api_key)])
def read_buildings(db: Session = Depends(get_db)):
    return crud.list_buildings(db)


@app.get("/buildings/{building_id}/organizations", response_model=List[schemas.OrganizationRead], dependencies=[Depends(verify_api_key)])
def read_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    return crud.get_organizations_by_building(db, building_id)


@app.get("/activities/{activity_id}/organizations", response_model=List[schemas.OrganizationRead], dependencies=[Depends(verify_api_key)])
def read_organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    return crud.get_organizations_by_activity(db, activity_id, depth_limit=3)


@app.get("/organizations/near", response_model=List[schemas.OrganizationRead], dependencies=[Depends(verify_api_key)])
def read_organizations_by_location(lat: float, lng: float, radius_km: float, db: Session = Depends(get_db)):
    return crud.get_organizations_by_location(db, lat, lng, radius_km)


@app.get("/organizations/{organization_id}", response_model=schemas.OrganizationRead, dependencies=[Depends(verify_api_key)])
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    org = crud.get_organization(db, organization_id)
    return org if org else {}


@app.get("/organizations/search", response_model=List[schemas.OrganizationRead], dependencies=[Depends(verify_api_key)])
def search_organizations(name: str, db: Session = Depends(get_db)):
    return crud.search_organization_by_name(db, name)
