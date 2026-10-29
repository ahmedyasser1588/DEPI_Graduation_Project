from enum import Enum
from typing import Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field
from app.models.base import StartupScopedDocument


class ArtifactType(str, Enum):
    RESEARCH_REPORT = "research_report"
    MARKETING_STRATEGY = "marketing_strategy"
    CONTENT_CALENDAR = "content_calendar"
    SALES_PLAYBOOK = "sales_playbook"
    FINANCIAL_MODEL = "financial_model"
    PITCH_DECK = "pitch_deck"
    INVESTOR_FAQ = "investor_faq"


class Artifact(StartupScopedDocument):
    """
    Versioned Deliverable produced by AI Employees.
    Can be reviewed, exported, or iteratively edited.
    """
    title: str = Field(..., description="Deliverable title")
    artifact_type: Indexed(ArtifactType) = Field(..., description="Category of artifact")
    version: int = Field(default=1, description="Sequential version number")
    
    # Creator info
    created_by_employee_id: PydanticObjectId = Field(
        ...,
        description="ID of the hired employee that generated this output"
    )
    assignment_id: Optional[PydanticObjectId] = Field(
        default=None,
        description="Linked assignment task if produced from an assignment"
    )
    
    # Content Representations
    summary: str = Field(..., description="Executive summary")
    content_markdown: str = Field(..., description="Markdown-formatted readable report")
    structured_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured data (e.g., financial formula cells, slide arrays, tabular data)"
    )
    
    is_current: bool = Field(default=True, description="Flag indicating if this is the latest approved version")
    file_download_url: Optional[str] = Field(default=None, description="Exported file URL (e.g. PDF, PPTX)")

    class Settings:
        name = "artifacts"
