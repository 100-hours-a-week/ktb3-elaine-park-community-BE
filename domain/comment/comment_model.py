from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base

class Comment(Base):
    __tablename__ = "comments"
    
    commentId = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False)
    author = relationship("User")
    
    postId = Column(Integer, ForeignKey("posts.postId", ondelete="CASCADE"), nullable=False)
    post = relationship("Post", back_populates="comments")
    