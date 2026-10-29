import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from beanie import PydanticObjectId
from app.routes.schemas import ProcessRequest, FileUploadResponse
from app.enums import ResponseSignal
from app.models.memory import DocumentMetadata

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data & Ingestion"]
)


@data_router.post("/upload/{workspace_id}", response_model=FileUploadResponse)
async def upload_document(workspace_id: str, file: UploadFile = File(...)):
    """Upload brand guidelines, PDFs, or research notes for RAG grounding."""
    allowed_types = ["application/pdf", "text/plain", "text/markdown"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        )

    # In production: save file to workspace storage folder
    contents = await file.read()
    file_size = len(contents)

    doc_meta = DocumentMetadata(
        workspace_id=PydanticObjectId(workspace_id),
        filename=file.filename,
        file_size_bytes=file_size,
        mime_type=file.content_type,
        chroma_collection_name=f"workspace_{workspace_id}",
        chunks_count=0
    )
    await doc_meta.insert()

    return FileUploadResponse(
        signal=ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        file_id=str(doc_meta.id),
        filename=file.filename,
        file_size_bytes=file_size
    )
