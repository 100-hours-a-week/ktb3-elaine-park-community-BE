from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from common.database import Base

class User(Base):
    __tablename__ = "users" # db에 저장될 실제 테이블 이름
    
    userId = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    
    profileImageId = Column(Integer, nullable=True)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Likes", back_populates="author", cascade="all, delete-orphan")
    
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())