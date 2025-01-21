from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

from .database import Base

# Промежуточная таблица many-to-many
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey(
        "organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    children = relationship("Activity", backref="parent", remote_side=[id])


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity", secondary=organization_activity, backref="organizations")
    phones = relationship("OrganizationPhone", cascade="all, delete-orphan")
