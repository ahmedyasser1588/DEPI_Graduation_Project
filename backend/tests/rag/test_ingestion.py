import pytest
from langchain_core.documents import Document

from app.rag.ingestion.chunker import clean_text, clean_doc, metadata_fixer, chunk_documents
from app.rag.ingestion.loader import inspect_documents


def test_clean_text_normalizes_whitespace_and_newlines():
    raw_text = "Line 1\r\n\r\n   Line 2   \r\n\n\n\nLine 3"
    cleaned = clean_text(raw_text)

    # Should replace \r\n with \n and collapse 3+ blank lines into \n\n
    assert "\r" not in cleaned
    assert "Line 1\n\nLine 2\n\nLine 3" == cleaned


def test_clean_doc_preserves_metadata():
    doc = Document(
        page_content="  Hello World  \r\n\r\nTest  ",
        metadata={"document_id": "DOC-001", "version": "1.0"}
    )
    cleaned_doc = clean_doc(doc)

    assert cleaned_doc.page_content == "Hello World\n\nTest"
    assert cleaned_doc.metadata["document_id"] == "DOC-001"
    assert cleaned_doc.metadata["version"] == "1.0"


def test_metadata_fixer_sanitizes_complex_types_for_chroma():
    dirty_meta = {
        "title": "Architecture Doc",
        "version": 2.0,
        "is_active": True,
        "null_val": None,
        "nested_dict": {"sub_key": "val"},
        "tags_list": ["kafka", "events"]
    }
    fixed = metadata_fixer(dirty_meta)

    # None values should be removed
    assert "null_val" not in fixed
    # Primitive types stay as-is
    assert fixed["title"] == "Architecture Doc"
    assert fixed["version"] == 2.0
    assert fixed["is_active"] is True
    # Non-primitives are serialized into JSON strings
    assert isinstance(fixed["nested_dict"], str)
    assert '{"sub_key": "val"}' in fixed["nested_dict"]
    assert isinstance(fixed["tags_list"], str)


def test_inspect_documents_detects_empty_and_suspicious_docs():
    docs = [
        Document(page_content="Valid technical documentation content."),
        Document(page_content="   "),  # Empty
        Document(page_content="Short"),  # Suspicious (< 10 chars)
    ]
    stats = inspect_documents(docs, min_length=10)

    assert stats["total_docs"] == 3
    assert stats["empty_docs"] == 1
    assert stats["suspicious_docs"] == 1


def test_chunk_documents_enriches_metadata_and_injects_context():
    docs = [
        Document(
            page_content="Kafka provides high-throughput, fault-tolerant event streaming for payment processing.",
            metadata={"document_id": "ADR-001", "title": "Kafka Architecture", "section": "Payments"}
        )
    ]
    chunks = chunk_documents(docs, inject_context=True)

    assert len(chunks) > 0
    chunk = chunks[0]

    # Verify deterministic chunk metadata
    assert "chunk_id" in chunk.metadata
    assert "chunk_index" in chunk.metadata
    assert chunk.metadata["chunk_index"] == 0
    assert chunk.metadata["document_id"] == "ADR-001"

    # Verify context injection header was prepended
    assert "[Document: Kafka Architecture | Section: Payments]" in chunk.page_content
