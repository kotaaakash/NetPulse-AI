from datetime import datetime

from pydantic import BaseModel

from app.enums.audit_log import AuditAction
from app.enums.change_request import ChangeRequestStatus


class AuditLogResponse(BaseModel):
    id: int
    change_request_id: int
    performed_by: int | None
    action: AuditAction
    old_status: ChangeRequestStatus
    new_status: ChangeRequestStatus
    remarks: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class AuditLogListResponse(BaseModel):
    audit_logs: list[AuditLogResponse]