from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime 
from enum import Enum

class ProjectStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

class ProjectBase(BaseModel):
    title: str = Field(..., max_length=150)
    status: ProjectStatus = ProjectStatus.OPEN
    current_row: int = 0
    target_row: int
    hook_size: str = Field(..., max_length=20)
    timer_seconds: Optional[int] = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, max_lenght=150)
    status: Optional[str] = None
    current_row: Optional[int] = None
    target_row: Optional[int] = None
    hook_size: Optional[str] = Field(None, max_length=20)
    timer_seconds: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    started_at: datetime
    last_worked: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
