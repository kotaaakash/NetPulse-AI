from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.device import (
    DeviceStatus,
    DeviceType,
    DeviceVendor,
)


class Device(Base):
    __tablename__ = "devices"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # -----------------------------
    # Identity
    # -----------------------------
    hostname: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="Unique hostname of the network device",
    )

    serial_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="Vendor serial number",
    )

    asset_tag: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Internal asset tracking ID",
    )

    # -----------------------------
    # Hardware
    # -----------------------------
    vendor: Mapped[DeviceVendor] = mapped_column(
        Enum(DeviceVendor),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device_type: Mapped[DeviceType] = mapped_column(
        Enum(DeviceType),
        nullable=False,
    )

    # -----------------------------
    # Software
    # -----------------------------
    os: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    software_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # -----------------------------
    # Management
    # -----------------------------
    management_ip: Mapped[str] = mapped_column(
        String(45),
        unique=True,
        index=True,
        nullable=False,
        comment="IPv4 or IPv6 management address",
    )

    management_mac: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # -----------------------------
    # Health
    # -----------------------------
    status: Mapped[DeviceStatus] = mapped_column(
        Enum(DeviceStatus),
        default=DeviceStatus.UNKNOWN,
        nullable=False,
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -----------------------------
    # Relationships
    # -----------------------------
    rack_id: Mapped[int] = mapped_column(
        ForeignKey("racks.id"),
        nullable=False,
    )

    rack: Mapped["Rack"] = relationship(
        back_populates="devices",
    )

    # -----------------------------
    # Audit Fields
    # -----------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    interfaces: Mapped[list["Interface"]] = relationship(
    back_populates="device",
    cascade="all, delete-orphan",
    )