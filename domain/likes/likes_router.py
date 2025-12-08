from fastapi import APIRouter, status, Path, Depends
from sqlalchemy.orm import Session
from common.dependencies import get_current_user_id
from common.database import get_db
from common.apiResponse import CommonResponse
from typing import Dict, Any, List
from . import likes_controller
from . import likes_schemas

router = APIRouter(
    prefix="/posts/{post_id}/likes",
    tags=["좋아요"]
)

@router.post("/", response_model=CommonResponse[likes_schemas.LikesResponse], status_code=status.HTTP_201_CREATED)
async def create_likes(
    post_id : int = Path(..., gt=0, description="좋아요를 등록할 게시글 아이디"),
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
) -> CommonResponse[Dict[str,Any]]:
    result = likes_controller.togle_likes(db, user_id, post_id)
    
    return CommonResponse.success_response(
        message="likes_register_success",
        result=result
    )