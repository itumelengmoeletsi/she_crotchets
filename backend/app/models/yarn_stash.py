from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func 
from app.database.database import Base

class YarnStash(Base):
    __tablename__ = "yarn_stash"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    brand = Column(String(255), nulllable=False)
    colorway = Column(String(100), nullable=False)
    weight_class = Column(String(50), nullable=False)
    fiber_content = Column(String(100), nullable=False)
    skein_count = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
