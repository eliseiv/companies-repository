import math
from sqlalchemy.orm import Session
from . import models, schemas


def create_building(db: Session, building: schemas.BuildingCreate):
    db_building = models.Building(
        address=building.address,
        latitude=building.latitude,
        longitude=building.longitude,
    )
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def get_building(db: Session, building_id: int):
    return db.query(models.Building).filter(models.Building.id == building_id).first()


def list_buildings(db: Session):
    return db.query(models.Building).all()


def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(
        name=activity.name,
        parent_id=activity.parent_id,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()


def list_activities(db: Session):
    return db.query(models.Activity).all()


def create_organization(db: Session, organization: schemas.OrganizationCreate):
    db_org = models.Organization(
        name=organization.name,
        building_id=organization.building_id,
    )
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    # Добавляем телефоны
    for phone in organization.phone_numbers:
        phone_obj = models.OrganizationPhone(
            phone_number=phone, organization_id=db_org.id)
        db.add(phone_obj)
    db.commit()

    # Добавляем деятельности
    if organization.activity_ids:
        activities = db.query(models.Activity).filter(
            models.Activity.id.in_(organization.activity_ids)).all()
        db_org.activities = activities
        db.commit()

    db.refresh(db_org)
    return db_org


def get_organization(db: Session, organization_id: int):
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()


def list_organizations(db: Session):
    return db.query(models.Organization).all()


def search_organization_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.name.ilike(f"%{name}%")).all()


def get_organizations_by_building(db: Session, building_id: int):
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()


def get_organizations_by_activity(db: Session, activity_id: int, depth_limit=3):
    # Рекурсивно соберём всех детей (до 3 уровней вложенности)
    def collect_child_ids(act, current_level=1):
        ids = [act.id]
        if current_level < depth_limit:
            for child in act.children:
                ids.extend(collect_child_ids(child, current_level + 1))
        return ids

    root_activity = get_activity(db, activity_id)
    if not root_activity:
        return []

    all_ids = collect_child_ids(root_activity)
    return (
        db.query(models.Organization)
        .join(models.Organization.activities)
        .filter(models.Activity.id.in_(all_ids))
        .all()
    )


def get_organizations_by_location(db: Session, center_lat: float, center_lng: float, radius_km: float):
    earth_radius = 6371.0
    organizations = db.query(models.Organization).join(models.Building).all()

    def haversine(lat1, lon1, lat2, lon2):
        import math
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2) + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * (math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius * c

    result = []
    for org in organizations:
        dist = haversine(center_lat, center_lng,
                         org.building.latitude, org.building.longitude)
        if dist <= radius_km:
            result.append(org)
    return result
