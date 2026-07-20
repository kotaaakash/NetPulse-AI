from enum import Enum


class ChangeRequestStatus(str, Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DEPLOYED = "Deployed"
    ROLLED_BACK = "Rolled Back"


class ChangePriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"