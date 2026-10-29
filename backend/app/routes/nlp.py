from fastapi import APIRouter, HTTPException, status
from app.routes.schemas import SearchRequest, SearchResultItem, RAGQueryRequest, RAGQueryResponse
from app.enums import ResponseSignal
from app.rag import RAGService

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["NLP & RAG"]
)

_rag_service_instance = None


def get_rag_service() -> RAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance


@nlp_router.post("/index/search/{workspace_id}")
async def search_index(workspace_id: str, request: SearchRequest):
    """Semantic vector search across brand workspace documents."""
    try:
        service = get_rag_service()
        docs = service.retrieve(question=request.query, top_k=request.limit)
        return {
            "signal": ResponseSignal.SEARCH_VECTOR_DB_SUCCESS.value,
            "workspace_id": workspace_id,
            "results": [
                {
                    "content": d.page_content,
                    "metadata": d.metadata
                }
                for d in docs
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@nlp_router.post("/index/answer/{workspace_id}", response_model=RAGQueryResponse)
async def answer_rag_question(workspace_id: str, request: RAGQueryRequest):
    """Execute end-to-end RAG query grounded in workspace documents with citations."""
    try:
        service = get_rag_service()
        result = service.ask(question=request.question, top_k=request.limit)
        return RAGQueryResponse(
            signal=ResponseSignal.RAG_ANSWER_SUCCESS.value,
            answer=result["answer"],
            sources=result["sources"],
            total_sources=result["total_sources"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG generation failed: {str(e)}"
        )
