from typing import Dict, Any, List, Optional
from datetime import datetime
from common.security import get_password_hash, verify_password, create_access_token
from common.exceptions.customException import AlreadyEmailException, InvalidIdPasswordException, UnauthorizedException
from . import user_schemas

USER_DB : List[Dict[str, Any]] = []
NEXT_USER_ID = 1

def sign_up(request: user_schemas.UserSignUpRequest) -> Dict[str, Any]:    
    global NEXT_USER_ID
    
    for user in USER_DB:
        if user["emal"] == request.email:
            raise AlreadyEmailException("이미 존재하는 이메일입니다.")
    
    hashed_pw = get_password_hash(request.password)
    
    new_user = {
        "userId" : NEXT_USER_ID,
        "email" : request.email,
        "password" : hashed_pw,
        "nickname" : request.nickname,
        "profileImageId" : request.profileImageId,
        "createdAt" : datetime.now()
    }
    
    USER_DB.append(new_user)
    NEXT_USER_ID += 1
    
    return{
        "userId": new_user["userId"],
        "email": new_user["email"],
        "nickname": new_user["nickname"],
        "profileImageId": new_user["profileImageId"]       
    }

def login(request : user_schemas.UserLoginRequest) -> Dict[str, Any]:
    user_found = None
    for user in USER_DB:
        if user["email"] == request.email:
            user_found = user
            break
        
    if not user_found:
        raise InvalidIdPasswordException
    
    if not verify_password(request.password, user_found["password"]):
        raise InvalidIdPasswordException
        
    access_token = create_access_token(data={"sub" : str(user_found["userId"])})
    
    return{
        "accessToken" : access_token,
        "tokenType" : "Bearer"
    }

def updateInfo(request : user_schemas.UserUpdateRequest, user_id : int) -> Dict[str, Any]:
    user_found = None
    for user in USER_DB:
        if user["userId"] == user_id:
            user_found = user
            break
    if not user_found:
        raise UnauthorizedException
    
    user_found["nickname"] = request.nickname if request.nickname is not None else user_found["nickname"]
    if request.profileImageId is not None:
        user["profileImageId"] = request.profileImageId
    
    return{
        "userId" : user_id,
        "isUpdated" : True
    }
    
def update_password(request : user_schemas.PasswordUpdateRequest, user_id : int) -> Dict[str, Any]:
    user_found = None
    for user in USER_DB:
        if user["userId"] == user_id:
            user_found = user
            break
    if not user_found:
        raise UnauthorizedException
    
    hashed_new_pw = get_password_hash(request.newPassword)
    
    user_found["password"] = hashed_new_pw
    
    return {"userId" : user_id, "isUpdated" : True}

def read_user_info(user_id : int) -> Dict[str, Any]:
    user_found = None
    for user in USER_DB:
        if user["userId"] == user_id:
            user_found = user
            break
    if not user_found:
        raise UnauthorizedException

    response_data = {
        "email" : user_found["email"],
        "nickname" : user_found["nickname"],
        "profileImageId" : user_found.get("profileImageId")
    }
    return response_data
    
def delete_user(user_id : int) -> Dict[str, Any]:
    user_found_index = -1
    for i, user in enumerate(USER_DB):
        if user["userId"] == user_id:
            user_found_index = i
            break
    if user_found_index == -1 :
        raise UnauthorizedException
    
    USER_DB.pop(user_found_index)
    
    response = {
        "userId" : user_id,
        "isDeleted" : True
    }
    return response
