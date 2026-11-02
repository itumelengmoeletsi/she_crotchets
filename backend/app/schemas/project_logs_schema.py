from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime 

class ProjectLogsBase(BaseModel):
    row_number: int
    photo_url: str = Field(..., max_length=500)

class ProjectLogsCreate(BaseModel):
    pass

class ProjectLogsUpdate(BaseModel):
    row_number: Optional[int]
    note_text: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(..., max_length=500)

class ProjectLogsResponse(ProjectLogsBase):
    id: int
    project_id: int
    note_text: Optional[str] = None
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)
