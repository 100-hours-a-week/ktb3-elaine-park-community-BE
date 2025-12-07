from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base

class Likes(Base):
    __tablename__ = "likes"
    
    likesId = Column(Integer, primary_key=True, index=True)
    
    postId = Column(Integer, ForeignKey("posts.postId"), nullable=False, ondelete="CASCADE")
    post = relationship("Post", back_populates="likes")
    
    userId = Column(Integer, ForeignKey("users.userId"), nullable=False, ondelete="CASCADE")
    author = relationship("User")
    