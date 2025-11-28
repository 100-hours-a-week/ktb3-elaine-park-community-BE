from fastapi import FastAPI
from common.exceptions.BaseException import UnicornException
from common.exceptions.handlers import unicorn_exception_handler, validation_exception_handler, path_exception_handler
from domain.post.post_router import router as post_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="커뮤니티 백엔드 (Route 단독)")

app.add_exception_handler(UnicornException, unicorn_exception_handler) # 커스텀 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, path_exception_handler)
app.include_router(post_router, prefix="/api/v1")






