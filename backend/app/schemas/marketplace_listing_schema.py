from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime 
from decimal import Decimal

class MarketplaceListingBase(BaseModel):
    price: Decimal = Field(..., ge=0, decimal_places=2)
    listing_type: str = Field(..., max_length=30)
    is_active: bool = True

class MarketplaceListingCreate(MarketplaceListingBase):
    pass

class MarketplaceListingUpdate(BaseModel):
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    listing_type: Optional[str] = Field(None, max_length=30)
    is_active: Optional[bool] = None

class MarketplaceListingResponse(MarketplaceListingBase):
    id: int
    museum_item_id: int
    created_at: datetime

    model_condig = ConfigDict(from_attributes=True)
