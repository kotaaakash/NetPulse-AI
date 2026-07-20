from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
    )

    role = relationship(
        "Role",
    )

    requested_changes: Mapped[list["ChangeRequest"]] = relationship(
    foreign_keys="ChangeRequest.requested_by",
    back_populates="requester",
    )

    approved_changes: Mapped[list["ChangeRequest"]] = relationship(
        foreign_keys="ChangeRequest.approved_by",
        back_populates="approver",
    )