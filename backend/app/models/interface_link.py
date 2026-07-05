from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from sqlalchemy import CheckConstraint

from app.enums.link import (
    LinkStatus,
    LinkType,
)

class InterfaceLink(Base):
    __tablename__="interface_links"
    __table_args__ = (
        CheckConstraint(
            "source_interface_id <> destination_interface_id",
            name="ck_interface_link_no_self_loop",
        ),
        UniqueConstraint(
            "source_interface_id",
            "destination_interface_id",
            name="uq_interface_link",
        ),
    )
    
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True,
    )
    
    source_interface_id:Mapped[int]=mapped_column(
        ForeignKey("interfaces.id"),
        nullable=False,
        index=True,
    )
    
    destination_interface_id: Mapped[int] = mapped_column(
        ForeignKey("interfaces.id"),
        nullable=False,
        index=True,
    )
    
    link_type: Mapped[LinkType] = mapped_column(
        Enum(LinkType),
        nullable=False,
    )

    status: Mapped[LinkStatus] = mapped_column(
        Enum(LinkStatus),
        default=LinkStatus.UP,
        nullable=False,
    )

    bandwidth: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    source_interface: Mapped["Interface"] = relationship(
        foreign_keys=[source_interface_id],
        back_populates="outgoing_links"
    )

    destination_interface: Mapped["Interface"] = relationship(
        foreign_keys=[destination_interface_id],
        back_populates="incoming_links",
        
    )
    
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False,
    )