from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from common.database import get_db  
from common.apiResponse import CommonResponse
from domain.music.music_controller import MusicService
from domain.music.music_schemas import RecommendationResponse, MusicRecommendRequest

router = APIRouter(
    prefix="/music",
    tags=["Music"]
)

@router.post("/recommend", response_model=CommonResponse[RecommendationResponse], status_code=status.HTTP_200_OK)
def recommend_music(
    request: MusicRecommendRequest,
    db: Session = Depends(get_db)
):
    """
    사용자의 기분(mood)을 쿼리 파라미터로 받아 노래를 추천.
    ex) /music/recommend?mood=이별
    """
    music_service = MusicService(db)
    
    songs = music_service.recommend_songs(request)
    
    # 결과가 없으면 랜덤 추천
    if not songs:
        random_song = music_service.get_random_song()
        result_data = RecommendationResponse(
            message=f"'{request.mood}'에 딱 맞는 곡을 못 찾았어요😢 대신 이 곡은 어때요?",
            count=1 if random_song else 0,
            data=[random_song] if random_song else []
        )
        return CommonResponse.success_response(message="recommend_music_success", result=result_data)
    
    result_data = RecommendationResponse(
        message=f"'{request.mood}' 분위기에 어울리는 노래들입니다.",
        count=len(songs),
        data=songs
    )
    return CommonResponse.success_response(message="recommend_music_success", result=result_data)