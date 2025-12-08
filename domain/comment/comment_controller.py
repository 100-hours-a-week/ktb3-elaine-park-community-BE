from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from common.exceptions.customException import (
    PostNotFoundException, CommentNotFoundException, 
    UnauthorizedException, UnMatchedPostCommentException,
    UserNotFoundException
    )
from datetime import datetime
from . import comment_model, comment_schemas
from domain.post import post_model

def create_comment(db: Session, user_id: int, post_id : int, content : str):
    post_exists = db.query(post_model.Post).filter(post_model.Post.postId == post_id).first()
        
    if not post_exists:
        raise PostNotFoundException("댓글 생성할 게시글을 찾을 수 없습니다.")
    
    new_comment = comment_model.Comment(
        userId = user_id,
        postId = post_id,
        content = content
    )
    
    post_exists.commentsCnt += 1
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

def update_comment(db: Session, user_id: int, post_id : int, comment_id : int, content: str):
    comment_found = db.query(comment_model.Comment).filter(comment_model.Comment.commentId == comment_id).first()
    
    if not comment_found:
        raise CommentNotFoundException
    
    if comment_found.postId != post_id:
        raise CommentNotFoundException
    
    if comment_found.userId != user_id:
        raise UnauthorizedException
    
    if content is not None:
        comment_found.content = content
    
    db.commit()
    
    return comment_found
    
def delete_comment(db: Session, user_id : int, post_id : int, comment_id : int):
    comment_found = db.query(comment_model.Comment).filter(comment_model.Comment.commentId == comment_id).first()
    
    if not comment_found:
        raise CommentNotFoundException
    
    if comment_found.postId != post_id:
        raise CommentNotFoundException("해당 게시글에 존재하지 않는 댓글입니다.")
    
    if comment_found.userId != user_id:
        raise UnauthorizedException
    
    if comment_found.post:
        comment_found.post.commentsCnt -= 1
        
    db.delete(comment_found)
    db.commit()
    
    deleted_comment = {
        "commentId" : comment_id,
        "isDeleted" : True
    }
    return deleted_comment
         