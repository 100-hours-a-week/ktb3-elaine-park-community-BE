from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from domain.comment.comment_schemas import CommentModel
from common.apiResponse import CommonResponse

#Entity 역할
class PostModel(BaseModel):
    postId : int
    userId : int
    title : str
    content : str
    imageId : Optional[int] = 0
    createdAt : datetime
    updatedAt : datetime
    likesCnt : Optional[int] = 0
    viewsCnt : Optional[int] = 0
    commentCnt : Optional[int] = 0
    comments : Optional[list[CommentModel]] = []
    
# DTO 역할(Pydantic Model 정의)
# 게시글
class PostCreateReqest(BaseModel):
    title : str
    content : str
    imageId : int = 0

class PostUpdateRequest(BaseModel):
    title: Optional[str] = None
    content : Optional[str] = None
    imageId : Optional[int] = None
    
class PostUpdateResponse(BaseModel):
    postId : int
    title : str
    content : str
    imageId : int
    
class PostDeleteResponse(BaseModel):
    postId : int
    isDeleted : bool

class PostAuthorDetail(BaseModel):
    userId : int
    nickname : str
    profileImageId : int  
    
class PostReadDetailResponse(BaseModel):
    postId : int
    title : str
    content : str
    author : PostAuthorDetail
    createdAt : datetime
    contentImageId : int
    likesCnt : int = 0
    viewsCnt : int = 0
    commentCnt : int = 0
    comments : List[CommentModel]
    
class PostListReadResponse(BaseModel):
    postId : int
    userId : int
    title : str
    likesCnt : int
    commentsCnt : int
    viewsCnt : int
    createdAt : datetime
    profileImageId : Optional[int]=None

class PostListResponseWrapper(CommonResponse[List[PostListReadResponse]]):
    pass