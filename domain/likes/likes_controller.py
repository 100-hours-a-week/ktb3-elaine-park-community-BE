from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from common.exceptions.customException import(
    PostNotFoundException, UnauthorizedException
)
from common.apiResponse import CommonResponse
from . import likes_model
from domain.post import post_model

def togle_likes(db: Session, user_id : int, post_id: int):
    post = db.query(post_model.Post).filter(post_model.Post.postId == post_id).first()
    
    if not post:
        raise PostNotFoundException
    
    found_index = -1
    existing_like = db.query(likes_model.Likes).filter(
        likes_model.Likes.userId == user_id,
        likes_model.Likes.postId == post_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        post.likesCnt -= 1
        message = "likes_cancel"
    else:
        new_like = likes_model.Likes(userId=user_id, postId = post_id)
        db.add(new_like)
        post.likesCnt += 1
        message = "likes_register"
    
    db.commit()
    
    return {"flag" : message, "likesCnt": post.likesCnt}
