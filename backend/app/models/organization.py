from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
class Organization(Base):
    __tablename__="organizations"
    
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True
    )
    name: Mapped[str]=mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str]=mapped_column(
        String(255),
        nullable=True
    )
    sites = relationship(
        "Site",
        back_populates="organization",
        cascade="all,delete-orphan"
    )