from enum import Enum
from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field
from app.models.base import WorkspaceScopedDocument


class DocumentMetadata(WorkspaceScopedDocument):
    """
    Metadata for user-uploaded documents (brand PDFs, brand guidelines, notes)
    indexed in ChromaDB for grounded RAG context.
    """
    filename: str = Field(..., description="Original filename")
    file_size_bytes: int = Field(...)
    mime_type: str = Field(default="application/pdf")
    chroma_collection_name: str = Field(..., description="Chroma collection name for this workspace")
    chunks_count: int = Field(default=0)
    summary: Optional[str] = None

    class Settings:
        name = "uploaded_documents"


class BrandMemory(WorkspaceScopedDocument):
    """
    Durable brand knowledge and facts (e.g. Tone of voice, target customer, past campaign results)
    available to all hired agents.
    """
    title: str = Field(..., description="Fact or policy title")
    content: str = Field(..., description="Knowledge content")
    category: str = Field(default="brand_context", description="e.g. guidelines, target_market, pricing")
    tags: List[str] = Field(default_factory=list)

    class Settings:
        name = "brand_memories"


# Backward compatibility aliases
DecisionLog = BrandMemory
HypothesisRegister = BrandMemory
EvidenceStore = BrandMemory
