from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from common.database import Base  

class Song(Base):
    __tablename__ = "songs" 

    songId = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), nullable=False)   # 노래 제목
    artist = Column(String(255), nullable=False)  # 가수
    genre = Column(String(100), nullable=False)   # 장르
    
    description = Column(Text, nullable=True) 
    
    # 나중에 앨범 커버 이미지 URL 등이 필요할 수 있음
    albumImage = Column(String(255), nullable=True)

    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())