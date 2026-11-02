from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class YarnStashBase(BaseModel):
    brand: str = Field(..., max_length=255)
    colorway: str = Field(..., max_length=100)
    weight_class: str = Field(..., max_length=50)
    fibre_content: str = Field(..., max_length=100)
    skein_count: int = 1

class YarnStashCreate(YarnStashBase):
    pass

class YarnStashUpdate(BaseModel):
    brand: Optional[str] = Field(None, max_length=255)
    colorway: Optional[str] = Field(None, max_length=100)
    weight_class: Optional[str] = Field(None, max_length=50)
    fibre_content: Optional[str] = Field(None, max_length=100)
    skein_count: Optional[int] = None

class YarnStashResponse(YarnStashBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)