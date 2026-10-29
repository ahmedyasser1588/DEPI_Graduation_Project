from enum import Enum


class AgentCategory(str, Enum):
    COFOUNDER_ORCHESTRATOR = "cofounder_orchestrator"
    MARKETING_SPECIALIST = "marketing_specialist"
    SALES_SPECIALIST = "sales_specialist"
    MARKET_CUSTOMER_RESEARCHER = "market_customer_researcher"
    FINANCIAL_ANALYST = "financial_analyst"
    PITCH_ADVISOR = "pitch_advisor"
