from typing import Optional
from beanie import PydanticObjectId, Indexed
from pydantic import EmailStr, Field
from app.models.base import AppBaseDocument


class User(AppBaseDocument):
    """
    User / Founder account.
    A user can create and manage their brand workspaces.
    """
    email: EmailStr = Field(..., unique=True, description="Login email address")
    hashed_password: str = Field(..., description="Bcrypt-hashed password")
    full_name: str = Field(..., description="Full name of user")
    avatar_url: Optional[str] = Field(default=None, description="Profile picture URL")
    
    is_active: bool = Field(default=True, description="Account active status")
    is_superuser: bool = Field(default=False, description="System administrator flag")
    
    # Active workspace/brand pointer for UI convenience
    current_active_workspace_id: Optional[PydanticObjectId] = Field(
        default=None,
        description="Currently selected brand workspace (e.g. Daz)"
    )

    class Settings:
        name = "users"
