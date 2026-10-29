from enum import Enum


class DeliverableType(str, Enum):
    MARKETING_PLAN = "marketing_plan"
    SOCIAL_POSTS = "social_posts"
    PITCH_DECK = "pitch_deck"
    COMPETITOR_RESEARCH = "competitor_research"
    FINANCIAL_MODEL = "financial_model"
    SALES_PLAYBOOK = "sales_playbook"
    DOCUMENT = "document"
