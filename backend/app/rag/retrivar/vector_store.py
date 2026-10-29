import hashlib
import logging
from typing import List, Optional
from langchain_core.documents import Document
from langchain_chroma import Chroma
from app.rag.retrivar.embedding import get_embedding
from app.rag.configuration.settings import settings

logger = logging.getLogger(__name__)


def generate_chunk_id(chunk: Document, fallback_idx: int) -> str:
    """Generates a stable, unique ID for a chunk based on doc_id and content hash."""
    doc_id = chunk.metadata.get("document_id", "doc")
    chunk_idx = chunk.metadata.get("chunk_index", fallback_idx)
    content_hash = hashlib.md5(chunk.page_content.encode("utf-8")).hexdigest()[:8]
    return f"{doc_id}_{chunk_idx}_{content_hash}"


def get_vector_store() -> Chroma:
    """Returns an existing persistent Chroma vector store configured with HNSW settings."""
    return Chroma(
        persist_directory=str(settings.vector_store_dir),
        collection_name=settings.collection_name,
        embedding_function=get_embedding(),
        collection_metadata={
            "hnsw:space": settings.vector_space,
            "hnsw:construction_ef": settings.hnsw_construction_ef,
            "hnsw:M": settings.hnsw_m,
            "hnsw:search_ef": settings.hnsw_search_ef,
        },
    )


def create_vector_store(chunks: List[Document]) -> Chroma:
    """Creates or updates a persistent Chroma vector store with deduplicated chunks."""
    vs = get_vector_store()

    if chunks:
        ids = [generate_chunk_id(chunk, idx) for idx, chunk in enumerate(chunks)]
        logger.info(f"Adding/Upserting {len(chunks)} chunks into collection '{settings.collection_name}'...")
        vs.add_documents(documents=chunks, ids=ids)

    return vs
