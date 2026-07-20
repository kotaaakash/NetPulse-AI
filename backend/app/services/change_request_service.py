from __future__ import annotations

from sqlalchemy.orm import Session

from app.enums.change_request import (
    ChangePriority,
    ChangeRequestStatus,
)
from app.models.change_request import ChangeRequest


class ChangeRequestService:
    """
    Business logic for change requests.
    """

    @staticmethod
    def create_change_request(
        db: Session,
        title: str,
        description: str,
        device_id: int,
        configuration_id: int,
        priority: ChangePriority,
        requested_by: int | None = None,
    ) -> ChangeRequest:

        change_request = ChangeRequest(
            title=title,
            description=description,
            device_id=device_id,
            configuration_id=configuration_id,
            priority=priority,
            status=ChangeRequestStatus.DRAFT,
            requested_by=requested_by,
        )

        db.add(change_request)
        db.commit()
        db.refresh(change_request)

        return change_request

    @staticmethod
    def get_change_request(
        db: Session,
        change_request_id: int,
    ) -> ChangeRequest | None:
        return (
            db.query(ChangeRequest)
            .filter(
                ChangeRequest.id == change_request_id
            )
            .first()
        )

    @staticmethod
    def get_all_change_requests(
        db: Session,
    ) -> list[ChangeRequest]:
        return (
            db.query(ChangeRequest)
            .order_by(ChangeRequest.created_at.desc())
            .all()
        )