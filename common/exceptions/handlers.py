from fastapi import Request
from fastapi.responses import JSONResponse
from common.apiResponse import CommonResponse
from common.exceptions.BaseException import UnicornException

async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    UnicornException을 상속받는 모든 커스텀 예외를 처리하는 핸들러.
    FastAPI의 JSONResponse를 사용하여 일관된 실패 응답 형식 반환
    """
    return JSONResponse(
        status_code=400,
        content=CommonResponse.fail_response(
            errorCode=exc.errorCode,
            message=exc.message,
            result=None
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """
    FastAPI/Pydantic 자체의 유효성 검사 오류(타입 불일치, 필수 필드 누락) 처리 핸들러
    """
    return JSONResponse(
        status_code=422,
        content=CommonResponse.fail_response(
            errorCode="VALIDATION_ERROR",
            message="요청 데이터의 형식이 올바르지 않습니다.",
            result=None
        ).model_dump
    )