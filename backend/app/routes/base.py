from fastapi import APIRouter
from app.core.config import settings

base_router = APIRouter(
    prefix=settings.API_V1_STR,
    tags=["System"]
)


@base_router.get("/")
async def api_root():
    """Welcome endpoint providing project version and status."""
    return {
        "project": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "version": "1.0.0",
        "documentation": "/docs"
    }


@base_router.get("/health")
async def health_check():
    """Service health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }
