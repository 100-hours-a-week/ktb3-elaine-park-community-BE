from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from common.apiResponse import CommonResponse
from common.dependencies import get_current_user_id
from common.database import get_db
from . import comment_controller
from . import comment_schemas

router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["댓글"]
)

@router.post("", response_model=CommonResponse[comment_schemas.CommentCreateResponse], status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment : comment_schemas.CommentCreateRequest,
    post_id : int = Path(..., gt=0, description="댓글 생성할 게시글의 아이디"),
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
)-> CommonResponse[Dict[str, Any]]:
    new_comment = comment_controller.create_comment(
        db = db,
        user_id = user_id,
        post_id=post_id,
        content = comment.content
    )
    
    return CommonResponse.success_response(message="comment_create_success", result=new_comment)

@router.patch("/{comment_id}", response_model=CommonResponse[comment_schemas.CommentUpdateResponse], status_code=status.HTTP_200_OK)
async def update_comment(
    comment : comment_schemas.CommentUpdateRequest,
    post_id : int = Path(..., gt=0, description="댓글 수정할 게시글의 아이디"),
    comment_id : int = Path(..., gt=0, description="수정할 댓글 아이디"),
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
)-> CommonResponse[Dict[str, Any]]:
    updated_comment = comment_controller.update_comment(
        db = db,
        user_id=user_id,
        post_id=post_id,
        comment_id=comment_id,
        content=comment.content
    )
    result = {
        "commentId" : updated_comment.commentId,
        "content" : updated_comment.content
    } 
    return CommonResponse.success_response(message="comment_update_success", result=result)    

@router.delete("/{comment_id}", response_model=CommonResponse[comment_schemas.CommentDeleteResponse], status_code=status.HTTP_200_OK)
async def delete_comment(
    post_id : int = Path(..., gt=0, description="삭제할 댓글의 게시글 아이디"),
    comment_id : int = Path(..., gt=0, description="삭제할 댓글 아이디"),
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
):
    deleted_comment = comment_controller.delete_comment(
        db=db,
        user_id = user_id,
        post_id = post_id, 
        comment_id = comment_id
    )       
    return CommonResponse.success_response(message="comment_delete_success", result=deleted_comment)