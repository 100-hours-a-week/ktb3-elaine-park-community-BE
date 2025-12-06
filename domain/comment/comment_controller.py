from typing import Dict, Any, List, Optional
from common.exceptions.customException import (
    PostNotFoundException, CommentNotFoundException, 
    UnauthorizedException, UnMatchedPostCommentException,
    UserNotFoundException
    )
from datetime import datetime
from common.database import USER_DB, POST_DB, COMMENT_DB, NEXT_COMMENT_ID

def create_comment(user_id: int, post_id : int, content : str) -> Dict[str, Any]:
    global NEXT_COMMENT_ID
    
    post_exists = any(post["id"] == post_id for post in POST_DB)
        
    if not post_exists:
        raise PostNotFoundException("댓글 생성할 게시글을 찾을 수 없습니다.")
    
    user_info = next((u for u in USER_DB if u["userId"] == user_id), None)
    if not user_info:
        raise UserNotFoundException
    
    author_data = {
        "userId" : user_id,
        "nickname" : user_info["nickname"]
    }
    
    new_comment = {
        "commentId" : NEXT_COMMENT_ID,
        "author" : author_data,
        "postId" : post_id,
        "content" : content,
        "createdAt" : datetime.now()
    }
    
    COMMENT_DB.append(new_comment)
    NEXT_COMMENT_ID += 1
    
    return new_comment

def update_comment(user_id: int, post_id : int, comment_id : int, content: str) -> Dict[str, Any]:
    found_index = -1
    for i, comment in enumerate(COMMENT_DB):
        if comment["id"] == comment_id:
            found_index = i
            break
    if found_index == -1:
        raise CommentNotFoundException("해당 댓글을 찾을 수 없습니다.")
    
    existing_comment = COMMENT_DB[found_index]

    if existing_comment["author"]["userId"] != user_id:
        raise UnauthorizedException("해당 권한을 사용할 수 없습니다.")
    
    existing_comment["content"] = content if content is not None else existing_comment["content"]
    
    updated_comment = {
        "id" : comment_id,
        "author" :{
            "userId" : user_id,
            "nickname" : existing_comment["author"]["nickname"]
        },
        "postId": existing_comment["postId"],
        "content" : existing_comment["content"],
        "createdAt" : existing_comment["createdAt"]
    }
    
    return updated_comment
    
def delete_comment(post_id : int, comment_id : int, user_id : int) -> Dict[str, Any]:
    found_index = -1
    for i, comment in enumerate(COMMENT_DB):
        if comment["id"] == comment_id:
            found_index = i
            break
    if found_index == -1:
        raise CommentNotFoundException("해당 댓글을 찾을 수 없습니다.")
    
    comment = COMMENT_DB[found_index]

    if comment["user_Id"] != user_id:
        raise UnauthorizedException("본인의 댓글만 삭제할 수 있습니다.")
       
    COMMENT_DB.pop(found_index)
    
    deleted_comment = {
        "commentId" : found_index,
        "isDeleted" : True
    }
    return deleted_comment
         