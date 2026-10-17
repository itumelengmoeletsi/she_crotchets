from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database.database import Base

class MuseumListing(Base):
    __tablename__ = "museum_listings"

    id = Column(Integer, primary_key=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title= Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    recipe_snapshot = Column(JSONB, nullable=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now())