from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from common.security import get_password_hash, verify_password, create_access_token
from common.exceptions.customException import AlreadyEmailException, InvalidIdPasswordException, UnauthorizedException, UserNotFoundException
from . import user_schemas, user_model

def sign_up(db : Session, request: user_schemas.UserSignUpRequest):        
    existing_user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    
    if existing_user:
        raise AlreadyEmailException
    
    hashed_pw = get_password_hash(request.password)
    
    new_user = user_model.User(
        email = request.email,
        password = hashed_pw,
        nickname = request.nickname,
        profileImageId = request.profileImageId
    )
    db.add(new_user)
    db.commit() # 확정 -> 이때 userId 자동 생성
    db.refresh(new_user)
    
    return new_user

def login(db: Session, request : user_schemas.UserLoginRequest) :
    user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    
    if not user:
        raise UserNotFoundException
    
    if not verify_password(request.password, user.password):
        raise InvalidIdPasswordException
        
    access_token = create_access_token(data={"sub" : str(user.userId)})
    
    return{
        "accessToken" : access_token,
        "tokenType" : "Bearer"
    }

def updateInfo(db: Session, request : user_schemas.UserUpdateRequest, user_id : int):
    user_found = db.query(user_model.User).filter(user_model.User.userId == user_id).first()
    
    if not user_found:
        raise UnauthorizedException
    
    if request.nickname is not None:
        user_found.nickname = request.nickname
        
    if request.profileImageId is not None:
        user_found.profileImageId = request.profileImageId
        
    db.commit() #⭐️⭐️⭐️

    return{
        "userId" : user_found.userId,
        "isUpdated" : True
    }
    
def update_password(db:Session, request : user_schemas.PasswordUpdateRequest, user_id : int) -> Dict[str, Any]:
    user_found = db.query(user_model.User).filter(user_model.User.userId == user_id).first()
    if not user_found:
        raise UnauthorizedException
    
    hashed_new_pw = get_password_hash(request.newPassword)
    
    user_found.password = hashed_new_pw
    
    db.commit()
    
    return {"userId" : user_id, "isUpdated" : True}

def read_user_info(db: Session, user_id : int) -> Dict[str, Any]:
    user_found = db.query(user_model.User).filter(user_model.User.userId == user_id).first()
    
    if not user_found:
        raise UnauthorizedException

    response_data = {
        "email" : user_found.email,
        "nickname" : user_found.nickname,
        "profileImageId" : user_found.profileImageId
    }
    return response_data
    
def delete_user(db: Session, user_id : int) -> Dict[str, Any]:
    user_found = db.query(user_model.User).filter(user_model.User.userId == user_id).first()
    
    if not user_found:
        raise UnauthorizedException
    
    db.delete(user_found)
    db.commit()
    
    response = {
        "userId" : user_id,
        "isDeleted" : True
    }
    return response
