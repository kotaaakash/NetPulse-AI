from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Rack(Base):
    __tablename__ = "racks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    row: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    rack_units: Mapped[int] = mapped_column(
        default=42,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=False,
    )

    location: Mapped["Location"] = relationship(
        back_populates="racks",
    )
    devices: Mapped[list["Device"]] = relationship(
    back_populates="rack",
    cascade="all, delete-orphan",
    )