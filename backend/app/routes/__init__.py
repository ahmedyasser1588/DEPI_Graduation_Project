from app.routes.base import base_router
from app.routes.auth import auth_router
from app.routes.workspaces import workspaces_router
from app.routes.agents import agents_router
from app.routes.data import data_router
from app.routes.nlp import nlp_router

__all__ = [
    "base_router",
    "auth_router",
    "workspaces_router",
    "agents_router",
    "data_router",
    "nlp_router",
]
