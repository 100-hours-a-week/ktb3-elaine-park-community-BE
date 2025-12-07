from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 형식: postgresql://아이디:비밀번호@주소:포트/DB이름
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:pwd1234@localhost:5432/mydb"

# 엔진 생성(파이썬과 DB 연결)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DB 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델(테이블)을 만들 떄 상속받는 기본 클래스
Base = declarative_base()

# DB 세션을 함수마다 빌려주고 닫아줌.(Dependency Injection용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()