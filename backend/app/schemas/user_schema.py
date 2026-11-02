from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime 

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    password_hash: str = Field(..., max_length=255)
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
