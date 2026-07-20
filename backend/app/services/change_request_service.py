from __future__ import annotations

from sqlalchemy.orm import Session

from app.enums.audit_log import AuditAction
from app.enums.change_request import (
    ChangePriority,
    ChangeRequestStatus,
)
from app.models.change_request import ChangeRequest
from app.services.audit_log_service import AuditLogService


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

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=requested_by,
            action=AuditAction.CREATED,
            old_status=ChangeRequestStatus.DRAFT,
            new_status=ChangeRequestStatus.DRAFT,
            remarks="Change request created",
        )

        return change_request

    @staticmethod
    def submit_change_request(
        db: Session,
        change_request_id: int,
    ) -> ChangeRequest:

        change_request = ChangeRequestService.get_change_request(
            db,
            change_request_id,
        )

        if change_request is None:
            raise ValueError("Change request not found")

        ChangeRequestService._validate_status(
            change_request,
            ChangeRequestStatus.DRAFT,
        )

        old_status = change_request.status

        change_request.status = ChangeRequestStatus.PENDING

        db.commit()
        db.refresh(change_request)

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=change_request.requested_by,
            action=AuditAction.SUBMITTED,
            old_status=old_status,
            new_status=change_request.status,
            remarks="Submitted for approval",
        )

        return change_request

    @staticmethod
    def approve_change_request(
        db: Session,
        change_request_id: int,
        approved_by: int | None = None,
    ) -> ChangeRequest:

        change_request = ChangeRequestService.get_change_request(
            db,
            change_request_id,
        )

        if change_request is None:
            raise ValueError("Change request not found")

        ChangeRequestService._validate_status(
            change_request,
            ChangeRequestStatus.PENDING,
        )

        old_status = change_request.status

        change_request.status = ChangeRequestStatus.APPROVED
        change_request.approved_by = approved_by

        db.commit()
        db.refresh(change_request)

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=approved_by,
            action=AuditAction.APPROVED,
            old_status=old_status,
            new_status=change_request.status,
            remarks="Change request approved",
        )

        return change_request

    @staticmethod
    def reject_change_request(
        db: Session,
        change_request_id: int,
    ) -> ChangeRequest:

        change_request = ChangeRequestService.get_change_request(
            db,
            change_request_id,
        )

        if change_request is None:
            raise ValueError("Change request not found")

        ChangeRequestService._validate_status(
            change_request,
            ChangeRequestStatus.PENDING,
        )

        old_status = change_request.status

        change_request.status = ChangeRequestStatus.REJECTED

        db.commit()
        db.refresh(change_request)

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=change_request.requested_by,
            action=AuditAction.REJECTED,
            old_status=old_status,
            new_status=change_request.status,
            remarks="Change request rejected",
        )

        return change_request

    @staticmethod
    def deploy_change_request(
        db: Session,
        change_request_id: int,
    ) -> ChangeRequest:

        change_request = ChangeRequestService.get_change_request(
            db,
            change_request_id,
        )

        if change_request is None:
            raise ValueError("Change request not found")

        ChangeRequestService._validate_status(
            change_request,
            ChangeRequestStatus.APPROVED,
        )

        old_status = change_request.status

        change_request.status = ChangeRequestStatus.DEPLOYED

        db.commit()
        db.refresh(change_request)

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=change_request.requested_by,
            action=AuditAction.DEPLOYED,
            old_status=old_status,
            new_status=change_request.status,
            remarks="Configuration deployed",
        )

        return change_request

    @staticmethod
    def rollback_change_request(
        db: Session,
        change_request_id: int,
    ) -> ChangeRequest:

        change_request = ChangeRequestService.get_change_request(
            db,
            change_request_id,
        )

        if change_request is None:
            raise ValueError("Change request not found")

        ChangeRequestService._validate_status(
            change_request,
            ChangeRequestStatus.DEPLOYED,
        )

        old_status = change_request.status

        change_request.status = ChangeRequestStatus.ROLLED_BACK

        db.commit()
        db.refresh(change_request)

        AuditLogService.create_log(
            db=db,
            change_request_id=change_request.id,
            performed_by=change_request.requested_by,
            action=AuditAction.ROLLED_BACK,
            old_status=old_status,
            new_status=change_request.status,
            remarks="Configuration rolled back",
        )

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

    @staticmethod
    def _validate_status(
        change_request: ChangeRequest,
        expected_status: ChangeRequestStatus,
    ):
        if change_request.status != expected_status:
            raise ValueError(
                f"Change request must be "
                f"{expected_status.value} "
                f"before performing this action."
            )