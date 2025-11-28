from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from common.apiResponse import CommonResponse
from fastapi.requests import Request
from common.exceptions.customException import FieldRequiredException, InvalidLengthException
from common.exceptions.BaseException import UnicornException
from common.exceptions.handlers import unicorn_exception_handler
from typing import Dict, Any, List

app = FastAPI(title="커뮤니티 백엔드 (Route 단독)")

app.add_exception_handler(UnicornException, unicorn_exception_handler) # 커스텀 핸들러 등록

# DB 역할
DUMMY_DB : List[Dict[str, Any]] = [
    {"postId" : 1, "title" : "제목1", "content" : "내용1", "imageId": 1},
    {"postId" : 2, "title" : "제목2", "content" : "내용2", "imageId": 0},
]
NEXT_ID = 3

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

# Router + Controller 역할
@app.post('/posts', response_model=CommonResponse[PostCreateResponse], status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreateReqest) -> CommonResponse[Dict[str, Any]]:
    global DUMMY_DB, NEXT_ID
        
    if not post.title or len(post.title.strip()) == 0:
        raise FieldRequiredException("제목은 필수 입력 사항입니다.")
        
    if len(post.title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")
    
    newPost = {
        "postId" : NEXT_ID,
        "title" : post.title,
        "content" : post.content,
        "imageId" : post.imageId
    }
    DUMMY_DB.append(newPost)
    NEXT_ID += 1
    
    return CommonResponse.success_response(message="게시글이 성공적으로 등록되었습니다.", result=newPost)

