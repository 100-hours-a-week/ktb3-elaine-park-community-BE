from pydantic import BaseModel, Field
from typing import List, Optional
from common.apiResponse import CommonResponse

class SongBase(BaseModel):
    title: str
    artist: str
    genre: str
    description: str
    # albumImage 등 필요한 필드 추가 예정

class SongResponse(SongBase):
    songId: int

    class Config:
        # ORM 객체(SQLAlchemy)를 Pydantic 모델로 변환할 수 있게 허용
        from_attributes = True 

# 추천 결과 전체를 감싸는 응답 스키마
class RecommendationResponse(BaseModel):
    message: str
    count: int
    data: List[SongResponse] 
    
class MusicRecommendRequest(BaseModel):
    mood: str = Field(..., description="사용자의 현재 기분(예: 우울, 신남)")