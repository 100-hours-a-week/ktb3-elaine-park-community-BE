from fastapi import Request
from fastapi.responses import JSONResponse
from common.apiResponse import CommonResponse
from common.exceptions.BaseException import UnicornException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    UnicornException을 상속받는 모든 커스텀 예외를 처리하는 핸들러.
    FastAPI의 JSONResponse를 사용하여 일관된 실패 응답 형식 반환
    """
    
    logger.warning(f"Business Logic Error: URL={request.url} CODE={exc.errorCode} MSG={exc.message}")
    
    return JSONResponse(
        status_code=400,
        content=CommonResponse.fail_response(
            errorCode=exc.errorCode,
            message=exc.message,
            result=None
        ).model_dump()
    )
    
async def internal_exception_handler(request: Request, exc: Exception):
    
    logger.exception(f"FATAL 500 ERROR Occured at URL : {request.url}")
    
    # 서버 500번대 오류
    return JSONResponse(
        status_code=500,
        content=CommonResponse.fail_response(
            errorCode="INTERNAL_SERVER_ERROR",
            message="서버에 예상치 못한 오류가 발생했습니다.",
            result=None
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    FastAPI/Pydantic 자체의 유효성 검사 오류(타입 불일치, 필수 필드 누락) 처리 핸들러
    """
    
    first_error = exc.errors()[0]
    error_loc = first_error.get('loc', ['body'])[-1]
    error_msg = first_error.get('msg')
    
    logger.error(f"Pydantic Validation Error at {error_loc}: {error_msg}")
    
    return JSONResponse(
        status_code=422,
        content=CommonResponse.fail_response(
            errorCode="VALIDATION_ERROR",
            message=error_msg,
            result=None
        ).model_dump()
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    FastAPI에서 발생하는 모든 HTTP 에러(401, 403, 404 등)를 처리.
    """
    
    # 1. 401 Unauthorized (로그인 안 함, 토큰 만료)
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content=CommonResponse.fail_response(
                errorCode="NOT_AUTHENTICATED",
                message="로그인이 필요합니다.", 
                result=None
            ).model_dump()
        )

    # 2. 403 Forbidden (권한 없음)
    if exc.status_code == 403:
        return JSONResponse(
            status_code=403,
            content=CommonResponse.fail_response(
                errorCode="PERMISSION_DENIED",
                message="권한이 없습니다.",
                result=None
            ).model_dump()
        )

    # 3. 404 Not Found (경로 없음)
    if exc.status_code == 404:
        logger.warning(f"404 Not Found: Path={request.url.path}")
        return JSONResponse(
            status_code=404,
            content=CommonResponse.fail_response(
                errorCode="ROUTE404_NOT_FOUND",
                message=f"요청 경로가 잘못되었습니다 : {request.url.path}",
                result=None
            ).model_dump()
        )
        
    # 4. 그 외 HTTP 에러들 (400, 405 등) 
    return JSONResponse(
        status_code=exc.status_code,
        content=CommonResponse.fail_response(
            errorCode=f"HTTP_{exc.status_code}",
            message=str(exc.detail), # FastAPI가 던진 에러 메시지 사용
            result=None
        ).model_dump()
    )