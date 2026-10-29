from typing import Optional, Dict, Any, List
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from app.rag.generation.llm import get_llm
from app.rag.generation.prompt import get_rag_prompt
from app.rag.retrivar.retriver import get_retriver


class RAGService:
    """End-to-end RAG Service orchestrating retrieval, formatting, generation, and citations."""

    def __init__(self):
        self.default_retriever = get_retriver()
        self.prompt = get_rag_prompt()
        self.llm = get_llm()

    def format_context(self, documents: List[Document]) -> str:
        """Formats retrieved documents into clean, structured context for the LLM."""
        if not documents:
            return "No relevant context found."

        context_blocks = []
        for i, doc in enumerate(documents, start=1):
            title = doc.metadata.get("title") or doc.metadata.get("document_id") or f"Document {i}"
            section = doc.metadata.get("section", "General")
            context_blocks.append(
                f"[Source {i}: {title} | Section: {section}]\n{doc.page_content}"
            )
        return "\n\n---\n\n".join(context_blocks)

    def retrieve(
        self,
        question: str,
        strategy: Optional[str] = None,
        top_k: Optional[int] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Retrieves relevant documents with optional override for strategy and filters."""
        if strategy or top_k or metadata_filter:
            retriever = get_retriver(
                strategy=strategy,
                top_k=top_k,
                metadata_filter=metadata_filter
            )
            return retriever.invoke(question)

        return self.default_retriever.invoke(question)

    def generate(self, question: str, documents: List[Document]) -> str:
        """Generates an answer using the LLM given formatted context documents."""
        formatted_context = self.format_context(documents)

        prompt_value = self.prompt.invoke(
            {
                "context": formatted_context,
                "question": question,
            }
        )

        response = self.llm.invoke(prompt_value)
        return StrOutputParser().invoke(response)

    def ask(
        self,
        question: str,
        strategy: Optional[str] = None,
        top_k: Optional[int] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Full RAG workflow: retrieve, rerank/filter, generate answer, and return source evidence."""
        documents = self.retrieve(
            question,
            strategy=strategy,
            top_k=top_k,
            metadata_filter=metadata_filter
        )

        answer = self.generate(question, documents)

        sources = [
            {
                "document_id": doc.metadata.get("document_id"),
                "title": doc.metadata.get("title"),
                "section": doc.metadata.get("section"),
                "source": doc.metadata.get("source"),
                "rerank_score": doc.metadata.get("rerank_score"),
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in documents
        ]

        return {
            "answer": answer,
            "sources": sources,
            "total_sources": len(sources),
        }
