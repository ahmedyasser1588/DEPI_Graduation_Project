import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.models import ALL_DOCUMENT_MODELS

logger = logging.getLogger(__name__)

class DatabaseManager:
    client: AsyncIOMotorClient = None
    chroma_client = None

db_manager = DatabaseManager()


async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM with all document models."""
    logger.info("Connecting to MongoDB at: %s", settings.MONGODB_URL)
    db_manager.client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = db_manager.client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=ALL_DOCUMENT_MODELS
    )
    logger.info("MongoDB & Beanie ODM successfully initialized.")


def init_chromadb():
    """Initialize ChromaDB client for vector storage and RAG."""
    logger.info("Connecting to ChromaDB at %s:%s", settings.CHROMA_HOST, settings.CHROMA_PORT)
    try:
        db_manager.chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        logger.info("ChromaDB HTTP Client initialized.")
    except Exception as e:
        logger.warning("Could not connect to ChromaDB HTTP Server directly (%s). Using local persistent fallback if needed.", e)
        db_manager.chroma_client = chromadb.PersistentClient(path="./chroma_data")


async def close_mongodb():
    """Close MongoDB connections."""
    if db_manager.client:
        db_manager.client.close()
        logger.info("MongoDB connection closed.")
