import re
import json
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.configuration.settings import settings


def clean_text(text: str) -> str:
    """Cleans raw text by normalizing line breaks and collapsing redundant blank lines."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_doc(doc: Document) -> Document:
    """Cleans a single Document's text content while preserving metadata."""
    cleaned = clean_text(doc.page_content)
    return Document(
        page_content=cleaned,
        metadata=dict(doc.metadata),
    )


def metadata_fixer(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitizes metadata so that all values are primitive types compatible with ChromaDB."""
    cleaned: Dict[str, Any] = {}
    for k, v in metadata.items():
        if v is None:
            continue
        if isinstance(v, (str, int, float, bool)):
            cleaned[str(k)] = v
        else:
            cleaned[str(k)] = json.dumps(v, default=str)
    return cleaned


def chunk_documents(docs: List[Document], inject_context: bool = True) -> List[Document]:
    """Cleans, chunks, and sanitizes documents, assigning deterministic chunk metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )

    cleaned_docs = [clean_doc(doc) for doc in docs if doc.page_content.strip()]

    chunks = splitter.split_documents(cleaned_docs)

    processed_chunks: List[Document] = []
    chunk_counter_by_doc: Dict[str, int] = {}

    for chunk in chunks:
        meta = metadata_fixer(chunk.metadata)
        doc_id = meta.get("document_id", meta.get("source", "doc"))

        chunk_idx = chunk_counter_by_doc.get(doc_id, 0)
        chunk_counter_by_doc[doc_id] = chunk_idx + 1

        meta["chunk_index"] = chunk_idx
        meta["chunk_id"] = f"{doc_id}_chunk_{chunk_idx}"

        chunk_content = chunk.page_content
        if inject_context and meta.get("title"):
            header = f"[Document: {meta['title']} | Section: {meta.get('section', 'General')}]\n"
            meta["original_content"] = chunk_content
            chunk_content = header + chunk_content

        processed_chunks.append(
            Document(page_content=chunk_content, metadata=meta)
        )

    return processed_chunks

