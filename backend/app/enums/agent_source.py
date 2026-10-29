from enum import Enum


class AgentSource(str, Enum):
    OFFICIAL = "official"
    BUILT_BY_PARTNER = "built_by_partner"
    COMMUNITY = "community"
