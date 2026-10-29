from typing import Optional
from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    file_id: Optional[str] = Field(default=None, description="Specific file ID to process or None for all")
    chunk_size: int = Field(default=500, description="Token/character chunk size")
    overlap_size: int = Field(default=50, description="Overlap between consecutive chunks")
    do_reset: bool = Field(default=False, description="Reset previous chunks before processing")


class FileUploadResponse(BaseModel):
    signal: str
    file_id: str
    filename: str
    file_size_bytes: int
