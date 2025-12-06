from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Entity 역할
class AuthorModel(BaseModel):
    userId : int
    nickname : str
    
class CommentModel(BaseModel):
    id : int
    author : AuthorModel
    postId : int
    content : str
    createdAt : datetime
  
# DTO 역할(Pydantic Model 정의)
# 댓글
class CommentCreateRequest(BaseModel):
    content : str
    
class CommentCreateResponse(BaseModel):
    postId : int
    commentId : int
    content : str
    author: AuthorModel
    createdAt: datetime
    
class CommentUpdateRequest(BaseModel):
    content : Optional[str]
    
class CommentUpdateResponse(BaseModel):
    commentId : int
    content : str  
    
class CommentDeleteResponse(BaseModel):
    commentId : int
    isDeleted : bool