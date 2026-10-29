from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field
from app.models.base import StartupScopedDocument


class AssignmentStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AssignmentPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssignedByType(str, Enum):
    FOUNDER = "founder"
    COFOUNDER = "cofounder"


class Assignment(StartupScopedDocument):
    """
    Structured work assignment dispatched to a specialized AI Employee.
    Can be created directly by the Founder or autonomously proposed by the Cofounder.
    """
    assigned_by: AssignedByType = Field(default=AssignedByType.FOUNDER)
    assigned_to_hired_employee_id: Indexed(PydanticObjectId) = Field(
        ...,
        description="ID of the hired employee responsible for this deliverable"
    )
    
    title: str = Field(..., description="Short summary of the task")
    goal: str = Field(..., description="Clear objective of the assignment")
    context: str = Field(..., description="Startup context, background, and specific instructions")
    
    status: Indexed(AssignmentStatus) = Field(
        default=AssignmentStatus.PENDING,
        description="Current assignment lifecycle status"
    )
    priority: AssignmentPriority = Field(default=AssignmentPriority.MEDIUM)
    
    # Workflow coordination
    dependency_assignment_ids: List[PydanticObjectId] = Field(
        default_factory=list,
        description="Assignments that must complete before this one starts"
    )
    deliverable_artifact_ids: List[PydanticObjectId] = Field(
        default_factory=list,
        description="Artifacts produced by the agent upon task completion"
    )
    
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Settings:
        name = "assignments"
