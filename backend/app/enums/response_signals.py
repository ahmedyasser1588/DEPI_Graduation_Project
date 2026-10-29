from enum import Enum


class ResponseSignal(str, Enum):
    # File & Upload Signals
    FILE_VALIDATED_SUCCESS = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_ID_NOT_FOUND = "file_id_not_found"
    
    # Processing & Chunking Signals
    FILE_PROCESSING_SUCCESS = "file_processing_successfully"
    FILE_PROCESSING_FAILED = "file_processing_failed"
    
    # Vector DB & Search Signals
    INSERT_INTO_VECTOR_DB_SUCCESS = "insert_into_vector_db_successfully"
    INSERT_INTO_VECTOR_DB_FAILED = "insert_into_vector_db_failed"
    SEARCH_VECTOR_DB_SUCCESS = "search_vector_db_successfully"
    SEARCH_VECTOR_DB_FAILED = "search_vector_db_failed"
    RAG_ANSWER_SUCCESS = "rag_answer_generated_successfully"
    RAG_ANSWER_FAILED = "rag_answer_failed"
    
    # Workspace & Agent Signals
    WORKSPACE_NOT_FOUND = "workspace_not_found"
    WORKSPACE_CREATED_SUCCESS = "workspace_created_successfully"
    AGENT_HIRED_SUCCESS = "agent_hired_successfully"
    AGENT_NOT_FOUND = "agent_not_found"
