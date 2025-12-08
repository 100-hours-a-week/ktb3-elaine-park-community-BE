from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base

class Likes(Base):
    __tablename__ = "likes"
    
    likesId = Column(Integer, primary_key=True, index=True)
    
    postId = Column(Integer, ForeignKey("posts.postId", ondelete="CASCADE"), nullable=False)
    post = relationship("Post", back_populates="likes")
    
    userId = Column(Integer, ForeignKey("users.userId", ondelete="CASCADE"), nullable=False)
    author = relationship("User")
    