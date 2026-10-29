from typing import Optional, List
from pydantic import BaseModel, Field
from app.enums import AgentCategory, AgentSource, AgentStatus


class AgentCatalogResponse(BaseModel):
    id: str
    name: str
    title: str
    category: AgentCategory
    source: AgentSource
    avatar_url: str
    short_bio: str
    rating: float
    reviews_count: int
    is_star_agent: bool
    is_official: bool
    built_by: str
    tags: List[str]
    monthly_price: float
    capabilities: List[str]


class AgentHireRequest(BaseModel):
    catalog_id: str = Field(..., description="ID of agent in catalog to hire")
    custom_instructions: Optional[str] = Field(default=None, description="Custom prompt instructions or tone preference")


class HiredAgentResponse(BaseModel):
    id: str
    workspace_id: str
    catalog_id: str
    name: str
    title: str
    category: AgentCategory
    avatar_url: str
    status: AgentStatus
    monthly_price: float
    custom_instructions: Optional[str] = None
