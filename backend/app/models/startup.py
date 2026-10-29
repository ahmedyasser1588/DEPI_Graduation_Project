from enum import Enum
from typing import List, Dict, Any, Optional
from beanie import PydanticObjectId, Indexed
from pydantic import BaseModel, Field
from app.models.base import AppBaseDocument


class StartupStage(str, Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    PROTOTYPE = "prototype"
    MVP = "mvp"
    EARLY_TRACTION = "early_traction"
    SCALING = "scaling"


class StartupSettings(BaseModel):
    """Configuration specific to the startup workspace."""
    default_llm_model: str = "gpt-4o"
    temperature: float = 0.7
    enable_notifications: bool = True
    slack_webhook_url: Optional[str] = None


class Startup(AppBaseDocument):
    """
    Startup Workspace Document.
    Acts as the primary multi-tenant boundary for all context, agents, and data.
    """
    owner_id: Indexed(PydanticObjectId) = Field(..., description="User ID of the founder who owns this startup")
    name: str = Field(..., description="Startup or company name")
    tagline: Optional[str] = Field(default=None, description="One-line elevator pitch")
    
    # Domain & Industry
    industry: str = Field(..., description="Industry domain (e.g. HealthTech, FinTech, EdTech)")
    stage: StartupStage = Field(default=StartupStage.IDEA, description="Current startup lifecycle stage")
    
    # Core Strategic Canvas
    problem_statement: Optional[str] = Field(default=None, description="The core problem being addressed")
    solution_statement: Optional[str] = Field(default=None, description="The proposed solution / product")
    target_customer: Optional[str] = Field(default=None, description="Ideal Customer Profile / Segment description")
    market_geography: Optional[str] = Field(default=None, description="Target market geography (e.g., MENA, Global)")
    business_model: Optional[str] = Field(default=None, description="Revenue model (e.g., B2B SaaS, Marketplace)")
    team_size: int = Field(default=1, description="Number of human founders/team members")
    goals: List[str] = Field(default_factory=list, description="Immediate strategic goals / priorities")
    
    # Onboarding Status
    onboarding_completed: bool = Field(default=False, description="Whether guided onboarding has been finished")
    onboarding_answers: Dict[str, Any] = Field(default_factory=dict, description="Raw survey responses from onboarding")
    
    # Workspace Settings
    settings: StartupSettings = Field(default_factory=StartupSettings)

    class Settings:
        name = "startups"
