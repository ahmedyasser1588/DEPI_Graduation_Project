from enum import Enum


class MessageSender(str, Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
