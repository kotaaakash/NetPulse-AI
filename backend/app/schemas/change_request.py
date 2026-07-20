from datetime import datetime

from pydantic import BaseModel

from app.enums.change_request import (
    ChangePriority,
    ChangeRequestStatus,
)


class ChangeRequestCreate(BaseModel):
    title: str
    description: str
    device_id: int
    configuration_id: int
    priority: ChangePriority = ChangePriority.MEDIUM


class ChangeRequestResponse(BaseModel):
    id: int
    title: str
    description: str

    status: ChangeRequestStatus
    priority: ChangePriority

    device_id: int
    configuration_id: int

    requested_by: int | None
    approved_by: int | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ChangeRequestListResponse(BaseModel):
    change_requests: list[ChangeRequestResponse]