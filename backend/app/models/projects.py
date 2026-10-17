from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class Project(Base):
    __tablename__ = "projects"


    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), nullable=False)
    status = Column(String(30), nullable=True)
    current_row = Column(Integer, nullable=True, default=0)
    target_row = Column(Integer, nullable=True)
    hook_size = Column(String(20), nullable=True)
    timer_seconds = Column(Integer, nullable=True, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_worked = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)