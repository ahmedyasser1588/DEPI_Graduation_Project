import pytest
from app.rag.generation.prompt import get_rag_prompt


def test_rag_prompt_structure_and_guardrails():
    prompt = get_rag_prompt()
    template_str = prompt.messages[0].prompt.template

    # Must contain context XML encapsulation
    assert "<context>" in template_str
    assert "</context>" in template_str
    assert "{context}" in template_str
    assert "{question}" in template_str

    # Must contain strict anti-hallucination instructions
    assert "Do not invent facts" in template_str
    assert "Answer the user's question using ONLY the provided context" in template_str
    assert "contain enough evidence" in template_str



def test_rag_prompt_formatting():
    prompt = get_rag_prompt()
    formatted = prompt.invoke({
        "context": "Kafka is used for payment events.",
        "question": "What is used for payments?"
    })

    text = formatted.to_string()
    assert "Kafka is used for payment events." in text
    assert "What is used for payments?" in text
