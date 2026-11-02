from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime 

class MuseumListingBase(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=255)
    recipe_snapshot: Optional[Dict[str, Any]] = None # Handles JSONB data as a dictionary

class MuseumListingCreate(MuseumListingBase):
    pass

class MuseumListingUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    recipe_snapshot: Optional[Dict[str, Any]] = None

class MuseumListingResponse(MuseumListingBase):
    id: int
    project_id: int
    user_id: int
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)