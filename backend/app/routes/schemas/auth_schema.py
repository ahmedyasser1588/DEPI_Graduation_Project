from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Account password")
    full_name: str = Field(..., min_length=2, description="Founder's full name")
    workspace_name: Optional[str] = Field(default=None, description="Optional initial brand workspace name")


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Login email")
    password: str = Field(..., description="Account password")


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    current_active_workspace_id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
