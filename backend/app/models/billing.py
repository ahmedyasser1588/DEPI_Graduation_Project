from datetime import datetime
from enum import Enum
from typing import List, Optional
from beanie import PydanticObjectId, Indexed
from pydantic import BaseModel, Field
from app.models.base import StartupScopedDocument


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    TRIALING = "trialing"


class EmployeeBillingLineItem(BaseModel):
    """Line item for a single hired specialist employee."""
    hired_employee_id: PydanticObjectId
    employee_name: str
    role: str
    monthly_rate: float
    is_active: bool = True
    added_at: datetime


class StartupBilling(StartupScopedDocument):
    """
    Per-Startup Billing and Subscription Tracker.
    Calculates monthly recurring cost based strictly on the hired specialist team.
    """
    status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)
    currency: str = Field(default="USD")
    
    # Line items for each hired AI employee
    employee_line_items: List[EmployeeBillingLineItem] = Field(default_factory=list)
    
    # Billing summary
    total_monthly_amount: float = Field(
        default=0.0,
        description="Current monthly run rate for this startup"
    )
    next_billing_date: Optional[datetime] = None
    last_payment_date: Optional[datetime] = None
    payment_method_last4: Optional[str] = None

    def recalculate_total(self) -> float:
        """Helper to recompute total monthly spend based on active hired staff."""
        self.total_monthly_amount = sum(
            item.monthly_rate for item in self.employee_line_items if item.is_active
        )
        return self.total_monthly_amount

    class Settings:
        name = "startup_billings"
