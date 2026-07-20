
from enum import StrEnum
class AuditAction(StrEnum):
    CREATED = "Created"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEPLOYED = "Deployed"
    ROLLED_BACK = "Rolled Back"