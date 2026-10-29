import logging
from functools import lru_cache
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from pydantic import Field

from app.rag.retrivar.vector_store import get_vector_store
from app.rag.configuration.settings import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Cross-Encoder Reranker
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_cross_encoder(model_name: str):
    """Lazily loads and caches the Cross-Encoder reranker model."""
    try:
        from sentence_transformers import CrossEncoder
        logger.info(f"Loading Cross-Encoder model: {model_name}")
        return CrossEncoder(model_name)
    except Exception as e:
        logger.warning(f"Could not load CrossEncoder ({e}). Falling back to vector search.")
        return None


def rerank_documents(
    query: str,
    documents: List[Document],
    top_k: int = 5,
    model_name: Optional[str] = None
) -> List[Document]:
    """Reranks candidate documents using a Cross-Encoder for maximum relevance."""
    if not documents:
        return []

    model_name = model_name or settings.reranker_model_name
    cross_encoder = get_cross_encoder(model_name)

    if cross_encoder is None:
        return documents[:top_k]

    pairs = [[query, doc.page_content] for doc in documents]
    scores = cross_encoder.predict(pairs)

    scored_docs = []
    for doc, score in zip(documents, scores):
        doc.metadata["rerank_score"] = float(score)
        scored_docs.append((doc, float(score)))

    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored_docs[:top_k]]


# ---------------------------------------------------------------------------
# BM25 Keyword Search Engine
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_bm25_index():
    """Builds and caches a BM25 index over all documents stored in ChromaDB."""
    try:
        from rank_bm25 import BM25Okapi
        vs = get_vector_store()
        data = vs.get()

        raw_texts = data.get("documents", [])
        metadatas = data.get("metadatas", [])

        if not raw_texts:
            return None, []

        documents = [
            Document(page_content=text, metadata=meta or {})
            for text, meta in zip(raw_texts, metadatas)
        ]

        tokenized_corpus = [doc.page_content.lower().split() for doc in documents]
        bm25 = BM25Okapi(tokenized_corpus)
        return bm25, documents
    except Exception as e:
        logger.warning(f"Could not initialize BM25 index: {e}")
        return None, []


def bm25_search(
    query: str,
    top_k: int = 15,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[Document]:
    """Performs exact keyword matching using the BM25 algorithm."""
    bm25, documents = get_bm25_index()
    if not bm25 or not documents:
        return []

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    scored_results = []
    for idx, score in enumerate(scores):
        if score > 0:
            doc = documents[idx]
            if metadata_filter:
                match = all(doc.metadata.get(k) == v for k, v in metadata_filter.items())
                if not match:
                    continue
            scored_results.append((doc, score))

    scored_results.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored_results[:top_k]]


# ---------------------------------------------------------------------------
# Reciprocal Rank Fusion (RRF)
# ---------------------------------------------------------------------------
def reciprocal_rank_fusion(
    doc_lists: List[List[Document]],
    c: int = 60,
    top_k: int = 15
) -> List[Document]:
    """Fuses and deduplicates ranked lists from multiple retrievers using RRF."""
    rrf_scores: Dict[str, float] = {}
    doc_map: Dict[str, Document] = {}

    for doc_list in doc_lists:
        for rank, doc in enumerate(doc_list, start=1):
            doc_id = doc.metadata.get("chunk_id") or doc.page_content[:100]
            doc_map[doc_id] = doc
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0.0
            rrf_scores[doc_id] += 1.0 / (c + rank)

    sorted_ids = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)
    return [doc_map[doc_id] for doc_id in sorted_ids[:top_k]]


# ---------------------------------------------------------------------------
# Advanced Retriever Class
# ---------------------------------------------------------------------------
class AdvancedRAGRetriever(BaseRetriever):
    """Production-grade Retriever supporting Hybrid (BM25 + Dense + RRF), Rerank, MMR, and Similarity."""

    strategy: str = Field(default_factory=lambda: settings.retrieval_strategy)
    top_k: int = Field(default_factory=lambda: settings.top_k)
    initial_k: int = Field(default_factory=lambda: settings.initial_k)
    metadata_filter: Optional[Dict[str, Any]] = None

    def _get_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        vs = get_vector_store()
        filter_kwargs = {"filter": self.metadata_filter} if self.metadata_filter else {}

        if self.strategy == "hybrid":
            # 1. Dense Semantic Search from ChromaDB
            dense_candidates = vs.similarity_search(query, k=self.initial_k, **filter_kwargs)

            # 2. Sparse Lexical Search from BM25
            bm25_candidates = bm25_search(query, top_k=self.initial_k, metadata_filter=self.metadata_filter)

            # 3. Fuse rankings with Reciprocal Rank Fusion (RRF)
            fused_candidates = reciprocal_rank_fusion([dense_candidates, bm25_candidates], top_k=self.initial_k)

            # 4. Final Precision Re-ranking with Cross-Encoder
            return rerank_documents(query, fused_candidates, top_k=self.top_k)

        elif self.strategy == "rerank":
            candidates = vs.similarity_search(query, k=self.initial_k, **filter_kwargs)
            return rerank_documents(query, candidates, top_k=self.top_k)

        elif self.strategy == "bm25":
            return bm25_search(query, top_k=self.top_k, metadata_filter=self.metadata_filter)

        elif self.strategy == "mmr":
            return vs.max_marginal_relevance_search(
                query,
                k=self.top_k,
                fetch_k=self.initial_k,
                lambda_mult=settings.mmr_lambda,
                **filter_kwargs
            )

        else:
            return vs.similarity_search(query, k=self.top_k, **filter_kwargs)


def get_retriver(
    strategy: Optional[str] = None,
    top_k: Optional[int] = None,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> AdvancedRAGRetriever:
    """Factory function to instantiate an AdvancedRAGRetriever."""
    return AdvancedRAGRetriever(
        strategy=strategy or settings.retrieval_strategy,
        top_k=top_k or settings.top_k,
        metadata_filter=metadata_filter,
    )
