from langchain_core.prompts import ChatPromptTemplate


def get_rag_prompt():

    return ChatPromptTemplate.from_template(
        """
You are an engineering knowledge assistant.

Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer
the question, say that the available knowledge base does not
contain enough evidence.

Do not invent facts.

Context:
<context>
{context}
</context>

Question:
{question}

Answer:
"""
    )
