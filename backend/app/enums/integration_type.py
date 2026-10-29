from enum import Enum


class IntegrationType(str, Enum):
    NOTION = "notion"
    GOOGLE_DRIVE = "google_drive"
    WHATSAPP = "whatsapp"
    SLACK = "slack"
    LINKEDIN = "linkedin"
