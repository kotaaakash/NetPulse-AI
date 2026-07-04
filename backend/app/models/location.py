from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Location(Base):
    __tablename__="locations"
    id: Mapped[int]= mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )
    location_type: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )
    floor: Mapped[str|None]= mapped_column(
        String(50),
        nullable=False
    )
    description: Mapped[str|None]=mapped_column(
        String(255),
        nullable=True
    )
    site_id: Mapped[int]=mapped_column(
        ForeignKey("sites.id"),
        nullable=False
    )
    site= relationship(
        "Site",
        back_populates="locations"
    )