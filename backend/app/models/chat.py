from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId, Indexed
from pydantic import Field

from app.models.base import WorkspaceScopedDocument
from app.enums import MessageSender


class Conversation(WorkspaceScopedDocument):
    """
    Chat thread with a specific hired AI Agent (e.g. # dm-cole).
    """
    hired_agent_id: PydanticObjectId = Field(
        ...,
        index=True,
        description="The hired AI employee associated with this chat thread"
    )
    title: str = Field(
        default="New Conversation",
        description="Thread topic title"
    )
    is_pinned: bool = Field(default=False)

    class Settings:
        name = "conversations"


class ChatMessage(WorkspaceScopedDocument):
    """
    Individual message inside a conversation.
    Supports inline Deliverables, thought process, and integration actions.
    """
    conversation_id: PydanticObjectId = Field(..., index=True, description="Parent conversation ID")
    sender: MessageSender = Field(..., description="Message author: user, agent, or system")
    sender_name: str = Field(..., description="Display name")
    
    content: str = Field(..., description="Text content of the message")
    thought_process: Optional[str] = Field(
        default=None,
        description="Chain-of-thought reasoning before answering"
    )
    
    deliverable_ids: List[PydanticObjectId] = Field(
        default_factory=list,
        description="Referenced deliverables produced in this turn"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "chat_messages"
