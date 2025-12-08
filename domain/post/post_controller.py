from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Dict, Any, List, Optional
from . import post_schemas
from common.exceptions.customException import (
    InvalidLengthException, PostNotFoundException,
    UnauthorizedException
)
from datetime import datetime
from . import post_model, post_schemas
    
def create_post(db: Session, request: post_schemas.PostCreateReqest, user_id : int) -> Dict[str, Any]:
        
    if len(request.title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")
    
    new_post = post_model.Post(
        userId = user_id,
        title = request.title,
        content = request.content,
        imageId = request.imageId,
        viewsCnt = 0,
        commentsCnt = 0,
        likesCnt = 0,
        comments = []    
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
        
    return new_post

def update_post(db: Session, request: post_schemas.PostUpdateRequest, post_id : int, user_id : int):
    if request.title is not None and len(request.title) > 26:
        raise InvalidLengthException("제목의 길이는 26자를 초과할 수 없습니다.")

    post_found = db.query(post_model.Post).filter(post_model.Post.postId == post_id).first()
    
    if not post_found:
        raise PostNotFoundException
    if post_found.userId != user_id:
        raise UnauthorizedException    
    
    if request.title is not None:
        post_found.title = request.title
        
    if request.content is not None:
        post_found.content = request.content
        
    if request.imageId is not None:
        post_found.imageId = request.imageId
    
    db.commit()
    
    return post_found

def delete_post(db: Session, post_id : int, user_id : int):
    post_found = db.query(post_model.Post).filter(post_model.Post.postId == post_id).first()
    
    if not post_found:
        raise PostNotFoundException
    
    if post_found.userId != user_id:
        raise UnauthorizedException("본인의 게시글만 삭제할 수 있습니다.")
    
    db.delete(post_found)
    db.commit()
    
    delete_post = {
        "postId" : post_id,
        "isDeleted" : True
    }
    
    return delete_post

def get_post_list(db: Session, page : int, limit : int):
    offset = page * limit #0 페이지부터 시작  
    
    # 최신순 정렬
    posts = db.query(post_model.Post)\
        .order_by(desc(post_model.Post.postId))\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    response_list = []
        
    for post in posts:
        item = {
            "postId" : post.postId,
            "userId" : post.userId,
            "title" : post.title,
            "likesCnt" : post.likesCnt,
            "commentsCnt" : post.commentsCnt,
            "viewsCnt" : post.viewsCnt,
            "createdAt" : post.createdAt,
            "profileImageId" : post.author.profileImageId if post.author else None
        }
        response_list.append(item)
        
    return response_list
    
def read_detail_post(db: Session, post_id : int):
    found_post = db.query(post_model.Post).filter(post_model.Post.postId == post_id).first()

    if not found_post:
        raise PostNotFoundException("상세조회 할 게시글 아이디를 찾을 수 없습니다.")
    
    found_post.viewsCnt += 1
    db.commit()
    
    author_nickname = found_post.author.nickname if found_post.author else "Unknown"
    author_profile_img = found_post.author.profileImageId if found_post.author else None
    
    comment_list = []
    for comment in found_post.comments:
        writer_name = comment.author.nickname if comment.author else "Unknown"
        
        comment_item = {
            "commentId" : comment.commentId,
            "content" : comment.content,
            "userId" : comment.userId,
            "writer" : writer_name,
            "createdAt" : comment.createdAt,
        } 
        comment_list.append(comment_item)
            
    detail_post = {
        "postId" : found_post.postId,
        "title" : found_post.title,
        "content" : found_post.content,
        "author" : {
            "userId" : found_post.userId,
            "nickname" : author_nickname,
            "profileImageId" : author_profile_img
        },
        "createdAt" : found_post.createdAt,
        "contentImageId" : found_post.imageId,
        "likesCnt" : found_post.likesCnt,
        "viewsCnt" : found_post.viewsCnt,
        "commentCnt" : len(comment_list),
        "comments" : comment_list
    }
    
    return detail_post