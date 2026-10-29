from datetime import datetime
from typing import Optional
from beanie import Indexed
from pydantic import Field

from app.models.base import WorkspaceScopedDocument
from app.enums import PlanType


class WorkspaceSubscription(WorkspaceScopedDocument):
    """
    Subscription and billing management for workspace.
    """
    plan: PlanType = Field(default=PlanType.FREE)
    hired_agents_count: int = Field(default=0, description="Number of currently hired agents")
    
    monthly_amount: float = Field(default=0.0, description="Monthly recurring bill in USD")
    is_active: bool = Field(default=True)
    next_billing_date: Optional[datetime] = None

    def calculate_bill(self, current_hired_count: int) -> float:
        """
        Calculates monthly price:
        - Free: 0 to 2 agents = $0
        - Pay as You Hire: first 2 free, $5 for each additional agent
        - Scale: Flat $50/mo unlimited
        """
        self.hired_agents_count = current_hired_count
        if self.plan == PlanType.SCALE:
            self.monthly_amount = 50.0
        elif self.plan == PlanType.PAY_AS_YOU_HIRE:
            billable_agents = max(0, current_hired_count - 2)
            self.monthly_amount = float(billable_agents * 5.0)
        else:  # FREE
            self.monthly_amount = 0.0
        return self.monthly_amount

    class Settings:
        name = "workspace_subscriptions"


# Alias for backward compatibility
StartupBilling = WorkspaceSubscription
