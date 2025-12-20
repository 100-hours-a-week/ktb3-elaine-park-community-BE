# ktv3-elaine-park-community-BE

## 🌊 Mood Waver (무드 웨이버)
<img width="700" height="500" alt="스크린샷 2025-12-19 오후 3 19 02" src="https://github.com/user-attachments/assets/b03bcbca-4526-41bd-97aa-ce102de209c1" />


**"당신의 감정을 음악으로"**

**Mood Waver**는 사용자가 작성한 글의 분위기를 **AI가 분석**하여, 그 순간 가장 잘 어울리는 **음악(BGM)을 추천**해주는 감성 커뮤니티 서비스입니다.

## 📖 목차
1. [프로젝트 소개](#-프로젝트-소개)
2. [기술 스택](#-tech-stack)
3. [주요 기능](#-key-features)
4. [폴더 구조](#-project-structure)
5. [API 명세](#-api-specification)
6. [실행 방법](#-how-to-run)

---

## 🚀 프로젝트 소개
일상의 소소한 이야기나 고민을 적으면, 텍스트에 담긴 감정을 분석해 위로가 되거나 분위기를 돋우는 음악을 추천받을 수 있습니다. 추천받은 음악을 게시글에 포함하여 다른 사용자들과 감정을 공유하고 소통할 수 있습니다.

---

## 🛠 Tech Stack

### Backend
| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | 비동기 처리를 지원하는 고성능 웹 프레임워크 |
| **Language** | Python 3.10.19 | 서버 로직 구현 |
| **Database** | SQLAlchemy | ORM을 이용한 DB 제어 |
| **AI / ML** | **Sentence-Transformers** | 텍스트 임베딩 및 코사인 유사도 분석 |
| **Auth** | JWT (JSON Web Token) | 사용자 인증 및 인가 |
| **Validation** | Pydantic | 데이터 유효성 검사 |

### Frontend
| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Core** | HTML5, CSS3 | 시맨틱 마크업 및 스타일링 |
| **Script** | **Vanilla JavaScript (ES6+)** | 프레임워크 없는 순수 자바스크립트 구현 |
| **Async** | Fetch API | 비동기 서버 통신 (Async/Await) |

---

## ✨ Key Features

### 1. 🤖 AI 기반 음악 추천 (AI Music Recommendation)
- **감정 분석:** 사용자가 작성 중인 글(제목+내용)을 실시간으로 분석합니다.
- **임베딩 및 매칭:** `Sentence-Transformers` 모델을 사용하여 텍스트를 벡터화하고, DB에 저장된 노래들의 분위기와 **코사인 유사도**를 계산합니다.
- **추천:** 가장 유사도가 높은 상위 5곡을 추천하며, 클릭 시 본문에 자동 삽입됩니다.

### 2. 📝 게시글 및 피드 (Feed & Post)
- **CRUD:** 게시글 작성, 조회, 수정, 삭제 기능을 완벽하게 지원합니다.
- **이미지 업로드:** 게시글 작성 및 수정 시 이미지를 업로드하고 미리볼 수 있습니다.
- **UI/UX:** 최신순 피드 정렬 및 직관적인 카드형 레이아웃을 제공합니다.

### 3. 💬 소통 및 반응 (Interaction)
- **댓글 시스템:** 게시글에 댓글을 달고, **인라인(In-line) 수정** 및 삭제가 가능합니다.
- **좋아요:** 하트 버튼을 통해 게시글에 공감을 표시할 수 있습니다.
- **조회수:** 게시글 클릭 시 조회수가 집계됩니다.

### 4. 👤 회원 관리 (User System)
- **보안:** JWT를 이용한 로그인 유지 및 `bcrypt`를 이용한 비밀번호 암호화.
- **마이페이지:**
  - 프로필 사진 변경 (이미지 업로드)
  - 닉네임 수정
  - 이메일 조회 (Read-only)
  - 회원 탈퇴
- **비밀번호 변경:** 현재 비밀번호 검증 후 안전하게 변경 가능.

---

## 📂 Project Structure
Backend
Domain-Driven Design (DDD) 패턴을 적용하여 기능별로 도메인을 분리하고, 공통 모듈과 예외 처리를 체계적으로 관리하고 있습니다.

```bash
📦 Backend-Root
├── 📂 common               # 공통 모듈 및 유틸리티
│   ├── 📂 exceptions       # 커스텀 예외 클래스 및 핸들러
│   │   ├── BaseException.py
│   │   ├── customException.py
│   │   └── handlers.py
│   ├── apiResponse.py      # 공통 API 응답 스키마
│   ├── database.py         # DB 연결 및 세션 설정
│   ├── dependencies.py     # 의존성 주입 관리
│   └── security.py         # 보안 관련 (JWT, 해싱 등)
├── 📂 data                 # 초기 데이터 파일
│   └── songs.json          # 음악 추천용 초기 데이터
├── 📂 domain               # 도메인별 비즈니스 로직 (Controller, Service, Router)
│   ├── 📂 comment          # 댓글 관리
│   ├── 📂 image            # 이미지 업로드 및 관리
│   ├── 📂 likes            # 좋아요 기능
│   ├── 📂 music            # AI 음악 추천
│   ├── 📂 post             # 게시글 CRUD
│   └── 📂 user             # 회원 가입, 로그인, 정보 관리
├── 📂 uploaded_images      # 사용자가 업로드한 이미지 저장소
├── .env                    # 환경 변수 설정
├── .gitignore              # Git 제외 파일 목록
├── docker-compose.yml      # Docker 컨테이너 설정
├── init_data.py            # 초기 데이터 적재 스크립트
├── main.py                 # FastAPI 애플리케이션 진입점 (Entry Point)
└── README.md               # 프로젝트 설명 파일
```
---
## 📡 주요 API 명세서
#### 🔐 Auth & User
* `POST /api/v1/auth/login` : 로그인
* `POST /api/v1/users/signup` : 회원가입
* `GET /api/v1/users/me` : 내 정보 조회
* `PATCH /api/v1/users/me` : 내 정보 수정
* `PATCH /api/v1/users/me/password` : 비밀번호 변경
* `DELETE /api/v1/users/me` : 회원 탈퇴

#### 📝 Post & Comment
* `GET /api/v1/posts` : 피드 목록 조회
* `POST /api/v1/posts` : 게시글 작성
* `GET /api/v1/posts/{id}` : 게시글 상세
* `PATCH /api/v1/posts/{id}` : 게시글 수정
* `DELETE /api/v1/posts/{id}` : 게시글 삭제
* `POST /api/v1/posts/{id}/comments` : 댓글 작성
* `PATCH /api/v1/comments/{id}` : 댓글 수정
* `DELETE /api/v1/comments/{id}` : 댓글 삭제

#### 🎵 Feature
* `POST /api/v1/music/recommend` : **AI 음악 추천**
* `POST /api/v1/images/upload` : 이미지 업로드
