from fastapi import APIRouter,status, Path, Query, Depends
from common.dependencies import get_current_user_id
from common.apiResponse import CommonResponse
from . import post_controller
from typing import Dict, Any, List
from . import post_schemas

router = APIRouter(
    prefix="/posts",
    tags=["게시글"],
)
    
@router.post("/", response_model=CommonResponse[post_schemas.PostModel], status_code=status.HTTP_201_CREATED)
async def create_post(
    post: post_schemas.PostCreateReqest,
    user_id : int = Depends(get_current_user_id)
    ) -> CommonResponse[Dict[str, Any]]:
    new_post = post_controller.create_post(
        user_id=user_id,
        title=post.title,
        content=post.content,
        image_id=post.imageId
    )
    
    return CommonResponse.success_response(message="post_create_success", result=new_post)

@router.patch("/{post_id}", response_model=CommonResponse[post_schemas.PostUpdateResponse], status_code=status.HTTP_200_OK)
async def update_post(
    post: post_schemas.PostUpdateRequest,
    post_id : int = Path(..., gt=0, description="수정할 게시글의 아이디"),
    user_id : int = Depends(get_current_user_id)
) -> CommonResponse[Dict[str, Any]]:
     updated_post = post_controller.update_post(
         post_id = post_id,
         user_id = user_id,
         title=post.title,
         content=post.content,
         image_id=post.imageId,
     )
     return CommonResponse.success_response(message="update_post_success", result= updated_post)
 
@router.delete("/{post_id}", response_model=CommonResponse[post_schemas.PostDeleteResponse], status_code=status.HTTP_200_OK)
async def delete_post(
    post_id : int = Path(..., gt=0, description="삭제할 게시글의 아이디"),
    user_id : int = Depends(get_current_user_id)
 ) -> CommonResponse[Dict[str, Any]]:
    is_deleted = post_controller.delete_post(post_id, user_id)
    return CommonResponse.success_response(message="delete_post_success", result= is_deleted)

@router.get("/{post_id}", response_model=CommonResponse[post_schemas.PostReadDetailResponse], status_code=status.HTTP_200_OK)
async def read_detail_post(
    post_id : int = Path(..., gt=0, description="상세조회할 게시글 아이디")
)-> CommonResponse[Dict[str, Any]]:
    detail_post = post_controller.read_detail_post(
        post_id=post_id
    )
    return CommonResponse.success_response(message="post_read_success", result=detail_post)

@router.get("/", response_model=CommonResponse[List[post_schemas.PostListReadResponse]], status_code=status.HTTP_200_OK)
async def read_list_post(
    offset : int = Query(0, ge=0, description="시작 인덱스(0부터)"),
    limit : int = Query(10, gt=0, le=100, description="한 번에 가져올 개수")
) -> CommonResponse[List[post_schemas.PostListReadResponse]]:
    result = post_controller.get_post_list(offset, limit)
    
    return CommonResponse.success_response(message="post_list_success", result=result)