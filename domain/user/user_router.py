from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from common.dependencies import get_current_user_id
from typing import Dict, Any
from common.apiResponse import CommonResponse
from common.database import get_db
from . import user_controller
from . import user_schemas

router = APIRouter(
    prefix="/users",
    tags=["유저(Auth)"]
)

@router.post("/signup", response_model=CommonResponse[user_schemas.UserSignUpResposne], status_code = status.HTTP_201_CREATED)
async def signup(
    request : user_schemas.UserSignUpRequest,
    db: Session = Depends(get_db)
):
    new_user = user_controller.sign_up(db, request)
    return CommonResponse.success_response(message="user_register_success", result=new_user)

@router.post("/login", response_model=CommonResponse[user_schemas.UserLoginResponse], status_code=status.HTTP_200_OK)
async def login(
    request: user_schemas.UserLoginRequest,
    db: Session = Depends(get_db)
):
    token_data = user_controller.login(db, request)
    return CommonResponse.success_response(message="login_success", result=token_data)

@router.patch("/me", response_model=CommonResponse[user_schemas.UsesrUpdateResponse], status_code=status.HTTP_200_OK)
async def update_user_info(
    request: user_schemas.UserUpdateRequest,
    db: Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
):
    updated_user = user_controller.updateInfo(db, request, user_id)
    return CommonResponse.success_response(message="user_update_success", result=updated_user)

@router.patch("/me/password", response_model=CommonResponse[user_schemas.PasswordUpdateResponse], status_code=status.HTTP_200_OK)
async def update_password(
    request: user_schemas.PasswordUpdateRequest,
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
):
    updated_pw = user_controller.update_password(db, request, user_id)
    return CommonResponse.success_response(message="password_update_success", result=updated_pw)

@router.get("/me", response_model=CommonResponse[user_schemas.UserInfoReadResponse], status_code=status.HTTP_200_OK)
async def read_user_info(
    db : Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
):
    get_user = user_controller.read_user_info(db, user_id)
    return CommonResponse.success_response(message="user_data_success", result=get_user)

@router.delete("/me", response_model=CommonResponse[user_schemas.UserDeleteResponse], status_code=status.HTTP_200_OK)
async def delete_user(
    db: Session = Depends(get_db),
    user_id : int = Depends(get_current_user_id)
):
    response = user_controller.delete_user(db, user_id)
    return CommonResponse.success_response(message="user_delete_success", result=response)