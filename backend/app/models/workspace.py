from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import BaseModel, Field
from app.models.base import AppBaseDocument


class WorkspaceSettings(BaseModel):
    """Custom settings for a brand workspace."""
    default_llm_model: str = "gpt-4o"
    temperature: float = 0.7
    brand_tone: str = "professional, innovative and data-driven"
    notion_auto_sync: bool = False


class Workspace(AppBaseDocument):
    """
    Brand / Workspace document (e.g. 'Daz' clothing brand).
    Acts as the multi-tenant container for hired agents, chats, deliverables, and integrations.
    """
    owner_id: PydanticObjectId = Field(..., index=True, description="User ID of the workspace owner")
    name: str = Field(..., description="Brand or Workspace name (e.g. 'Daz', 'NovaPay')")
    slug: str = Field(..., description="URL-friendly slug")
    
    brand_description: Optional[str] = Field(
        default=None,
        description="Core overview of the brand, products, value proposition and market"
    )
    website_url: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None, description="Industry domain (e.g. E-commerce / Fashion)")
    target_audience: Optional[str] = Field(default=None, description="Ideal customer profile (ICP)")
    
    settings: WorkspaceSettings = Field(default_factory=WorkspaceSettings)

    class Settings:
        name = "workspaces"


# Alias for backward compatibility
Startup = Workspace
