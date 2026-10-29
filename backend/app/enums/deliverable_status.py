from enum import Enum


class DeliverableStatus(str, Enum):
    DRAFT = "draft"
    NEEDS_WORK = "needs_work"
    APPROVED = "approved"
    SYNCED_TO_INTEGRATION = "synced_to_integration"
