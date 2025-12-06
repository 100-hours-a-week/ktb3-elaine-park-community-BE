import re
from pydantic import BaseModel, field_validator, model_validator, EmailStr
from typing import Optional

def validate_password_logic(v:str) -> str:
    if len(v) < 8 or len(v) > 20:
        raise ValueError("비밀번호에는 8자 이상, 20자 이하여야 합니다.")
    if not re.search(r"[a-z]", v):
        raise ValueError("비밀번호에는 최소 하나의 소문자가 포함되어야 합니다.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("비밀번호에는 최소 하나의 대문자가 포함되어야 합니다.")
    if not re.search(r"[0-9]", v):
        raise ValueError("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("비밀번호에는 최소 하나의 특수문자가 포함되어야 합니다.")
    return v

#DTO 역할
class UserSignUpRequest(BaseModel):
    email: EmailStr
    password : str 
    nickname : str
    profileImageId : Optional[int] = None
    
    @field_validator('password')
    def validate_pw(cls, v): 
        return validate_password_logic(v)
        
class UserSignUpResposne(BaseModel):
    userId : int
    email : str
    nickname : str
    profileImageId : Optional[int] = None
    
class UserLoginRequest(BaseModel):
    email : EmailStr
    password : str

class UserLoginResponse(BaseModel):
    accessToken : str
    tokenType : str
    
class UserUpdateRequest(BaseModel):
    nickname : str
    profileImageId : Optional[int] = None

class UsesrUpdateResponse(BaseModel):
    userId : int
    isUpdated : bool
    
class PasswordUpdateRequest(BaseModel):
    newPassword : str
    newPasswordCheck : str
    
    @field_validator('newPassword')
    def validate_pw(cls, v):
        return validate_password_logic(v)
    
    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.newPassword != self.newPasswordCheck:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return self

class PasswordUpdateResponse(BaseModel):
    userId : int
    isUpdated : bool
    
class UserInfoReadResponse(BaseModel):
    profileImageId : Optional[int] = None
    email : str
    nickname : str
    
class UserDeleteResponse(BaseModel):
    userId : int
    isDeleted : bool