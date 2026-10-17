from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.sql import func
from app.database.database import Base

class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"

    id = Column(Integer, primary_key=True, nullable=False)
    museum_item_id = Column(Integer, ForeignKey("museum_listings.id"), nullable=False, unique=True)
    price = Column(Numeric(10,2), nullable=False)
    listing_type = Column(String(30), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())