from typing import Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field

from app.models.base import WorkspaceScopedDocument
from app.enums import IntegrationType, IntegrationStatus


class UserIntegration(WorkspaceScopedDocument):
    """
    Connected third-party platforms (Notion, Google Drive, WhatsApp, Slack).
    Allows AI agents to read context or export deliverables directly into user tools.
    """
    provider: IntegrationType = Field(..., index=True, description="Platform type")
    status: IntegrationStatus = Field(default=IntegrationStatus.CONNECTED)
    
    account_name: Optional[str] = Field(default=None, description="Connected workspace/account name")
    access_token: Optional[str] = Field(default=None, description="Encrypted API token")
    refresh_token: Optional[str] = None
    
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration such as target Notion parent page or Drive folder"
    )

    class Settings:
        name = "user_integrations"
