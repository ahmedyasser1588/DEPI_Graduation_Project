from datetime import datetime, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class AppBaseDocument(Document):
    """
    Base document containing audit timestamps and soft-delete capabilities.
    Inherited by all domain models.
    """
    created_at: datetime = Field(default_factory=utc_now, description="Record creation UTC timestamp")
    updated_at: datetime = Field(default_factory=utc_now, description="Record last update UTC timestamp")
    is_deleted: bool = Field(default=False, description="Soft delete flag")

    async def save(self, *args, **kwargs):
        """Automatically refresh updated_at before save."""
        self.updated_at = utc_now()
        return await super().save(*args, **kwargs)

    class Settings:
        use_state_management = True


class WorkspaceScopedDocument(AppBaseDocument):
    """
    Multi-tenant Base Document.
    Guarantees strict isolation by associating the entity with a specific workspace/brand.
    """
    workspace_id: PydanticObjectId = Field(
        ...,
        index=True,
        description="Reference to the brand / workspace this record belongs to"
    )

    class Settings:
        use_state_management = True


# Alias for backwards compatibility if needed
StartupScopedDocument = WorkspaceScopedDocument
