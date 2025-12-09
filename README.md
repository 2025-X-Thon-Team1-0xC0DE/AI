# 🧠 gAIde AI 모델 서버

> gAIde에서 백엔드의 요청을 받아 AI 모델에 요청하고, 받아낸 응답을 다시 백엔드로 전달해주는 역할을 합니다.

## 📋 프로젝트 개요

FastAPI 기반의 AI 문서 작성 지원 서버입니다. OpenAI GPT-4o 모델을 활용하여 다양한 유형의 문서(이력서, 보고서, 논문, 자기소개서)에 대한 피드백, 개요 생성, 평가 기능을 제공합니다.

## 🏗️ 프로젝트 구조

```
AI/
├── main.py                    # FastAPI 애플리케이션 진입점
├── settings.py                # 환경 변수 및 설정 관리
├── requirements.txt           # 프로젝트 의존성
├── README.md
└── src/
    ├── enums.py              # 문서 카테고리 및 피드백 타입 정의
    ├── routes.py             # API 엔드포인트 정의
    ├── schemas.py            # Pydantic 모델 정의
    └── prompters/            # 프롬프트 생성 모듈
        ├── __init__.py
        ├── abstract.py       # Prompter 추상 클래스
        ├── feedback.py       # 피드백 프롬프터
        ├── evaluation.py     # 평가 프롬프터
        └── outline.py        # 개요 생성 프롬프터
```

## ✨ 주요 기능

### 1. 문서 피드백 생성 (`POST /api/feedback`)
- 사용자가 작성한 문서에 대한 전문가 수준의 피드백 제공
- 문서 카테고리별 맞춤형 검토 (이력서, 보고서, 논문, 자기소개서)
- 키워드 강조 및 작성 의도 기반 피드백

### 2. 문서 개요 생성 (`POST /api/feedback`)
- 문서 카테고리와 키워드 기반 작성 가이드라인 제공
- 구조화된 개요 제안

### 3. 문서 평가 (`POST /api/evaluation`)
- 작성된 문서의 종합적인 평가 및 요약
- 강점과 개선점 분석

## 🚀 시작하기

### 필수 요구사항

- Python 3.8 이상
- OpenAI API 키

### 설치 및 실행

1. **의존성 설치**
```bash
pip install -r requirements.txt
```

2. **환경 변수 설정**

프로젝트 루트에 `.env` 파일 생성:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. **서버 실행**

```bash
python main.py
```

또는 VS Code에서 F5를 눌러 디버그 모드로 실행

서버가 `http://localhost:8000`에서 시작됩니다.

4. **API 문서 확인**

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API 명세

### POST /api/feedback

문서에 대한 피드백 또는 개요를 생성합니다.

**Request Body:**
```json
{
  "category": "RESUME",
  "keywords": ["프로젝트 관리", "팀 리더십"],
  "request_type": 1,
  "description": "신입 개발자 지원용 이력서",
  "user_text": "사용자가 작성한 문서 내용"
}
```

**Parameters:**
- `category`: 문서 유형 (RESUME, REPORT, ESSAY, COVER_LETTER)
- `keywords`: 강조할 키워드 리스트
- `request_type`: 요청 타입 (0: 개요 생성, 1: 피드백)
- `description`: 문서 작성 의도
- `user_text`: 검토할 문서 내용

**Response:**
```json
{
  "feedback": [
    "피드백 내용 1",
    "피드백 내용 2",
    "..."
  ]
}
```

### POST /api/evaluation

문서를 평가하고 종합적인 피드백을 제공합니다.

**Request Body:**
```json
{
  "category": "RESUME",
  "keywords": ["프로젝트 관리", "팀 리더십"],
  "description": "신입 개발자 지원용 이력서",
  "user_text": "사용자가 작성한 문서 내용"
}
```

**Response:**
```json
{
  "eval": "종합 평가 내용"
}
```

## 🔧 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **OpenAI API**: GPT-4o 모델을 통한 AI 피드백 생성
- **Pydantic**: 데이터 검증 및 스키마 정의
- **Uvicorn**: ASGI 서버
- **python-dotenv**: 환경 변수 관리

## 📝 문서 카테고리

| 카테고리 | 설명 | 검토 기준 |
|---------|------|----------|
| RESUME | 이력서 | 성과 중심, 구체성, 가독성 |
| REPORT | 보고서/기획서 | 논리적 완결성, 두괄식 구성, 비즈니스 톤 |
| ESSAY | 논문/에세이 | 논증의 깊이, 문단 연결, 어휘 선택 |
| COVER_LETTER | 자기소개서 | 스토리텔링, 직무 적합성, 진정성 |

## 🔄 개발 모드

서버는 `reload=True` 옵션으로 실행되어 `src/` 디렉토리의 변경사항을 자동으로 감지하고 재시작합니다.
