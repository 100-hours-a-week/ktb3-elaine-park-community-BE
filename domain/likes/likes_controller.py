from typing import Dict, Any, Optional
from common.exceptions.customException import(
    PostNotFoundException, UnauthorizedException
)
from common.apiResponse import CommonResponse
from common.database import USER_DB, POST_DB, COMMENT_DB, NEXT_LIKES_ID
from . import likes_schemas

def create_likes(user_id : int, post_id: int) -> Dict[str, Any]:
    global NEXT_LIKES_ID
    
    found_index = -1
    for i, post in enumerate(POST_DB):
        if post["id"] == post_id:
            found_index = i
            break
    if found_index == -1:
        raise PostNotFoundException("좋아요 등록할 게시글을 찾을 수 없습니다.")
    
    post = POST_DB[found_index]

    post["likesCnt"] += 1
    
    created_likes = {
        "id" : NEXT_LIKES_ID,
        "post_id" : post["id"],
        "user_id" : user_id,
        "likesCnt" : post["likesCnt"]
    }
    
    return created_likes
