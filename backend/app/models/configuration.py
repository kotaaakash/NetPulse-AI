from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.configuration import ConfigurationType


class Configuration(Base):
    __tablename__= "configurations"
    __table_args__=(
        UniqueConstraint(
            "device_id",
            "version",
            name="uq_device_configuration_version"
        ),
    )
    id:Mapped[int]=mapped_column(
        primary_key=True,
        index=True,
    )
    device_id:Mapped[int]=mapped_column(
        ForeignKey("devices.id"),
        nullable=False,
        index=True,
    )
    device: Mapped["Device"]=relationship(
        back_populates="configurations",
    )
    version: Mapped[int]=mapped_column(
        nullable=False,
    )
    config_type:Mapped[ConfigurationType]=mapped_column(
        Enum(ConfigurationType),
        nullable=False,
    )
    checksum:Mapped[str]=mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    content:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )
    collected_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    change_requests: Mapped[list["ChangeRequest"]] = relationship(
    back_populates="configuration",
    )