from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from app.enums.interface import (
    InterfaceStatus,
    InterfaceType,
)
class Interface(Base):
    __tablename__="interfaces"
    
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str]= mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    description: Mapped[str | None]= mapped_column(
        String(255),
        nullable=True,
    )
    ip_address: Mapped [str |None]=mapped_column(
        String(45),
        nullable=True,
    )
    mac_address: Mapped [str | None]= mapped_column(
        String(50),
        nullable=True,
    )
    interface_type: Mapped[InterfaceType]= mapped_column(
        Enum(InterfaceType),
        nullable=False,
    )
    admin_status:Mapped[InterfaceStatus]= mapped_column(
        Enum(InterfaceStatus),
        default=InterfaceStatus.UP,
        nullable=False,
    )
    oper_status: Mapped[InterfaceStatus] = mapped_column(
        Enum(InterfaceStatus),
        default=InterfaceStatus.DOWN,
        nullable=False,
    )

    speed: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    mtu: Mapped[int] = mapped_column(
        default=1500,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"),
        nullable=False,
    )

    device: Mapped["Device"] = relationship(
        back_populates="interfaces",
    )
    