from __future__ import annotations

from sqlalchemy.orm import Session

from app.enums.audit_log import AuditAction
from app.enums.change_request import ChangeRequestStatus
from app.models.audit_log import AuditLog


class AuditLogService:
    """
    Business logic for audit logs.
    """

    @staticmethod
    def create_log(
        db: Session,
        change_request_id: int,
        performed_by: int | None,
        action: AuditAction,
        old_status: ChangeRequestStatus,
        new_status: ChangeRequestStatus,
        remarks: str | None = None,
    ) -> AuditLog:
        """
        Create a new audit log entry.
        """

        audit_log = AuditLog(
            change_request_id=change_request_id,
            performed_by=performed_by,
            action=action,
            old_status=old_status,
            new_status=new_status,
            remarks=remarks,
        )

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log

    @staticmethod
    def get_log(
        db: Session,
        audit_log_id: int,
    ) -> AuditLog | None:
        """
        Retrieve a single audit log.
        """

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.id == audit_log_id
            )
            .first()
        )

    @staticmethod
    def get_logs_for_change_request(
        db: Session,
        change_request_id: int,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs for a change request,
        ordered from newest to oldest.
        """

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.change_request_id == change_request_id
            )
            .order_by(AuditLog.created_at.desc())
            .all()
        )