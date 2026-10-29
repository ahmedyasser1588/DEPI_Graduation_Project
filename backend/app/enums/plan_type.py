from enum import Enum


class PlanType(str, Enum):
    FREE = "free"                        # Free tier (up to 2 agents)
    PAY_AS_YOU_HIRE = "pay_as_you_hire"  # $5 / agent / month
    SCALE = "scale"                      # $50 / month (unlimited)
