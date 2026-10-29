from langchain_groq import ChatGroq
from app.rag.configuration.settings import settings


def get_llm():
    api_key = settings.llm_api_key or "gsk_test_placeholder_key"
    return ChatGroq(
        api_key=api_key,
        model=settings.llm_model_name
    )


