from fastapi import APIRouter,status, Path
from pydantic import BaseModel
from common.apiResponse import CommonResponse
from . import post_controller
from typing import Dict, Any, List

router = APIRouter(
    prefix="/posts",
    tags=["게시글"],
)

# DTO 역할(Pydantic Model 정의)
class PostCreateReqest(BaseModel):
    title : str
    content : str
    imageId : int = 0
    
class PostCreateResponse(BaseModel):
    postId : int
    title : str
    content : str
    imageId : int

    
@router.post("/", response_model=CommonResponse[PostCreateResponse], status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreateReqest) -> CommonResponse[Dict[str, Any]]:
    new_post = post_controller.create_post(
        title=post.title,
        content=post.content,
        image_id=post.imageId
    )
    
    return CommonResponse.success_response(message="게시글이 성공적으로 등록되었습니다.", result=new_post)
