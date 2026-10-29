from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field
from app.models.base import StartupScopedDocument


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EDITED_AND_APPROVED = "edited_and_approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


class ExternalActionType(str, Enum):
    SOCIAL_MEDIA_POST = "social_media_post"
    EMAIL_OUTREACH = "email_outreach"
    WHATSAPP_MESSAGE = "whatsapp_message"
    SALES_CALL = "sales_call"
    CAMPAIGN_UPDATE = "campaign_update"
    THIRD_PARTY_INTEGRATION = "third_party_integration"


class ApprovalRequest(StartupScopedDocument):
    """
    Approval Center Request.
    Enforces Human-in-the-Loop governance before any agent executes an external action.
    """
    proposed_by_employee_id: PydanticObjectId = Field(
        ...,
        description="The AI employee that prepared this action"
    )
    action_type: ExternalActionType = Field(..., description="Category of external action")
    destination_platform: str = Field(
        ...,
        description="Target destination (e.g., LinkedIn, WhatsApp, Instagram, Notion)"
    )
    
    # Payload proposed by Agent
    proposed_payload: Dict[str, Any] = Field(
        ...,
        description="The exact content, post copy, recipient, or schedule parameters"
    )
    justification_reason: str = Field(
        ...,
        description="Explanation by the agent why this action is recommended"
    )
    context_summary: str = Field(
        ...,
        description="Relevant background context for the founder to make an informed decision"
    )
    
    # Review & Audit Trail
    status: Indexed(ApprovalStatus) = Field(
        default=ApprovalStatus.PENDING,
        description="Current approval status"
    )
    founder_modified_payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Modified payload if founder edited before approval"
    )
    founder_feedback: Optional[str] = Field(
        default=None,
        description="Founder's comment or reason for rejection"
    )
    
    reviewed_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    execution_result: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Log or API response after external execution"
    )

    class Settings:
        name = "approval_requests"
