from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from common.database import Base

class Image(Base):
    __tablename__ = "images"
    
    imageId = Column(Integer, primary_key=True, index=True)
    originalName = Column(String, nullable=False)
    storedName = Column(String, nullable=False)
    url = Column(String, nullable=False)
    
    createdAt = Column(DateTime, default=func.now())