from fastapi import APIRouter, status, Path, Depends
from common.dependencies import get_current_user_id
from common.apiResponse import CommonResponse
from typing import Dict, Any, List
from . import likes_controller
from . import likes_schemas

router = APIRouter(
    prefix="/posts/{post_id}/likes",
    tags=["좋아요"]
)

@router.post("/", response_model=CommonResponse[likes_schemas.LikesModel], status_code=status.HTTP_201_CREATED)
async def create_likes(
    post_id : int = Path(..., gt=0, description="좋아요를 등록할 게시글 아이디"),
    user_id : int = Depends(get_current_user_id)
) -> CommonResponse[Dict[str,Any]]:
    result = likes_controller.create_likes(user_id=user_id, post_id=post_id)
    
    return CommonResponse.success_response(
        message="likes_register_success",
        result=result
    )