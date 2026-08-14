from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime


# --- embedded, not their own collections ---

class Project(BaseModel):
    id: str
    title: str
    description: str
    image: Optional[str] = None
    link: Optional[str] = None

class Certificate(BaseModel):
    id: str
    name: str
    issuer: str
    date: Optional[str] = None


# the pydantic model we use to validate llm output against
class Info(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    github_handle: Optional[str] = None      # not LLM-extractable from resume text reliably —
    leetcode_handle: Optional[str] = None    # probably user-entered in the form step, not v1 extraction
    projects: list[Project] = []
    certificates: list[Certificate] = []


# --- top-level collections ---

class User(Document):
    email: str
    hashed_password: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"


class Portfolio(Document):
    user_id: PydanticObjectId
    slug: str           #for the time when we build shareable links
    status: Literal["draft", "published"] = "draft"

    info: Optional[Info] = None

    # which optional widgets are turned on for this portfolio
    enabled_widgets: list[Literal[
        "github_performance_card",
        "leetcode_stats_card",
        "contact_me_section",
    ]] = []

    theme: str = "default"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "portfolios"