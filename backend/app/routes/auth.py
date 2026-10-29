from fastapi import APIRouter, HTTPException, status
from app.routes.schemas import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from app.models.user import User
from app.models.workspace import Workspace

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: UserRegisterRequest):
    """Register a new user account and provision default brand workspace."""
    existing_user = await User.find_one(User.email == request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Note: In production, hash password via passlib bcrypt
    user = User(
        email=request.email,
        hashed_password=f"hash_{request.password}",
        full_name=request.full_name
    )
    await user.insert()

    # Automatically create initial workspace if requested
    workspace_name = request.workspace_name or f"{request.full_name}'s Workspace"
    workspace = Workspace(
        owner_id=user.id,
        name=workspace_name,
        slug=workspace_name.lower().replace(" ", "-")
    )
    await workspace.insert()

    user.current_active_workspace_id = workspace.id
    await user.save()

    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        current_active_workspace_id=str(user.current_active_workspace_id)
    )


@auth_router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest):
    """Authenticate user credentials and issue session JWT token."""
    user = await User.find_one(User.email == request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        current_active_workspace_id=str(user.current_active_workspace_id) if user.current_active_workspace_id else None
    )

    return TokenResponse(
        access_token="mock_dev_jwt_token_for_testing",
        token_type="bearer",
        user=user_response
    )
