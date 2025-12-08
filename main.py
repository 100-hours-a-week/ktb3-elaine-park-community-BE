from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #CORS 설정
from fastapi.staticfiles import StaticFiles
from common.exceptions.BaseException import UnicornException
from common.exceptions.handlers import *
from domain.post.post_router import router as post_router
from domain.user.user_router import router as user_router
from domain.likes.likes_router import router as likes_router
from domain.image.image_router import router as image_router
from domain.music.music_router import router as music_router
from domain.comment.comment_router import router as comment_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from common.database import engine, Base, SessionLocal
from contextlib import asynccontextmanager
from init_data import init_song_data
from domain.user import user_model
from domain.post import post_model
from domain.comment import comment_model
from domain.likes import likes_model
from domain.image import image_model
from domain.music import music_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 시작! 데이터 확인 및 초기화 중...")
    db = SessionLocal()
    try:
        init_song_data(db)
    except Exception as e:
        print(f"데이터 초기화 중 오류 발생 : {e}")
    finally:
        db.close()
    
    yield # 이 지점에서 서버가 실행되고 요청 받음.
    
    print("서버 종료 및 리소스 정리")

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(UnicornException, unicorn_exception_handler) # 커스텀 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)

#CORS 설정 추가(app 생성 직후에 작성)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 주소에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"], # GET, POST 등 모든 메소드 허용
    allow_headers=["*"] # 모든 헤더 허용
)

app.include_router(post_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(likes_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")
app.include_router(comment_router, prefix="/api/v1")
app.include_router(music_router, prefix="/api/v1")

app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")

# DB 테이블 생성(Spring의 ddl-auto 역할)
Base.metadata.create_all(bind=engine)




