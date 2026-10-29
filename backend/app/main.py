from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_mongodb, init_chromadb, close_mongodb
from app.routes import (
    base_router,
    auth_router,
    workspaces_router,
    agents_router,
    data_router,
    nlp_router,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: Startup and Shutdown lifecycle events."""
    logger.info("Initializing %s API services...", settings.PROJECT_NAME)
    await init_mongodb()
    init_chromadb()
    yield
    logger.info("Gracefully closing %s API connections...", settings.PROJECT_NAME)
    await close_mongodb()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous AI workforce platform with specialized AI employees, multi-tenancy, and integrated RAG.",
    version="1.0.0",
    lifespan=lifespan,
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Application Routers
app.include_router(base_router)
app.include_router(auth_router)
app.include_router(workspaces_router)
app.include_router(agents_router)
app.include_router(data_router)
app.include_router(nlp_router)
