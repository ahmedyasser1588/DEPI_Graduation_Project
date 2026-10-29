from typing import Optional, List
from pydantic import BaseModel, Field


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Brand or company name (e.g. Daz Apparel)")
    brand_description: Optional[str] = Field(default=None, description="Overview of brand and products")
    industry: Optional[str] = Field(default=None, description="Industry sector")
    target_audience: Optional[str] = Field(default=None, description="Ideal customer persona summary")
    website_url: Optional[str] = None


class WorkspaceResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    slug: str
    brand_description: Optional[str] = None
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    website_url: Optional[str] = None
