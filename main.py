from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from common.exceptions.BaseException import UnicornException
from common.exceptions.handlers import *
from domain.post.post_router import router as post_router
from domain.user.user_router import router as user_router
from domain.likes.likes_router import router as likes_router
from domain.image.image_router import router as image_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="커뮤니티 백엔드 (Route 단독)")

app.add_exception_handler(UnicornException, unicorn_exception_handler) # 커스텀 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)
app.include_router(post_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(likes_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")

app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")






