from app.models.base import AppBaseDocument, WorkspaceScopedDocument, StartupScopedDocument
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceSettings, Startup
from app.models.agent import (
    AgentCatalog,
    HiredAgent,
    EmployeeCatalog,
    HiredEmployee,
    EmployeeRole,
)
from app.models.chat import (
    Conversation,
    ChatMessage,
)
from app.models.deliverable import (
    Deliverable,
    Artifact,
    ArtifactType,
)
from app.models.integration import (
    UserIntegration,
)
from app.models.subscription import (
    WorkspaceSubscription,
    StartupBilling,
)
from app.models.memory import (
    DocumentMetadata,
    BrandMemory,
)
from app.enums import (
    AgentCategory,
    AgentSource,
    AgentStatus,
    DeliverableStatus,
    DeliverableType,
    IntegrationType,
    IntegrationStatus,
    MessageSender,
    PlanType,
)

ALL_DOCUMENT_MODELS = [
    User,
    Workspace,
    AgentCatalog,
    HiredAgent,
    Conversation,
    ChatMessage,
    Deliverable,
    UserIntegration,
    WorkspaceSubscription,
    DocumentMetadata,
    BrandMemory,
]

__all__ = [
    "AppBaseDocument",
    "WorkspaceScopedDocument",
    "StartupScopedDocument",
    "User",
    "Workspace",
    "WorkspaceSettings",
    "Startup",
    "AgentCatalog",
    "HiredAgent",
    "EmployeeCatalog",
    "HiredEmployee",
    "EmployeeRole",
    "Conversation",
    "ChatMessage",
    "Deliverable",
    "Artifact",
    "ArtifactType",
    "UserIntegration",
    "WorkspaceSubscription",
    "StartupBilling",
    "DocumentMetadata",
    "BrandMemory",
    "AgentCategory",
    "AgentSource",
    "AgentStatus",
    "DeliverableStatus",
    "DeliverableType",
    "IntegrationType",
    "IntegrationStatus",
    "MessageSender",
    "PlanType",
    "ALL_DOCUMENT_MODELS",
]
