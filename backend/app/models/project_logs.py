from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.database import Base

class ProjectLog(Base):
    __tablename__ = "project_logs"

    id = Column(Integer, primary_key=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False) # ON DELETE CASCADE
    row_number = Column(Integer, nullable=False)
    note_text = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=False)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())