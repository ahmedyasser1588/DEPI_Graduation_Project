from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    llm_api_key: str = ""
    llm_model_name: str = "llama3-70b-8192"

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    normalize_embeddings: bool = True

    chunk_size: int = 500
    chunk_overlap: int = 50

    vector_space: str = "cosine"  
    hnsw_construction_ef: int = 100
    hnsw_m: int = 16
    hnsw_search_ef: int = 50

    retrieval_strategy: str = "hybrid"  # 'hybrid', 'rerank', 'mmr', 'similarity', 'bm25'
    top_k: int = 5
    initial_k: int = 15
    mmr_lambda: float = 0.5
    score_threshold: float = 0.0
    reranker_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


    rag_base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = Path(__file__).resolve().parent.parent / "data" / "documents"
    metadata_path: Path = Path(__file__).resolve().parent.parent / "data" / "metadata" / "documents.json"
    vector_store_dir: Path = Path(__file__).resolve().parent.parent / "data" / "VS"
    collection_name: str = "Knowledge"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
