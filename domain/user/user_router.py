from fastapi import APIRouter, status, Depends
from common.dependencies import get_current_user_id
from typing import Dict, Any
from common.apiResponse import CommonResponse
from . import user_controller
from . import user_schemas

router = APIRouter(
    prefix="/users",
    tags=["유저(Auth)"]
)

@router.post("/signup", response_model=CommonResponse[user_schemas.UserSignUpResposne], status_code = status.HTTP_201_CREATED)
async def signup(request : user_schemas.UserSignUpRequest):
    new_user = user_controller.sign_up(request)
    return CommonResponse.success_response(message="user_register_success", result=new_user)

@router.post("/login", response_model=CommonResponse[user_schemas.UserLoginResponse], status_code=status.HTTP_200_OK)
async def login(request: user_schemas.UserLoginRequest):
    token_data = user_controller.login(request)
    return CommonResponse.success_response(message="login_success", result=token_data)

@router.patch("/{user_id}", response_model=CommonResponse[user_schemas.UsesrUpdateResponse], status_code=status.HTTP_200_OK)
async def update_user_info(
    request: user_schemas.UserUpdateRequest,
    user_id : int = Depends(get_current_user_id)):
    updated_user = user_controller.updateInfo(request, user_id)
    return CommonResponse.success_response(message="user_update_success", result=updated_user)

@router.patch("/{user_id}/password", response_model=CommonResponse[user_schemas.PasswordUpdateResponse], status_code=status.HTTP_200_OK)
async def update_password(
    request: user_schemas.PasswordUpdateRequest,
    user_id : int = Depends(get_current_user_id)):
    updated_pw = user_controller.update_password(request, user_id)
    return CommonResponse.success_response(message="password_update_success", result=updated_pw)

@router.get("/{user_id}", response_model=CommonResponse[user_schemas.UserInfoReadResponse], status_code=status.HTTP_200_OK)
async def read_user_info(
    user_id : int = Depends(get_current_user_id)):
    get_user = user_controller.read_user_info(user_id)
    return CommonResponse.success_response(message="user_data_success", result=get_user)

@router.delete("/{user_id}", response_model=CommonResponse[user_schemas.UserDeleteResponse], status_code=status.HTTP_200_OK)
async def delete_user(
    user_id : int = Depends(get_current_user_id)
):
    response = user_controller.delete_user(user_id)
    return CommonResponse.success_response(message="user_delete_success", result=response)