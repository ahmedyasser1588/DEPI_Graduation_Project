import asyncio
import logging
from app.core.database import init_mongodb, close_mongodb
from app.models.agent import AgentCatalog
from app.enums import AgentCategory, AgentSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The 6 Official AI Employees from Project Definition
PROJECT_AGENTS = [
    {
        "name": "Alex",
        "title": "AI Cofounder / Orchestrator",
        "category": AgentCategory.COFOUNDER_ORCHESTRATOR,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=AlexCofounder",
        "short_bio": "Company-wide reasoning, coordination, delegation, memory and synthesis. Always available as the central core of the company.",
        "rating": 5.0,
        "reviews_count": 210,
        "is_star_agent": True,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Company Reasoning", "Team Coordination", "Delegation", "Memory Synthesis"],
        "monthly_price": 0.0,
        "system_prompt_template": (
            "You are the central AI Cofounder and Orchestrator. You maintain company-wide context, "
            "synthesize insights across departments, and delegate specialized tasks to hired team members."
        ),
        "capabilities": ["company_reasoning", "task_delegation", "memory_synthesis", "conflict_resolution"],
    },
    {
        "name": "Nora",
        "title": "Marketing Specialist",
        "category": AgentCategory.MARKETING_SPECIALIST,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=NoraMarketing",
        "short_bio": "Marketing strategy, content, campaigns, and approved social execution.",
        "rating": 5.0,
        "reviews_count": 95,
        "is_star_agent": True,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Marketing Strategy", "Content Calendar", "Campaigns", "Social Execution"],
        "monthly_price": 5.0,
        "system_prompt_template": (
            "You are Nora, the Marketing Specialist. You develop positioning, content calendars, "
            "and marketing campaigns tailored to the startup target customer."
        ),
        "capabilities": ["gtm_strategy", "content_calendar", "campaign_planning", "social_drafting"],
    },
    {
        "name": "Karim",
        "title": "Sales Specialist",
        "category": AgentCategory.SALES_SPECIALIST,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=KarimSales",
        "short_bio": "Sales strategy and, as an explored capability, approved AI sales calls and discovery playbooks.",
        "rating": 4.9,
        "reviews_count": 78,
        "is_star_agent": False,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Sales Strategy", "Discovery Scripts", "Objection Handling", "Outbound"],
        "monthly_price": 5.0,
        "system_prompt_template": (
            "You are Karim, the Sales Specialist. You build conversion funnels, discovery scripts, "
            "and objection-handling guidance to support founder-led sales."
        ),
        "capabilities": ["sales_strategy", "discovery_playbooks", "call_prep", "objection_handling"],
    },
    {
        "name": "Tarek",
        "title": "Market & Customer Researcher",
        "category": AgentCategory.MARKET_CUSTOMER_RESEARCHER,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=TarekResearch",
        "short_bio": "Market, competitors, customers, ICPs, personas, pain points and validation.",
        "rating": 4.9,
        "reviews_count": 88,
        "is_star_agent": True,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Market Sizing", "Competitor Analysis", "ICPs & Personas", "Customer Validation"],
        "monthly_price": 5.0,
        "system_prompt_template": (
            "You are Tarek, the Market & Customer Researcher. You research market size, analyze competitors, "
            "define granular personas, and validate customer hypotheses with verified evidence."
        ),
        "capabilities": ["competitor_benchmarking", "market_sizing", "icp_definition", "interview_analysis"],
    },
    {
        "name": "Salma",
        "title": "Financial Analyst",
        "category": AgentCategory.FINANCIAL_ANALYST,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=SalmaFinance",
        "short_bio": "Advanced startup financial analysis, modeling, unit economics, and scenarios.",
        "rating": 4.8,
        "reviews_count": 64,
        "is_star_agent": False,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Financial Modeling", "Unit Economics", "Runway & Burn Rate", "Sensitivity Analysis"],
        "monthly_price": 5.0,
        "system_prompt_template": (
            "You are Salma, the Financial Analyst. You provide transparent, assumption-driven financial modeling, "
            "CAC/LTV unit economics, and runway analysis without false certainty."
        ),
        "capabilities": ["revenue_modeling", "cost_driver_analysis", "cash_flow_runway", "unit_economics"],
    },
    {
        "name": "Youssef",
        "title": "Pitch Advisor",
        "category": AgentCategory.PITCH_ADVISOR,
        "source": AgentSource.OFFICIAL,
        "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=YoussefPitch",
        "short_bio": "Pitch strategy, pitch-deck generation/review and investor preparation.",
        "rating": 5.0,
        "reviews_count": 112,
        "is_star_agent": True,
        "is_official": True,
        "built_by": "Core Platform",
        "tags": ["Pitch Strategy", "Deck Generation", "Deck Review", "Investor Q&A"],
        "monthly_price": 5.0,
        "system_prompt_template": (
            "You are Youssef, the Pitch Advisor. You help communicate the startup story to investors, "
            "generate slide content, audit existing decks, and prepare founders for VC questions."
        ),
        "capabilities": ["pitch_deck_builder", "deck_audit", "investor_qa_prep", "storyline_development"],
    },
]


async def seed_agent_catalog():
    """Seeds the 6 project AI employees into MongoDB."""
    logger.info("Seeding project AI employees catalog...")
    for agent_data in PROJECT_AGENTS:
        existing = await AgentCatalog.find_one(AgentCatalog.category == agent_data["category"])
        if not existing:
            doc = AgentCatalog(**agent_data)
            await doc.insert()
            logger.info("Seeded employee: %s - %s", doc.name, doc.title)
        else:
            logger.info("Employee already exists: %s - %s", existing.name, existing.title)


async def main():
    await init_mongodb()
    try:
        await seed_agent_catalog()
    finally:
        await close_mongodb()


if __name__ == "__main__":
    asyncio.run(main())
