
from functools import lru_cache
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from app.rag.configuration.settings import settings


@lru_cache(maxsize=1)
def get_embedding() -> HuggingFaceEmbeddings:
    """Returns a cached HuggingFaceEmbeddings instance with cosine normalization."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model_name,
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": settings.normalize_embeddings},
    )

