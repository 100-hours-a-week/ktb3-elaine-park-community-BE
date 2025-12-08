# ktb3-elaine-park-BE

# 🌊 MoodWaver Backend API

**MoodWaver**는 사용자의 감정 텍스트를 분석하여 상황에 맞는 음악을 추천해주는 커뮤니티 서비스의 백엔드 서버입니다.
**FastAPI**를 기반으로 구축되었으며, **Sentence-Transformers** AI 모델을 활용한 텍스트 임베딩 및 유사도 분석 기능을 제공합니다.

## 🛠 Tech Stack

| Category | Technology |
| --- | --- |
| **Framework** | Python 3.10, FastAPI |
| **Database** | SQLAlchemy, RDBMS (MySQL/PostgreSQL) |
| **AI / ML** | Sentence-Transformers (`jhgan/ko-sroberta-multitask`), NumPy, PyTorch |
| **Auth** | JWT (JSON Web Token), bcrypt |
| **Validation** | Pydantic |

## ✨ Key Features

* **AI 음악 추천 시스템 (TBR)**
    * SBERT 모델을 활용한 한국어 문장 임베딩
    * Cosine Similarity(코사인 유사도) 기반 Top-K 추천 알고리즘
* **RESTful API 설계**
    * 계층형 아키텍처 (Router - Controller - Model - Schema) 적용
* **사용자 인증 및 인가**
    * 회원가입, 로그인, JWT 액세스 토큰 발급 및 검증
* **커뮤니티 기능**
    * 게시글 CRUD (작성, 조회, 수정, 삭제)
    * 댓글 및 좋아요 기능
    * 게시글 상세 조회 시 Eager Loading을 통한 성능 최적화
* **이미지 처리**
    * Local Storage 기반 이미지 업로드 및 정적 파일 서빙 (StaticFiles)

## 📂 Project Structure

```text
music-backend/
├── common/             # 공통 모듈 (DB 연결, 예외 처리, 응답 포맷)
├── data/               # 초기 음악 데이터 (song.json)
├── domain/             # 도메인별 로직 분리
│   ├── comment/        # 댓글 기능
│   ├── image/          # 이미지 업로드
│   ├── likes/          # 좋아요 기능
│   ├── music/          # AI 음악 추천
│   ├── post/           # 게시글 기능
│   └── user/           # 회원가입/로그인
├── static/             # 업로드된 이미지 저장소
├── init_data.py        # 초기 데이터 적재 스크립트
└── main.py             # 앱 진입점 (Server Entry)
