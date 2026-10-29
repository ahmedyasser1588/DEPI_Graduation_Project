from typing import List
from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from app.routes.schemas import AgentCatalogResponse, AgentHireRequest, HiredAgentResponse
from app.models.agent import AgentCatalog, HiredAgent

agents_router = APIRouter(
    prefix="/api/v1/agents",
    tags=["Agents"]
)


@agents_router.get("/catalog", response_model=List[AgentCatalogResponse])
async def get_agent_catalog():
    """Retrieve full catalog of available specialized AI employees."""
    catalog = await AgentCatalog.find_all().to_list()
    return [
        AgentCatalogResponse(
            id=str(a.id),
            name=a.name,
            title=a.title,
            category=a.category,
            source=a.source,
            avatar_url=a.avatar_url,
            short_bio=a.short_bio,
            rating=a.rating,
            reviews_count=a.reviews_count,
            is_star_agent=a.is_star_agent,
            is_official=a.is_official,
            built_by=a.built_by,
            tags=a.tags,
            monthly_price=a.monthly_price,
            capabilities=a.capabilities
        )
        for a in catalog
    ]


@agents_router.post("/hire", response_model=HiredAgentResponse, status_code=status.HTTP_201_CREATED)
async def hire_agent(request: AgentHireRequest, workspace_id: str):
    """Hire an agent from catalog into the specified brand workspace."""
    agent_template = await AgentCatalog.get(PydanticObjectId(request.catalog_id))
    if not agent_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found in catalog."
        )

    hired = HiredAgent(
        workspace_id=PydanticObjectId(workspace_id),
        catalog_id=agent_template.id,
        name=agent_template.name,
        title=agent_template.title,
        category=agent_template.category,
        avatar_url=agent_template.avatar_url,
        monthly_price=agent_template.monthly_price,
        custom_instructions=request.custom_instructions
    )
    await hired.insert()

    return HiredAgentResponse(
        id=str(hired.id),
        workspace_id=str(hired.workspace_id),
        catalog_id=str(hired.catalog_id),
        name=hired.name,
        title=hired.title,
        category=hired.category,
        avatar_url=hired.avatar_url,
        status=hired.status,
        monthly_price=hired.monthly_price,
        custom_instructions=hired.custom_instructions
    )


@agents_router.get("/my-workforce/{workspace_id}", response_model=List[HiredAgentResponse])
async def get_my_workforce(workspace_id: str):
    """Retrieve all active hired AI agents for the workspace."""
    hired_agents = await HiredAgent.find(HiredAgent.workspace_id == PydanticObjectId(workspace_id)).to_list()
    return [
        HiredAgentResponse(
            id=str(h.id),
            workspace_id=str(h.workspace_id),
            catalog_id=str(h.catalog_id),
            name=h.name,
            title=h.title,
            category=h.category,
            avatar_url=h.avatar_url,
            status=h.status,
            monthly_price=h.monthly_price,
            custom_instructions=h.custom_instructions
        )
        for h in hired_agents
    ]
