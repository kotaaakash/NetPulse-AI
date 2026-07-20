from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base
from app.enums.change_request import (
    ChangePriority,
    ChangeRequestStatus,
)


class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[ChangeRequestStatus] = mapped_column(
        Enum(ChangeRequestStatus),
        default=ChangeRequestStatus.DRAFT,
        nullable=False,
    )

    priority: Mapped[ChangePriority] = mapped_column(
        Enum(ChangePriority),
        default=ChangePriority.MEDIUM,
        nullable=False,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"),
        nullable=False,
        index=True,
    )

    configuration_id: Mapped[int] = mapped_column(
        ForeignKey("configurations.id"),
        nullable=False,
        index=True,
    )

    requested_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

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

    device = relationship(
        "Device",
        back_populates="change_requests",
    )

    configuration = relationship(
        "Configuration",
        back_populates="change_requests",
    )

    requester = relationship(
        "User",
        foreign_keys=[requested_by],
        back_populates="requested_changes",
    )

    approver = relationship(
        "User",
        foreign_keys=[approved_by],
        back_populates="approved_changes",
    )