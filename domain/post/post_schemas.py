from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from domain.comment.comment_schemas import CommentModel

#Entity 역할
class PostModel(BaseModel):
    id : int
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
    id : int
    title : str
    content : str
    imageId : int
    
class PostDeleteResponse(BaseModel):
    postId : int
    isDeleted : bool

class PostAuthorDetail(BaseModel):
    userId : int
    nickname : str
    profileImage : str  
    
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
    likes : int
    comment : int
    views : int
    createdAt : datetime
    profileImage : str