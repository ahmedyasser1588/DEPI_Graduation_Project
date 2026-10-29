import pytest
from langchain_core.documents import Document

from app.rag.application.rag_service import RAGService


def test_rag_service_initialization():
    service = RAGService()
    assert service.default_retriever is not None
    assert service.prompt is not None
    assert service.llm is not None


def test_format_context_builds_structured_blocks():
    service = RAGService()
    docs = [
        Document(
            page_content="Kafka documentation details.",
            metadata={"title": "Payment Runbook", "section": "Operations"}
        ),
        Document(
            page_content="OAuth 2.0 instructions.",
            metadata={"document_id": "API-ORDERS", "section": "Auth"}
        ),
    ]

    context_str = service.format_context(docs)

    assert "[Source 1: Payment Runbook | Section: Operations]" in context_str
    assert "Kafka documentation details." in context_str
    assert "[Source 2: API-ORDERS | Section: Auth]" in context_str
    assert "OAuth 2.0 instructions." in context_str


def test_format_context_handles_empty_docs():
    service = RAGService()
    context_str = service.format_context([])
    assert context_str == "No relevant context found."
