from typing import List
from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from app.routes.schemas import WorkspaceCreateRequest, WorkspaceResponse
from app.models.workspace import Workspace

workspaces_router = APIRouter(
    prefix="/api/v1/workspaces",
    tags=["Workspaces"]
)


@workspaces_router.get("/", response_model=List[WorkspaceResponse])
async def list_workspaces():
    """Retrieve all brand workspaces."""
    workspaces = await Workspace.find_all().to_list()
    return [
        WorkspaceResponse(
            id=str(w.id),
            owner_id=str(w.owner_id),
            name=w.name,
            slug=w.slug,
            brand_description=w.brand_description,
            industry=w.industry,
            target_audience=w.target_audience,
            website_url=w.website_url
        )
        for w in workspaces
    ]


@workspaces_router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(request: WorkspaceCreateRequest):
    """Create a new brand workspace."""
    # Using dummy owner id for initial dev bootstrap
    workspace = Workspace(
        owner_id=PydanticObjectId(),
        name=request.name,
        slug=request.name.lower().replace(" ", "-"),
        brand_description=request.brand_description,
        industry=request.industry,
        target_audience=request.target_audience,
        website_url=request.website_url
    )
    await workspace.insert()
    return WorkspaceResponse(
        id=str(workspace.id),
        owner_id=str(workspace.owner_id),
        name=workspace.name,
        slug=workspace.slug,
        brand_description=workspace.brand_description,
        industry=workspace.industry,
        target_audience=workspace.target_audience,
        website_url=workspace.website_url
    )
