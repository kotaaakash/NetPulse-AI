from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.audit_log import (
    AuditLogListResponse,
    AuditLogResponse,
)
from app.services.audit_log_service import AuditLogService

router = APIRouter(
    prefix="/change-requests",
    tags=["Audit Logs"],
)


@router.get(
    "/{change_request_id}/audit-logs",
    response_model=AuditLogListResponse,
    summary="Get audit logs for a change request",
)
def get_audit_logs(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    audit_logs = AuditLogService.get_logs_for_change_request(
        db=db,
        change_request_id=change_request_id,
    )

    return AuditLogListResponse(
        audit_logs=audit_logs,
    )


@router.get(
    "/audit-logs/{audit_log_id}",
    response_model=AuditLogResponse,
    summary="Get an audit log",
)
def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
):
    audit_log = AuditLogService.get_log(
        db=db,
        audit_log_id=audit_log_id,
    )

    if audit_log is None:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found",
        )

    return audit_log