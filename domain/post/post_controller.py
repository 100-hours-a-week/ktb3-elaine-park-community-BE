from typing import Dict, Any, List, Optional
from . import post_schemas
from common.exceptions.customException import (
    InvalidLengthException, PostNotFoundException,
    UnauthorizedException
)
from datetime import datetime
from common.database import USER_DB, POST_DB, COMMENT_DB, NEXT_POST_ID
    
    
def create_post(user_id : int, title: str, content: str, image_id : int) -> Dict[str, Any]:
    global NEXT_POST_ID
        
    if len(title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")
    
    new_post = {
        "id" : NEXT_POST_ID,
        "userId" : user_id,
        "title" : title,
        "content" : content,
        "imageId" : image_id,
        "createdAt" : datetime.now(),
        "updatedAt" : datetime.now(),
        "likesCnt": 0,
        "viewsCnt": 0,
        "commentCnt": 0,
        "comments": []    
    }
    
    POST_DB.append(new_post)
    NEXT_POST_ID += 1
    
    return new_post

def update_post(post_id: int, user_id : int,  title: str, content: str, image_id: int) -> Dict[str, Any]:
    if title is not None and len(title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")

    found_index = -1
    for i, post in enumerate(POST_DB):
        if post["id"] == post_id:
            found_index = i
            break
    
    if found_index == -1:
        raise PostNotFoundException("수정할 게시글 아이디를 찾을 수 없습니다.")
    
    existing_post = POST_DB[found_index]
    
    if existing_post["userId"] != user_id:
        raise UnauthorizedException("본인의 게시글만 수정할 수 있습니다.")
    
    existing_post["title"] = title if title is not None else existing_post["title"]
    existing_post["content"] = content if content is not None else existing_post["content"]
    existing_post["imageId"] = image_id if image_id is not None else existing_post["imageId"]
    existing_post["updatedAt"] = datetime.now()
    
    POST_DB[found_index] = existing_post
    return existing_post

def delete_post(post_id : int, user_id : int):
    found_index = -1
    for i, post in enumerate(POST_DB):
        if post["id"] == post_id:
            found_index = i
            break
    if found_index == -1:
        raise PostNotFoundException("삭제할 게시글 아이디를 찾을 수 없습니다.")
    
    existing_post = POST_DB[found_index]
    
    if existing_post["userId"] != user_id:
        raise UnauthorizedException("본인의 게시글만 삭제할 수 있습니다.")
    
    POST_DB.pop(found_index)
    
    delete_post = {
        "postId" : i,
        "isDeleted" : True
    }
    return delete_post

def get_post_list(offset : int, limit : int) -> dict:
    # 최신순 정렬
    sorted_posts = sorted(POST_DB, key=lambda x:x["id"], reverse=True)
    
    # 페이징 처리
    paginated_posts = sorted_posts[offset : offset + limit]
    
    response_list = []
        
    for post in paginated_posts:
        item = {
            "postId" : post["id"],
            "userId" : post["userId"],
            "title" : post["title"],
            "likes" : post.get("likesCnt", 0),
            "comment" : post.get("commentCnt", 0),
            "views" : post.get("viewsCnt", 0),
            "createdAt" : post["createdAt"],
            "profileImage" : "https://example.com/default_profile.png"
        }
        response_list.append(item)
        
    return response_list
    
def read_detail_post(post_id : int):
    
    found_post = next((p for p in POST_DB if p["id"] == post_id), None)
    if not found_post:
        raise PostNotFoundException("상세조회 할 게시글 아이디를 찾을 수 없습니다.")
    
    found_post["viewsCnt"] += 1
    
    post_author_id = found_post["userId"]
    author_info = next((u for u in USER_DB if u["userId"] == post_author_id), None)
    
    if author_info:
        nickname = author_info["nickname"]
    else:
        nickname = "Unknown"
    
    comments = [c for c in COMMENT_DB if c["postId"] == post_id]   
     
    detail_post = {
        "postId" : found_post["id"],
        "title" : found_post["title"],
        "content" : found_post["content"],
        "author" : {
            "userId" : post_author_id,
            "nickname" : nickname,
            "profileImage" : "default.png"
        },
        "createdAt" : found_post["createdAt"],
        "contentImage" : found_post["imageId"],
        "likesCnt" : found_post.get("likesCnt", 0),
        "viewsCnt" : found_post["viewsCnt"],
        "commentCnt" : len(comments),
        "comments" : comments
    }
    
    return detail_post