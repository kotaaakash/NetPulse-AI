from __future__ import annotations

from datetime import UTC, datetime
from app.enums.audit_log import AuditAction
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
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True,
    )
    change_request_id: Mapped[int] = mapped_column(
    ForeignKey("change_requests.id"),
    nullable=False,
    index=True,
    )

    change_request: Mapped["ChangeRequest"] = relationship(
    back_populates="audit_logs",
    )

    performed_by: Mapped[int | None] = mapped_column(
    ForeignKey("users.id"),
    nullable=True,
    )

    user: Mapped["User"] = relationship(
    back_populates="audit_logs",
    )
    action: Mapped[AuditAction] = mapped_column(
    Enum(AuditAction),
    nullable=False,
    )

    old_status: Mapped[ChangeRequestStatus] = mapped_column(
        Enum(ChangeRequestStatus),
        nullable=False,
    )

    new_status: Mapped[ChangeRequestStatus] = mapped_column(
        Enum(ChangeRequestStatus),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False,
    )