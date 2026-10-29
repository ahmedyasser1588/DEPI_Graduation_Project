from enum import Enum
from typing import List, Optional
from beanie import PydanticObjectId, Indexed
from pydantic import BaseModel, Field
from app.models.base import AppBaseDocument, StartupScopedDocument


class EmployeeRole(str, Enum):
    COFOUNDER = "cofounder"
    MARKETING_SPECIALIST = "marketing_specialist"
    SALES_SPECIALIST = "sales_specialist"
    RESEARCHER = "market_customer_researcher"
    FINANCIAL_ANALYST = "financial_analyst"
    PITCH_ADVISOR = "pitch_advisor"


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    TERMINATED = "terminated"


class EmployeeCapability(BaseModel):
    """Specific skill or tool capability supported by the AI Employee."""
    name: str
    description: str
    requires_approval: bool = False


class EmployeeCatalog(AppBaseDocument):
    """
    System catalog defining available AI employees that startups can hire.
    """
    role: Indexed(EmployeeRole, unique=True) = Field(..., description="Role identifier")
    default_name: str = Field(..., description="Default human-style name (e.g. Nora, Karim)")
    title: str = Field(..., description="Display title (e.g. 'Marketing Specialist')")
    avatar_url: str = Field(..., description="Default avatar image path or URL")
    short_bio: str = Field(..., description="Brief biography and background description")
    
    is_core_platform: bool = Field(default=False, description="True if always available (e.g. Cofounder)")
    monthly_price: float = Field(default=49.0, description="Base monthly subscription price in USD")
    
    capabilities: List[EmployeeCapability] = Field(default_factory=list)
    system_prompt_template: str = Field(..., description="Base system instructions for this role")

    class Settings:
        name = "employee_catalog"


class HiredEmployee(StartupScopedDocument):
    """
    An instance of an AI employee hired by a specific startup workspace.
    Enforces per-startup hiring and individual subscription status.
    """
    catalog_id: PydanticObjectId = Field(..., description="Reference to EmployeeCatalog")
    role: EmployeeRole = Field(..., description="Role identifier")
    
    # Customization per startup
    custom_name: str = Field(..., description="Customized or default name")
    avatar_url: str = Field(..., description="Avatar image path")
    custom_instructions: Optional[str] = Field(
        default=None,
        description="Startup-specific instructions or founder preferences"
    )
    
    status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE, description="Current hiring status")
    monthly_price: float = Field(..., description="Effective agreed monthly fee")
    
    # Live stats
    active_assignments_count: int = Field(default=0, description="Number of currently ongoing tasks")

    class Settings:
        name = "hired_employees"
