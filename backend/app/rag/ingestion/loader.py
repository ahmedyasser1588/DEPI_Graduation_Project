import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from app.rag.configuration.settings import settings

logger = logging.getLogger(__name__)


def inspect_documents(docs: List[Document], min_length: int = 10) -> Dict[str, Any]:
    """Inspect loaded documents for quality, reporting empty or suspicious docs."""
    empty_docs = 0
    suspicious_docs = 0

    for doc in docs:
        content = doc.page_content.strip()
        if not content:
            empty_docs += 1
        elif len(content) < min_length:
            suspicious_docs += 1

    return {
        "total_docs": len(docs),
        "empty_docs": empty_docs,
        "suspicious_docs": suspicious_docs,
    }


def _load_metadata_map() -> Dict[str, Dict[str, Any]]:
    """Loads document metadata indexed by document_id from metadata_path."""
    if not settings.metadata_path.exists():
        return {}

    try:
        with open(settings.metadata_path, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)
            return {
                item["document_id"]: item
                for item in metadata_list
                if "document_id" in item
            }
    except Exception as e:
        logger.warning(f"Failed to read metadata file {settings.metadata_path}: {e}")
        return {}


def load_documents(filter_empty: bool = True) -> List[Document]:
    """Loads all TXT, PDF, and Markdown documents, enriches with metadata, and inspects quality."""
    documents: List[Document] = []

    txt_loader = DirectoryLoader(
        str(settings.data_dir),
        loader_cls=TextLoader,
        glob="**/*.txt",
        show_progress=True,
    )

    pdf_loader = DirectoryLoader(
        str(settings.data_dir),
        loader_cls=PyPDFLoader,
        glob="**/*.pdf",
        show_progress=True,
    )

    md_loader = DirectoryLoader(
        str(settings.data_dir),
        loader_cls=TextLoader,
        glob="**/*.md",
        show_progress=True,
    )

    documents.extend(txt_loader.load())
    documents.extend(pdf_loader.load())
    documents.extend(md_loader.load())

    metadata_map = _load_metadata_map()
    valid_documents: List[Document] = []

    for doc in documents:
        content = doc.page_content.strip()
        if filter_empty and not content:
            continue

        source_path = doc.metadata.get("source", "")
        doc_id = Path(source_path).stem if source_path else ""

        if doc_id in metadata_map:
            for key, val in metadata_map[doc_id].items():
                doc.metadata[key] = val
        elif doc_id:
            doc.metadata["document_id"] = doc_id

        valid_documents.append(doc)

    stats = inspect_documents(valid_documents)
    logger.info(f"Loaded {len(valid_documents)} documents. Stats: {stats}")

    return valid_documents


def _register_uploaded_metadata(doc_id: str, title: str, source_format: str):
    """Registers new uploaded document metadata into documents.json."""
    if not settings.metadata_path.exists():
        return
    try:
        with open(settings.metadata_path, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)

        existing_ids = {item.get("document_id") for item in metadata_list}
        if doc_id not in existing_ids:
            metadata_list.append({
                "document_id": doc_id,
                "title": title,
                "type": "uploaded_doc",
                "version": "1.0",
                "language": "en",
                "section": "User Uploads",
                "source_format": source_format,
            })
            with open(settings.metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata_list, f, indent=2)
            logger.info(f"Registered {doc_id} into {settings.metadata_path}")
    except Exception as e:
        logger.warning(f"Could not update metadata file: {e}")


def load_uploaded_files(uploaded_files: list) -> List[Document]:
    """Loads and parses files uploaded via Streamlit (PDF, TXT, MD) and registers them in metadata."""
    import tempfile

    documents: List[Document] = []

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_ext = Path(file_name).suffix.lower()
        doc_id = Path(file_name).stem
        title = doc_id.replace("_", " ").replace("-", " ")
        fmt = file_ext.replace(".", "")

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            if file_ext == ".pdf":
                loader = PyPDFLoader(tmp_path)
                loaded_docs = loader.load()
            elif file_ext in [".txt", ".md"]:
                loader = TextLoader(tmp_path, encoding="utf-8")
                loaded_docs = loader.load()
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                continue

            for doc in loaded_docs:
                doc.metadata["source"] = file_name
                doc.metadata["document_id"] = doc_id
                doc.metadata["title"] = title
                doc.metadata["type"] = "uploaded_doc"
                doc.metadata["section"] = "User Uploads"
                doc.metadata["source_format"] = fmt
                documents.append(doc)

            _register_uploaded_metadata(doc_id, title, fmt)

        except Exception as e:
            logger.error(f"Error loading uploaded file {file_name}: {e}")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    return [doc for doc in documents if doc.page_content.strip()]

