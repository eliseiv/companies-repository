from pydantic import BaseModel
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    children: List["ActivityRead"] = []

    class Config:
        orm_mode = True


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    class Config:
        orm_mode = True


class PhoneBase(BaseModel):
    phone_number: str


class PhoneCreate(PhoneBase):
    pass


class PhoneRead(PhoneBase):
    id: int

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []
    phone_numbers: List[str] = []


class OrganizationRead(OrganizationBase):
    id: int
    phones: List[PhoneRead] = []
    activities: List[ActivityRead] = []

    class Config:
        orm_mode = True


# Разрешаем рекурсивные ссылки
ActivityRead.update_forward_refs()
