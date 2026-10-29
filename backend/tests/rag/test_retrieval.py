import pytest
from langchain_core.documents import Document

from app.rag.retrivar.vector_store import generate_chunk_id
from app.rag.retrivar.retriver import (
    reciprocal_rank_fusion,
    get_retriver,
    bm25_search
)


def test_generate_chunk_id_is_deterministic():
    doc1 = Document(
        page_content="Sample text content for idempotency testing.",
        metadata={"document_id": "API-001", "chunk_index": 0}
    )
    doc2 = Document(
        page_content="Sample text content for idempotency testing.",
        metadata={"document_id": "API-001", "chunk_index": 0}
    )

    id1 = generate_chunk_id(doc1, fallback_idx=0)
    id2 = generate_chunk_id(doc2, fallback_idx=0)

    # Identical content & doc_id must yield exact same ID (Deduplication)
    assert id1 == id2
    assert id1.startswith("API-001_0_")


def test_reciprocal_rank_fusion_merges_and_deduplicates():
    doc_a = Document(page_content="Document A", metadata={"chunk_id": "doc_a"})
    doc_b = Document(page_content="Document B", metadata={"chunk_id": "doc_b"})
    doc_c = Document(page_content="Document C", metadata={"chunk_id": "doc_c"})

    # List 1 from Dense Vector Search: [A, B]
    list_dense = [doc_a, doc_b]
    # List 2 from BM25 Keyword Search: [B, C]
    list_bm25 = [doc_b, doc_c]

    fused = reciprocal_rank_fusion([list_dense, list_bm25], c=60, top_k=3)

    # Document B was present in both lists, so its RRF score must be the highest!
    assert len(fused) == 3
    assert fused[0].metadata["chunk_id"] == "doc_b"


def test_get_retriever_initialization_with_strategies():
    retriever_hybrid = get_retriver(strategy="hybrid", top_k=3)
    assert retriever_hybrid.strategy == "hybrid"
    assert retriever_hybrid.top_k == 3

    retriever_rerank = get_retriver(strategy="rerank", top_k=5)
    assert retriever_rerank.strategy == "rerank"
    assert retriever_rerank.top_k == 5

    retriever_bm25 = get_retriver(strategy="bm25", top_k=4)
    assert retriever_bm25.strategy == "bm25"
    assert retriever_bm25.top_k == 4
