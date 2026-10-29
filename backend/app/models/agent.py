from datetime import datetime
from typing import List, Optional
from beanie import PydanticObjectId, Indexed
from pydantic import BaseModel, Field

from app.models.base import AppBaseDocument, WorkspaceScopedDocument
from app.enums import AgentCategory, AgentSource, AgentStatus


class AgentCatalog(AppBaseDocument):
    """
    Marketplace definition of an AI Agent.
    Users browse and hire agents from this catalog.
    """
    name: str = Field(..., description="Agent display name (e.g. Cole, Lily, Marcus)")
    title: str = Field(..., description="Professional title (e.g. Marketing Strategist)")
    category: AgentCategory = Field(..., index=True, description="Functional specialization")
    source: AgentSource = Field(default=AgentSource.OFFICIAL, description="Official, Partner, or Community")
    
    avatar_url: str = Field(..., description="Avatar image URL")
    short_bio: str = Field(..., description="Description of deliverables and skills")
    
    # Marketplace badges and stats
    rating: float = Field(default=5.0, description="Star rating out of 5.0")
    reviews_count: int = Field(default=0, description="Number of user ratings")
    is_star_agent: bool = Field(default=False, description="Featured badge")
    is_official: bool = Field(default=True, description="Official verified badge")
    built_by: str = Field(default="Core Platform", description="Builder name")
    
    tags: List[str] = Field(
        default_factory=list,
        description="Skill tags (e.g. ['Social copy', 'Visual specs'])"
    )
    monthly_price: float = Field(default=5.0, description="Monthly fee in USD ($5/agent/mo)")
    
    system_prompt_template: str = Field(..., description="Base AI prompt instructing role persona and output formats")
    capabilities: List[str] = Field(default_factory=list, description="Supported actions and tool integrations")

    class Settings:
        name = "agent_catalog"


class HiredAgent(WorkspaceScopedDocument):
    """
    Instance of an AI Agent hired into a user's brand workspace.
    Enables 1-on-1 direct chat and deliverable generation.
    """
    catalog_id: PydanticObjectId = Field(..., index=True, description="Reference to AgentCatalog")
    name: str = Field(..., description="Agent name")
    title: str = Field(..., description="Agent title")
    category: AgentCategory = Field(...)
    avatar_url: str = Field(...)
    
    status: AgentStatus = Field(default=AgentStatus.ACTIVE, description="Hiring status")
    monthly_price: float = Field(default=5.0, description="Effective monthly price")
    
    custom_instructions: Optional[str] = Field(
        default=None,
        description="Brand-specific guidelines or tone preferences from founder"
    )

    class Settings:
        name = "hired_agents"


# Aliases for backward compatibility
EmployeeCatalog = AgentCatalog
HiredEmployee = HiredAgent
EmployeeRole = AgentCategory
