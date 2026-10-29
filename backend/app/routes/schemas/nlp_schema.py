from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PushRequest(BaseModel):
    page_size: int = Field(default=50, description="Batch size for vector ingestion")
    do_reset: bool = Field(default=False, description="Reset vector collection before ingestion")


class SearchRequest(BaseModel):
    query: str = Field(..., description="Semantic search query text")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of chunks to retrieve")


class SearchResultItem(BaseModel):
    content: str
    metadata: Dict[str, Any]


class RAGQueryRequest(BaseModel):
    question: str = Field(..., description="User query / question for RAG")
    limit: int = Field(default=5, description="Number of context passages to retrieve")


class RAGQueryResponse(BaseModel):
    signal: str
    answer: str
    sources: List[Dict[str, Any]]
    total_sources: int
