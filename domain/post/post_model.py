from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from common.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    postId = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    imageId = Column(Integer, nullable=True)
    viewsCnt = Column(Integer, default=0)
    likesCnt = Column(Integer, default=0)
    commentsCnt = Column(Integer, default=0)

    # 외래키 설정
    userId = Column(Integer, ForeignKey("users.userId"), nullable=False, ondelete="CASCADE")
    
    author = relationship("User", back_populates="posts")
    
    comments = relationship("Comment", back_populates="post")
    
    likes = relationship("Likes", back_populates="post")
    
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    