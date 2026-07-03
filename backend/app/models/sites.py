from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
class Site(Base):
    __tablename__="sites"
    
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )
    site_type: Mapped[str]= mapped_column(
        String(50),
        nullable=False
    )
    city: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )
    timezone: Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )
    status: Mapped[str]= mapped_column(
        String(20),
        default="Active"
    )
    organization_id:Mapped[int]=mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )
    organization=relationship(
        "Organization",
        back_populates="sites"
    )