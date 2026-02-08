# LinkNote - Completed Tasks Archive

> This file contains detailed documentation of completed tasks.
> For active tasks and project overview, see TASKS.md

---

## Completed Tasks Summary

| Task ID | Task Name | Completed Date |
|---------|-----------|----------------|
| ENV-01 | 서버 환경 변수 및 설정 구성 | 2024-01-19 |
| DB-01 | Supabase 프로젝트 생성 및 테이블 설정 | 2024-01-19 |
| SERVER-01 | 서버 로컬 실행 및 기본 API 테스트 | 2024-01-19 |
| BE-01 | YouTube 메타데이터 추출 개선 | 2024-01-19 |
| BE-02 | 서버 에러 핸들링 및 로깅 시스템 | 2024-01-19 |
| AI-01 | AI 요약 프롬프트 최적화 | 2024-01-19 |
| AI-02 | AI 태그 및 카테고리 분류 개선 | 2024-01-19 |
| AI-03 | AI 요청 실패 시 폴백 처리 | 2024-01-20 |
| BE-03 | 링크 삭제 API 구현 | 2025-01-21 |
| BE-04 | 링크 중복 저장 방지 | 2025-02-02 |
| APP-01 | 앱 환경 변수 및 API 연결 설정 | 2025-02-02 |
| APP-02 | 홈 화면 FAB 버튼 및 네비게이션 개선 | 2025-02-02 |
| APP-03 | 링크 상세 화면 구현 | 2025-02-02 |
| APP-04 | 링크 삭제 기능 (앱) | 2025-02-02 |
| APP-05 | Android 공유 인텐트 수신 구현 | 2025-02-02 |
| APP-06 | iOS 공유 익스텐션 기본 설정 | 2025-02-02 |
| APP-07 | 에러 처리 및 토스트 메시지 시스템 | 2025-02-03 |
| APP-08 | 로딩 상태 및 스켈레톤 UI 구현 | 2025-02-03 |
| APP-09 | 앱 아이콘 및 스플래시 화면 설정 | 2025-02-03 |
| SERVER-02 | 서버 배포 (Railway/Render) | 2025-02-03 |
| APP-10 | 프로덕션 API URL 설정 및 빌드 테스트 | 2025-02-03 |
| APP-11 | EAS Build 설정 및 APK/IPA 빌드 | 2025-02-03 |
| DEPLOY-01 | GitHub 푸시 및 서버 실제 배포 | 2026-02-08 |
| DEPLOY-02 | Expo 계정 및 EAS 프로젝트 설정 | 2026-02-08 |
| DEPLOY-03 | 빌드 전 코드 수정 (플러그인 활성화 등) | 2026-02-08 |
| DEPLOY-04 | Android APK 빌드 (EAS Build) | 2026-02-08 |
| DEPLOY-05 | 스마트폰 설치 및 전체 기능 테스트 | 2026-02-08 |
| AUTH-01 | Supabase Auth 스키마 + 서버 인증 미들웨어 | 2026-02-08 |

---

# PHASE 1: 환경 설정

---

## TASK ENV-01: 서버 환경 변수 및 설정 구성 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | FastAPI 서버 실행을 위한 환경 변수 파일 구성 |
| **작업 유형** | 설정 |
| **의존성** | 없음 |

### 현재 상태
- `server/.env.example` 파일 존재
- 실제 `.env` 파일 미생성

### 작업 내용

#### 1. 외부 서비스 API 키 준비
| 서비스 | URL | 필요 정보 |
|--------|-----|-----------|
| Supabase | https://supabase.com | Project URL, anon key |
| OpenAI | https://platform.openai.com | API key |

#### 2. 환경 변수 파일 생성
```bash
# server/.env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
OPENAI_API_KEY=sk-...
DEBUG=true
```

#### 3. 설정 로드 검증
`server/app/core/config.py`에서 환경 변수 로드 확인

### 테스트 수행

#### 테스트 케이스
| TC-ID | 테스트 항목 | 입력/조건 | 예상 결과 |
|-------|-------------|-----------|-----------|
| ENV-01-TC01 | 환경 변수 로드 | Python 인터프리터 실행 | 값 정상 출력 |
| ENV-01-TC02 | 빈 값 검증 | 필수 값 누락 시 | 에러 메시지 |

#### 테스트 실행 방법
```bash
cd server
python -c "
from app.core.config import settings
print('SUPABASE_URL:', settings.SUPABASE_URL[:30] + '...' if settings.SUPABASE_URL else 'EMPTY')
print('OPENAI_API_KEY:', 'SET' if settings.OPENAI_API_KEY else 'EMPTY')
"
```

### 테스트 결과 체크
- [x] ENV-01-TC01: 환경 변수 로드 성공
- [x] ENV-01-TC02: 값 유효성 확인

### 완료 조건
- [x] `.env` 파일 생성됨
- [x] 모든 테스트 케이스 통과
- [x] 작업 현황 체크리스트 상태 업데이트

### 참고 파일
- `server/.env.example`
- `server/app/core/config.py`

---

## TASK DB-01: Supabase 프로젝트 생성 및 테이블 설정 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | Supabase에 links 테이블 생성하여 데이터 저장소 준비 |
| **작업 유형** | 데이터베이스 |
| **의존성** | ENV-01 완료 |

### 현재 상태
- `server/supabase_schema.sql` 파일에 SQL 준비됨

### 작업 내용

#### 1. Supabase 대시보드에서 SQL 실행
```sql
-- server/supabase_schema.sql 전체 실행

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS links (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  thumbnail TEXT,
  summary TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_links_category ON links(category);

ALTER TABLE links ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all access for all users" ON links
  FOR ALL USING (true) WITH CHECK (true);
```

### 테스트 수행

#### 테스트 케이스
| TC-ID | 테스트 항목 | 입력/조건 | 예상 결과 |
|-------|-------------|-----------|-----------|
| DB-01-TC01 | 테이블 생성 확인 | Table Editor 확인 | links 테이블 표시 |
| DB-01-TC02 | 데이터 삽입 테스트 | SQL로 INSERT | 성공 |
| DB-01-TC03 | 데이터 조회 테스트 | SQL로 SELECT | 삽입된 데이터 반환 |

#### 테스트 실행 방법
```sql
-- Supabase SQL Editor에서 실행

-- TC02: INSERT 테스트
INSERT INTO links (url, title, summary, tags, category)
VALUES ('https://test.com', 'Test Title', 'Test Summary', ARRAY['tag1', 'tag2'], 'test');

-- TC03: SELECT 테스트
SELECT * FROM links WHERE url = 'https://test.com';

-- 테스트 데이터 정리
DELETE FROM links WHERE url = 'https://test.com';
```

### 테스트 결과 체크
- [x] DB-01-TC01: 테이블 존재 확인
- [x] DB-01-TC02: INSERT 성공
- [x] DB-01-TC03: SELECT 성공

### 완료 조건
- [x] `links` 테이블 생성됨
- [x] RLS 정책 적용됨
- [x] 모든 테스트 케이스 통과

### 왜 이렇게 설계했는가?
| 결정 사항 | 이유 |
|-----------|------|
| UUID를 PK로 | 분산 환경 충돌 방지, 클라이언트에서 미리 ID 생성 가능 |
| tags를 TEXT[] 배열 | 별도 조인 테이블 없이 간단하게 저장, PostgreSQL 네이티브 지원 |
| created_at 인덱스 | 최신순 정렬이 가장 빈번한 쿼리 |
| RLS 전체 허용 | MVP에서는 인증 없이 개인 사용, 추후 인증 추가 시 변경 |

### 참고 파일
- `server/supabase_schema.sql`

---

## TASK SERVER-01: 서버 로컬 실행 및 기본 API 테스트 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | FastAPI 서버 로컬 실행 및 기본 API 동작 검증 |
| **작업 유형** | 서버 |
| **의존성** | DB-01 완료 |

### 현재 상태
- 서버 코드 `server/` 디렉토리에 구성됨
- 의존성 `requirements.txt` 정의됨

### 작업 내용

#### 1. 가상환경 생성 및 의존성 설치
```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 서버 실행
```bash
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 테스트 수행

#### 테스트 케이스
| TC-ID | 테스트 항목 | 입력/조건 | 예상 결과 |
|-------|-------------|-----------|-----------|
| SV-01-TC01 | 헬스 체크 | GET /health | `{"status": "healthy"}` |
| SV-01-TC02 | 링크 저장 | POST /api/links/save | 저장된 링크 정보 반환 |
| SV-01-TC03 | 링크 목록 조회 | GET /api/links/ | 링크 배열 반환 |
| SV-01-TC04 | Swagger 문서 | GET /docs | Swagger UI 표시 |

#### 테스트 실행 방법
```bash
# TC01: 헬스 체크
curl http://localhost:8000/health

# TC02: 링크 저장 (실제 유튜브 URL 사용)
curl -X POST http://localhost:8000/api/links/save \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# TC03: 링크 목록 조회
curl http://localhost:8000/api/links/

# TC04: 브라우저에서 확인
# http://localhost:8000/docs
```

### 테스트 결과 체크
- [x] SV-01-TC01: 헬스 체크 응답 확인
- [x] SV-01-TC02: 링크 저장 성공 (요약, 태그 포함)
- [x] SV-01-TC03: 저장된 링크 목록 조회 성공
- [x] SV-01-TC04: Swagger 문서 접근 가능

### 완료 조건
- [x] 서버 8000 포트 실행
- [x] 모든 테스트 케이스 통과
- [x] Supabase에 저장된 데이터 확인

### 트러블슈팅
| 문제 | 해결 방법 |
|------|-----------|
| ModuleNotFoundError | `pip install -r requirements.txt` 재실행 |
| Supabase 연결 실패 | `.env` URL/KEY 확인 |
| OpenAI API 오류 | API 키 유효성 및 잔액 확인 |
| yt-dlp 오류 | `pip install --upgrade yt-dlp` |
| yt-dlp 버전 문제 | requirements.txt에서 `yt-dlp>=2024.1.0`으로 변경 |
| httpx 버전 충돌 | `httpx>=0.24.0`으로 변경 |

### 참고 파일
- `server/main.py`
- `server/app/api/links.py`
- `server/requirements.txt`

---

# PHASE 2: 백엔드 기능 개선

---

## TASK BE-01: YouTube 메타데이터 추출 개선 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | YouTube 링크에서 더 풍부한 메타데이터 추출 및 에러 처리 강화 |
| **작업 유형** | 백엔드 |
| **의존성** | SERVER-01 완료 |

### 구현 내용

#### 1. 추출 필드 확장
- duration (영상 길이)
- view_count (조회수)
- upload_date (업로드 날짜)
- channel_url (채널 링크)
- tags (유튜브 태그)

#### 2. URL 유효성 검사 강화
- video_id 추출 함수 (`extract_video_id`)
- URL 검증 함수 (`validate_youtube_url`)
- URL 정규화 함수 (`normalize_youtube_url`)

#### 3. 에러 케이스 처리
| 에러 케이스 | 처리 방법 |
|-------------|-----------|
| 비공개 영상 | "비공개 영상입니다. 공개 영상만 저장할 수 있습니다." |
| 삭제된 영상 | "삭제되었거나 존재하지 않는 영상입니다." |
| 지역 제한 | "해당 지역에서 재생할 수 없는 영상입니다." |
| 연령 제한 | "연령 제한 영상입니다." |
| 네트워크 오류 | 재시도 로직 (최대 2회) |

### 테스트 결과 체크
- [x] BE01-TC01: 정상 URL 메타데이터 추출
- [x] BE01-TC02: 단축 URL 처리
- [x] BE01-TC03: Shorts URL 처리
- [x] BE01-TC04: 잘못된 URL 에러 처리
- [x] BE01-TC05: 비유튜브 URL 거부

### 참고 파일
- `server/app/services/youtube.py`
- `server/app/api/links.py`

---

## TASK BE-02: 서버 에러 핸들링 및 로깅 시스템 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 체계적인 에러 핸들링과 로깅으로 디버깅 및 모니터링 개선 |
| **작업 유형** | 백엔드 |
| **의존성** | BE-01 완료 |

### 구현 내용

#### 1. 로깅 설정 구성
```python
# server/app/core/logging.py 생성
import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO") -> logging.Logger:
    log_level = getattr(logging, level.upper(), logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    root_logger.addHandler(stream_handler)
    return logging.getLogger("linknote")

def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name:
        return logging.getLogger(f"linknote.{name}")
    return logging.getLogger("linknote")
```

#### 2. 커스텀 예외 클래스 생성
```python
# server/app/core/exceptions.py 생성
class LinkNoteException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_type: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type or self.__class__.__name__
        super().__init__(self.message)

class YouTubeExtractionError(LinkNoteException):
    def __init__(self, message: str, error_type: str = "youtube_error"):
        super().__init__(message, status_code=400, error_type=error_type)

# Also: AIProcessingError, DatabaseError, ValidationError, NotFoundError, DuplicateError
```

#### 3. 전역 예외 핸들러 등록
- `LinkNoteException` 핸들러
- 일반 `Exception` 핸들러 (500 에러)
- 요청 로깅 미들웨어

### 테스트 결과 체크
- [x] BE02-TC01: 정상 요청 INFO 로그 출력
- [x] BE02-TC02: 에러 응답 JSON 형식 확인
- [x] BE02-TC03: 예외 ERROR 로그 출력

### 참고 파일
- `server/app/core/logging.py`
- `server/app/core/exceptions.py`
- `server/main.py`
- `server/app/services/*.py`

---

# PHASE 3: AI 기능 개선

---

## TASK AI-01: AI 요약 프롬프트 최적화 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 더 정확하고 유용한 한 줄 요약 생성을 위한 프롬프트 개선 |
| **작업 유형** | AI |
| **의존성** | BE-02 완료 |

### 구현 내용

#### 1. 프롬프트 개선
```python
SUMMARY_SYSTEM_PROMPT = """당신은 콘텐츠 요약 전문가입니다.

## 작업
주어진 YouTube 영상의 제목과 설명을 바탕으로 **핵심 가치**를 담은 한 줄 요약을 작성하세요.

## 규칙
1. 길이: 20-50자 (한국어 기준)
2. 형식: "~하는 방법", "~에 대한 내용", "~을 다룬 영상" 등
3. 핵심 정보 포함: 누가/무엇을/왜
4. 클릭베이트 지양: 과장 없이 사실적으로
5. 존댓말 사용 안 함

## 예시
- 좋은 예: "초보자를 위한 주식 투자 기초 개념 설명"
- 좋은 예: "React 18의 새로운 기능과 마이그레이션 방법"
- 좋은 예: "30분 전신 홈트레이닝 루틴 소개"
- 나쁜 예: "주식 투자에 대한 영상입니다"
- 나쁜 예: "이 영상을 보세요"

## 주의
- 제목만 반복하지 말 것
- 설명이 없으면 제목만으로 추론
- "영상입니다", "콘텐츠입니다" 같은 무의미한 표현 사용 금지
"""
```

#### 2. 요약 검증 로직 추가
```python
def validate_summary(self, summary: str, title: str) -> bool:
    # 길이 검증: 10자 이상 60자 이하
    # 의미 없는 패턴 필터링: "영상입니다", "콘텐츠입니다" 등
    # 제목과 동일한지 체크 (80% 이상 유사하면 무효)
```

#### 3. 실패 시 기본 요약 생성
```python
def generate_fallback_summary(self, title: str) -> str:
    # AI 실패 시 제목 기반 기본 요약 생성
    # 예: "{title}에 대한 영상"
```

### 테스트 결과 체크
- [x] AI01-TC01: 튜토리얼 영상 요약 품질 확인
- [x] AI01-TC02: 뉴스 영상 요약 품질 확인
- [x] AI01-TC03: 짧은 설명 처리 확인
- [x] AI01-TC04: 요약 길이 범위 확인 (10-60자)

### 설계 결정
| 결정 사항 | 이유 |
|-----------|------|
| 상세 프롬프트 규칙 | GPT가 일관된 형식으로 출력하도록 유도 |
| 예시 포함 | Few-shot 학습 효과로 품질 향상 |
| 길이 제한 20-50자 | 카드 UI에 적합한 길이 |
| 폴백 요약 | AI 실패 시에도 서비스 중단 방지 |

### 참고 파일
- `server/app/services/ai.py`

---

## TASK AI-02: AI 태그 및 카테고리 분류 개선 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 더 정확하고 유용한 태그와 카테고리 생성 |
| **작업 유형** | AI |
| **의존성** | AI-01 완료 |

### 구현 내용

#### 1. 태그 프롬프트 개선
- 5개 태그 생성 (주제 2개, 형식 1개, 대상 1개, 감성 1개)
- 명확한 출력 형식 지정

#### 2. 카테고리 프롬프트 개선
- 테이블 형식으로 카테고리 정의
- 8개 카테고리: 개발, 투자, 건강, 교육, 엔터테인먼트, 뉴스, 라이프스타일, 기타

#### 3. 검증 로직 추가
- `validate_tags()`: 태그 개수 및 형식 검증
- `validate_category()`: 유효한 카테고리인지 확인
- `generate_fallback_tags()`: 실패 시 제목 기반 태그 생성

### 참고 파일
- `server/app/services/ai.py`

---

## TASK AI-03: AI 요청 실패 시 폴백 처리 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | OpenAI API 실패 시에도 서비스 지속 가능하도록 폴백 처리 |
| **작업 유형** | AI |
| **의존성** | AI-02 완료 |

### 구현 내용

#### 1. 재시도 로직 데코레이터 구현
```python
def retry_on_failure(max_retries: int = 2, delay: float = 1.0):
    """
    AI API 호출 실패 시 재시도 데코레이터
    - max_retries: 최대 재시도 횟수
    - delay: 재시도 간 대기 시간 (지수 백오프 적용)
    """
    # RateLimitError: 지수 백오프 (delay * 2^attempt)
    # APITimeoutError, APIConnectionError: 선형 백오프
    # 기타 예외: 일반 대기
```

#### 2. OpenAI 클라이언트 타임아웃 설정
```python
self.client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=30.0,  # 30초 타임아웃
    max_retries=0,  # OpenAI 내부 재시도 비활성화 (우리 데코레이터 사용)
)
```

#### 3. Rate Limit 및 연결 에러 전용 처리
- `RateLimitError`: 재시도 후 폴백
- `APITimeoutError`: 재시도 후 폴백
- `APIConnectionError`: 재시도 후 폴백

#### 4. API 호출 메서드 분리
- `_call_summary_api()`, `_call_tags_api()`, `_call_category_api()`: 실제 API 호출
- `_call_*_api_with_retry()`: 재시도 데코레이터 적용
- `generate_*()`: 폴백 처리 포함 공개 메서드

### 테스트 결과 체크
- [x] AI03-TC01: 정상 동작 확인 (API 호출 성공)
- [x] AI03-TC02: 재시도 로직 동작 확인 (14개 유닛 테스트 통과)
- [x] AI03-TC03: 폴백 요약 반환 확인
- [x] AI03-TC04: 폴백 태그 반환 확인

### 테스트 파일
- `server/tests/test_ai_fallback.py`: 14개 테스트 케이스
  - `TestRetryDecorator`: 재시도 데코레이터 테스트 (3개)
  - `TestAIServiceFallback`: 폴백 함수 테스트 (8개)
  - `TestAIServiceAPIFallback`: API 실패 시 폴백 테스트 (3개)

### 참고 파일
- `server/app/services/ai.py`
- `server/tests/test_ai_fallback.py`

---

## TASK BE-03: 링크 삭제 API 구현 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 저장된 링크를 삭제할 수 있는 API 엔드포인트 구현 |
| **작업 유형** | 백엔드 |
| **의존성** | AI-03 완료 |

### 구현 내용

#### 1. Database 서비스에 삭제 메서드 추가
```python
# server/app/services/database.py
async def delete_link(self, link_id: str) -> bool:
    result = self.client.table('links').delete().eq('id', link_id).execute()
    return len(result.data) > 0
```

#### 2. API DELETE 엔드포인트 구현
```python
# server/app/api/links.py
@router.delete("/{link_id}")
async def delete_link(link_id: str):
    # 0. UUID 형식 검증
    try:
        uuid.UUID(link_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 링크 ID 형식입니다.")

    # 1. 링크 존재 확인
    link = await db_service.get_link_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다.")

    # 2. 삭제 실행
    success = await db_service.delete_link(link_id)
    if not success:
        raise HTTPException(status_code=500, detail="삭제에 실패했습니다.")

    return {"message": "삭제되었습니다.", "id": link_id}
```

### 테스트 결과 체크
- [x] BE03-TC01: 정상 삭제 성공 (200 응답)
- [x] BE03-TC02: 없는 링크 삭제 시 404 에러 반환
- [x] BE03-TC03: 잘못된 ID 형식 시 400 에러 반환

### 설계 결정
| 결정 사항 | 이유 |
|-----------|------|
| UUID 형식 검증 | 잘못된 형식의 ID로 DB 쿼리 방지, 명확한 에러 메시지 제공 |
| 존재 확인 후 삭제 | 삭제 전 링크 존재 여부 확인으로 명확한 에러 처리 |
| 로깅 추가 | 삭제 작업 추적 가능 |

### 참고 파일
- `server/app/api/links.py`
- `server/app/services/database.py`

---

## TASK BE-04: 링크 중복 저장 방지 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 동일한 URL 중복 저장 방지 |
| **작업 유형** | 백엔드 |
| **의존성** | BE-03 완료 |

### 구현 내용

#### 1. Database 서비스에 URL 조회 메서드 추가
```python
# server/app/services/database.py
async def get_link_by_url(self, url: str) -> Optional[dict]:
    """URL로 링크 조회 (중복 체크용)"""
    result = self.client.table('links').select('*').eq('url', url).execute()
    return result.data[0] if result.data else None
```

#### 2. 저장 로직에 중복 체크 추가
```python
# server/app/api/links.py
@router.post("/save", response_model=LinkResponse)
async def save_link(link: LinkCreate):
    url = link.url.strip()

    if not youtube_service.is_youtube_url(url):
        raise HTTPException(status_code=400, detail="현재는 유튜브 링크만 지원합니다.")

    # 1. URL 정규화
    normalized_url = youtube_service.normalize_youtube_url(url)

    # 2. 중복 체크
    existing = await db_service.get_link_by_url(normalized_url)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 저장된 링크입니다.",
            headers={"X-Existing-Link-Id": existing['id']}
        )

    # 3. 저장 진행 (정규화된 URL 사용)
    ...
```

### 테스트 결과 체크
- [x] BE04-TC01: 최초 저장 성공 (200 응답)
- [x] BE04-TC02: 중복 저장 시 409 에러 반환
- [x] BE04-TC03: 단축 URL 중복 감지 (youtu.be → youtube.com 정규화 후 비교)
- [x] BE04-TC04: URL 정규화 동작 확인 (5개 케이스)

### 설계 결정
| 결정 사항 | 이유 |
|-----------|------|
| URL 정규화 후 저장 | 다양한 형식의 YouTube URL을 표준 형식으로 통일 |
| 409 Conflict 응답 | HTTP 표준에 맞는 중복 리소스 응답 코드 |
| X-Existing-Link-Id 헤더 | 클라이언트가 기존 링크 ID를 알 수 있도록 |
| 정규화된 URL로 DB 저장 | 중복 체크 정확도 향상 |

### 테스트 파일
- `server/tests/test_duplicate_prevention.py`: 8개 테스트 케이스
  - `TestURLNormalization`: URL 정규화 테스트 (5개)
  - `TestDuplicatePrevention`: API 중복 방지 테스트 (3개)

### 참고 파일
- `server/app/api/links.py`
- `server/app/services/database.py`
- `server/app/services/youtube.py`

---

# PHASE 4: 앱 기능 구현

---

## TASK APP-01: 앱 환경 변수 및 API 연결 설정 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | Expo 앱에서 환경 변수를 통한 API URL 관리 |
| **작업 유형** | 앱 |
| **의존성** | BE-04 완료 |

### 구현 내용

#### 1. app.config.js 생성
```javascript
// app.config.js
export default {
  expo: {
    // ... 기존 설정
    extra: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/api',
    },
  },
};
```

#### 2. 환경 설정 모듈 생성
```typescript
// src/config/index.ts
import Constants from 'expo-constants';

const getConfig = () => ({
  apiBaseUrl: Constants.expoConfig?.extra?.apiBaseUrl || 'http://localhost:8000/api',
});

export const config = getConfig();
```

#### 3. API 서비스 수정
```typescript
// src/services/api.ts
import { config } from '../config';

const API_BASE_URL = config.apiBaseUrl;
// deleteLink API 추가
```

#### 4. 타입 선언 파일 추가
- `src/types/expo-constants.d.ts`: expo-constants 타입 정의

### 테스트 결과 체크
- [x] APP01-TC01: 환경 변수 로드 확인 (`env: load .env`)
- [x] APP01-TC02: TypeScript 타입 체크 통과
- [x] APP01-TC03: API 서비스 환경 변수 사용

### 설계 결정
| 결정 사항 | 이유 |
|-----------|------|
| app.config.js 사용 | Expo 공식 권장 방식, process.env 접근 가능 |
| config 모듈 분리 | 타입 안정성, 중앙 집중 관리 |
| expo-constants 타입 직접 정의 | 패키지 타입 누락 대응 |

### 참고 파일
- `app/app.config.js`
- `app/src/config/index.ts`
- `app/src/services/api.ts`
- `app/src/types/expo-constants.d.ts`
- `app/.env`

---

## TASK APP-02: 홈 화면 FAB 버튼 및 네비게이션 개선 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 홈 화면에서 링크 저장 화면으로 쉽게 이동, 저장 후 자동 복귀 |
| **작업 유형** | 앱 |
| **의존성** | APP-01 완료 |

### 구현 내용

#### 1. HomeScreen FAB 버튼 추가
```typescript
// FAB 버튼 컴포넌트
<TouchableOpacity style={styles.fab} onPress={handleAddLink}>
  <Text style={styles.fabText}>+</Text>
</TouchableOpacity>

// FAB 스타일
fab: {
  position: 'absolute',
  right: 20,
  bottom: 30,
  width: 56,
  height: 56,
  borderRadius: 28,
  backgroundColor: '#007AFF',
  // ... shadow styles
}
```

#### 2. useFocusEffect로 자동 새로고침
```typescript
import { useFocusEffect } from '@react-navigation/native';

useFocusEffect(
  useCallback(() => {
    fetchLinks();
  }, [fetchLinks])
);
```

#### 3. SaveLinkScreen 저장 후 자동 복귀
```typescript
// 저장 성공 후 1.5초 뒤 홈으로 이동
setTimeout(() => {
  navigation.goBack();
}, 1500);
```

### 테스트 결과 체크
- [x] APP02-TC01: FAB 버튼 표시 확인
- [x] APP02-TC02: FAB 클릭 시 SaveLink 화면 이동
- [x] APP02-TC03: 저장 완료 후 홈 화면 자동 복귀
- [x] APP02-TC04: 홈 화면 복귀 시 목록 자동 새로고침
- [x] APP02-TC05: TypeScript 타입 체크 통과

### 참고 파일
- `app/src/screens/HomeScreen.tsx`
- `app/src/screens/SaveLinkScreen.tsx`

---

## TASK APP-03: 링크 상세 화면 구현 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 저장된 링크의 상세 정보 확인 및 YouTube 열기/공유 기능 |
| **작업 유형** | 앱 |
| **의존성** | APP-02 완료 |

### 구현 내용

#### 1. LinkDetailScreen 생성
- 썸네일 이미지 (전체 너비)
- 제목 (굵은 글씨)
- 카테고리 배지 (파란색)
- 요약 섹션
- 태그 목록
- 저장일시

#### 2. 액션 버튼
```typescript
// YouTube에서 보기 (빨간색 버튼)
<TouchableOpacity style={styles.primaryButton} onPress={handleOpenLink}>
  <Text>YouTube에서 보기</Text>
</TouchableOpacity>

// 공유하기 (흰색 버튼)
<TouchableOpacity style={styles.secondaryButton} onPress={handleShare}>
  <Text>공유하기</Text>
</TouchableOpacity>
```

#### 3. 네비게이션 연결
```typescript
// App.tsx - 라우트 추가
<Stack.Screen name="LinkDetail" component={LinkDetailScreen} />

// HomeScreen - 카드 클릭 시 이동
<LinkCard
  link={item}
  onPress={() => navigation.navigate('LinkDetail', { link: item })}
/>
```

### 테스트 결과 체크
- [x] APP03-TC01: 상세 화면 표시 확인
- [x] APP03-TC02: 썸네일, 제목, 요약 표시
- [x] APP03-TC03: YouTube에서 보기 버튼 동작
- [x] APP03-TC04: 공유하기 버튼 동작
- [x] APP03-TC05: TypeScript 타입 체크 통과

### 참고 파일
- `app/src/screens/LinkDetailScreen.tsx` (신규)
- `app/src/screens/HomeScreen.tsx` (수정)
- `app/App.tsx` (수정)

---

## TASK APP-04: 링크 삭제 기능 (앱) ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 앱에서 저장된 링크 삭제 기능 구현 |
| **작업 유형** | 앱 |
| **의존성** | APP-03 완료, BE-03 (삭제 API) 완료 |

### 구현 내용

#### 1. 삭제 확인 Alert
```typescript
const handleDelete = () => {
  Alert.alert(
    '링크 삭제',
    '이 링크를 삭제하시겠습니까?\n삭제된 링크는 복구할 수 없습니다.',
    [
      { text: '취소', style: 'cancel' },
      { text: '삭제', style: 'destructive', onPress: deleteLink },
    ]
  );
};
```

#### 2. API 호출 및 결과 처리
```typescript
await linkApi.deleteLink(link.id);
Alert.alert('삭제 완료', '링크가 삭제되었습니다.', [
  { text: '확인', onPress: () => navigation.goBack() },
]);
```

#### 3. 삭제 버튼 UI
- 빨간 테두리 + 빨간 텍스트
- 삭제 중 로딩 인디케이터 표시
- disabled 상태 처리

### 테스트 결과 체크
- [x] APP04-TC01: 삭제 버튼 표시 확인
- [x] APP04-TC02: 삭제 확인 Alert 표시
- [x] APP04-TC03: 삭제 API 호출
- [x] APP04-TC04: 삭제 완료 후 홈 화면 복귀
- [x] APP04-TC05: TypeScript 타입 체크 통과

### 참고 파일
- `app/src/screens/LinkDetailScreen.tsx` (수정)

---

## TASK APP-05: Android 공유 인텐트 수신 구현 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | YouTube 앱에서 공유 시 링크 노트 앱에서 URL 수신 |
| **작업 유형** | 앱 |
| **의존성** | APP-04 완료 |

### 구현 내용

#### 1. expo-share-intent 설치
```bash
npm install expo-share-intent
```

#### 2. app.config.js 플러그인 설정
```javascript
plugins: [
  [
    'expo-share-intent',
    {
      androidIntentFilters: ['text/*'],
    },
  ],
],
```

#### 3. App.tsx ShareIntentProvider 적용
```typescript
import { ShareIntentProvider, useShareIntent } from 'expo-share-intent';

const AppNavigator = () => {
  const { hasShareIntent, shareIntent, resetShareIntent } = useShareIntent();

  useEffect(() => {
    if (hasShareIntent && shareIntent?.text) {
      const url = extractYouTubeUrl(shareIntent.text);
      if (url) {
        navigationRef.current?.navigate('SaveLink', { url });
        resetShareIntent();
      }
    }
  }, [hasShareIntent, shareIntent]);
  // ...
};

export default function App() {
  return (
    <ShareIntentProvider>
      <AppNavigator />
    </ShareIntentProvider>
  );
}
```

#### 4. SaveLinkScreen URL 파라미터 처리
```typescript
useEffect(() => {
  if (route.params?.url) {
    setUrl(route.params.url);
  }
}, [route.params?.url]);
```

### 테스트 결과 체크
- [x] APP05-TC01: expo-share-intent 설치 확인
- [x] APP05-TC02: TypeScript 타입 체크 통과
- [x] APP05-TC03: 공유 URL 추출 로직 구현
- [x] APP05-TC04: SaveLink 화면으로 URL 전달

### 참고
- 실제 Android 기기 테스트는 EAS Build 후 가능
- Development Build 필요 (expo-share-intent는 네이티브 코드 포함)

### 참고 파일
- `app/App.tsx` (수정)
- `app/app.config.js` (수정)
- `app/src/screens/SaveLinkScreen.tsx` (수정)

---

## TASK APP-06: iOS 공유 익스텐션 기본 설정 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | Safari/다른 앱에서 공유 시 링크 노트 앱에서 URL 수신 (iOS) |
| **작업 유형** | 앱 |
| **의존성** | APP-05 완료 |

### 구현 내용

#### app.config.js iOS Share Extension 설정
```javascript
plugins: [
  [
    'expo-share-intent',
    {
      // Android 설정
      androidIntentFilters: ['text/*'],
      // iOS Share Extension 설정
      iosShareExtensionName: 'LinkNoteShare',
      iosActivationRules: {
        NSExtensionActivationSupportsText: true,
        NSExtensionActivationSupportsWebURLWithMaxCount: 1,
      },
    },
  ],
],
```

### iOS 활성화 규칙 설명
- `NSExtensionActivationSupportsText`: 텍스트 공유 지원
- `NSExtensionActivationSupportsWebURLWithMaxCount`: URL 공유 지원 (최대 1개)

### 테스트 결과 체크
- [x] APP06-TC01: app.config.js 설정 추가
- [x] APP06-TC02: TypeScript 타입 체크 통과
- [x] APP06-TC03: APP-05 코드 재사용 확인

### 참고
- 실제 테스트는 **EAS Build** 필요
- iOS Share Extension은 별도 타겟으로 빌드됨
- expo-share-intent가 자동으로 Share Extension 생성

### 참고 파일
- `app/app.config.js` (수정)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01-19 | Initial archive creation with ENV-01 through AI-01 |
| 1.1 | 2024-01-20 | Added AI-02, AI-03 completion documentation |
| 1.2 | 2025-01-21 | Added BE-03 completion documentation |
| 1.3 | 2025-02-02 | Added BE-04 completion documentation |
| 1.4 | 2025-02-02 | Added APP-01 completion documentation |
| 1.5 | 2025-02-02 | Added APP-02 completion documentation |
| 1.6 | 2025-02-02 | Added APP-03 completion documentation |
| 1.7 | 2025-02-02 | Added APP-04 completion documentation |
| 1.8 | 2025-02-02 | Added APP-05 completion documentation |
| 1.9 | 2025-02-02 | Added APP-06 completion documentation |
| 2.0 | 2025-02-03 | Added APP-07 completion documentation |
| 2.1 | 2025-02-03 | Added APP-08 completion documentation |
| 2.2 | 2025-02-03 | Added APP-09 completion documentation |
| 2.3 | 2025-02-03 | Added SERVER-02 completion documentation |
| 2.4 | 2025-02-03 | Added APP-10 completion documentation |
| 2.5 | 2025-02-03 | Added APP-11 completion documentation |
| 3.0 | 2026-02-08 | Added DEPLOY-01~05 (PHASE 5) completion documentation |
| 3.1 | 2026-02-08 | Added AUTH-01 (PHASE 6) completion documentation |

---

## TASK APP-11: EAS Build 설정 및 APK/IPA 빌드 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | EAS Build 설정 완성 및 빌드 가이드 작성 |
| **작업 유형** | 앱 |
| **의존성** | APP-10 완료 |

### 구현 내용

#### 1. eas.json 빌드 프로파일
| 프로파일 | 용도 | 특징 |
|---------|------|------|
| `base` | 공통 설정 | Node 18.18.0, 환경 변수 |
| `development` | 개발용 | Dev Client, localhost API |
| `preview` | 내부 테스트 | APK 빌드, production API |
| `production` | 스토어 배포 | 자동 버전 증가, production API |

#### 2. package.json 빌드 스크립트
```json
{
  "build:dev": "eas build --profile development --platform all",
  "build:dev:android": "eas build --profile development --platform android",
  "build:dev:ios": "eas build --profile development --platform ios",
  "build:preview": "eas build --profile preview --platform all",
  "build:preview:android": "eas build --profile preview --platform android",
  "build:preview:ios": "eas build --profile preview --platform ios",
  "build:prod": "eas build --profile production --platform all",
  "build:prod:android": "eas build --profile production --platform android",
  "build:prod:ios": "eas build --profile production --platform ios"
}
```

#### 3. BUILD.md 가이드
- EAS CLI 설치 방법
- 빌드 명령어 모음
- iOS/Android 요구사항
- 문제 해결 가이드

### 테스트 결과 체크
- [x] APP11-TC01: eas.json 프로파일 완성
- [x] APP11-TC02: package.json 스크립트 추가
- [x] APP11-TC03: BUILD.md 가이드 작성
- [x] APP11-TC04: TypeScript 타입 체크 통과

### 참고 파일
- `app/eas.json` (수정)
- `app/package.json` (수정)
- `app/BUILD.md` (신규)

---

## TASK APP-10: 프로덕션 API URL 설정 및 빌드 테스트 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 프로덕션 환경 분리 및 EAS 빌드 설정 |
| **작업 유형** | 앱 |
| **의존성** | SERVER-02 완료 |

### 구현 내용

#### 1. 환경별 설정 파일
| 파일 | 용도 |
|------|------|
| `.env.development` | 개발 환경 (localhost) |
| `.env.production` | 프로덕션 환경 |
| `.env.example` | 환경 변수 예시 |

#### 2. eas.json 빌드 프로파일
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "env": { "API_BASE_URL": "http://localhost:8000/api" }
    },
    "preview": {
      "distribution": "internal",
      "env": { "API_BASE_URL": "https://linknote-api.up.railway.app/api" }
    },
    "production": {
      "env": { "API_BASE_URL": "https://linknote-api.up.railway.app/api" }
    }
  }
}
```

#### 3. app.config.js 업데이트
- APP_VARIANT에 따른 앱 이름 변경
- EAS project ID 설정 추가

### 테스트 결과 체크
- [x] APP10-TC01: 환경별 .env 파일 생성
- [x] APP10-TC02: eas.json 생성
- [x] APP10-TC03: app.config.js 업데이트
- [x] APP10-TC04: TypeScript 타입 체크 통과
- [x] APP10-TC05: Expo config 검증 통과

### 참고 파일
- `app/.env.development` (신규)
- `app/.env.production` (신규)
- `app/eas.json` (신규)
- `app/app.config.js` (수정)
- `app/.env.example` (수정)

---

## TASK SERVER-02: 서버 배포 (Railway/Render) ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | FastAPI 서버 클라우드 배포 설정 |
| **작업 유형** | 서버 |
| **의존성** | APP-09 완료 |

### 구현 내용

#### 1. 생성된 파일
| 파일 | 용도 |
|------|------|
| `Procfile` | 서버 시작 커맨드 |
| `runtime.txt` | Python 버전 (3.11.7) |
| `railway.json` | Railway 플랫폼 설정 |
| `render.yaml` | Render 플랫폼 설정 |
| `DEPLOY.md` | 배포 가이드 문서 |
| `.gitignore` | Git 제외 파일 |

#### 2. Procfile
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 3. railway.json
```json
{
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

#### 4. 필요한 환경 변수
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY`

### 테스트 결과 체크
- [x] SERVER02-TC01: Procfile 생성
- [x] SERVER02-TC02: runtime.txt 생성
- [x] SERVER02-TC03: railway.json 생성
- [x] SERVER02-TC04: render.yaml 생성
- [x] SERVER02-TC05: DEPLOY.md 가이드 작성
- [x] SERVER02-TC06: .gitignore 생성

### 참고 파일
- `server/Procfile` (신규)
- `server/runtime.txt` (신규)
- `server/railway.json` (신규)
- `server/render.yaml` (신규)
- `server/DEPLOY.md` (신규)
- `server/.gitignore` (신규)

---

## TASK APP-09: 앱 아이콘 및 스플래시 화면 설정 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 커스텀 앱 아이콘 및 스플래시 화면 설정 |
| **작업 유형** | 앱 |
| **의존성** | APP-08 완료 |

### 구현 내용

#### 1. 아이콘 생성 스크립트 (scripts/generate-icons.js)
- Jimp 라이브러리로 프로그래밍 방식 아이콘 생성
- 북마크 + 체인링크 디자인 컨셉

#### 2. 생성된 파일
| 파일 | 크기 | 용도 |
|------|------|------|
| `icon.png` | 1024x1024 | iOS/일반 앱 아이콘 |
| `adaptive-icon.png` | 1024x1024 | Android Adaptive Icon |
| `splash-icon.png` | 200x200 | 스플래시 화면 아이콘 |
| `favicon.png` | 48x48 | 웹 파비콘 |

#### 3. 디자인 사양
- 배경색: #007AFF (프라이머리 블루)
- 아이콘: 북마크 모양 + 체인 링크 심볼
- 접힌 모서리 효과로 입체감 표현
- Adaptive Icon: 투명 배경 + foreground 이미지

### 테스트 결과 체크
- [x] APP09-TC01: 아이콘 생성 스크립트 작성
- [x] APP09-TC02: icon.png 생성 (1024x1024)
- [x] APP09-TC03: adaptive-icon.png 생성
- [x] APP09-TC04: splash-icon.png 생성
- [x] APP09-TC05: favicon.png 생성

### 참고 파일
- `app/scripts/generate-icons.js` (신규)
- `app/assets/icon.png` (갱신)
- `app/assets/adaptive-icon.png` (갱신)
- `app/assets/splash-icon.png` (갱신)
- `app/assets/favicon.png` (갱신)

---

## TASK APP-08: 로딩 상태 및 스켈레톤 UI 구현 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 로딩 중 스켈레톤 UI로 사용자 경험 향상 |
| **작업 유형** | 앱 |
| **의존성** | APP-07 완료 |

### 구현 내용

#### 1. SkeletonCard 컴포넌트 (src/components/SkeletonCard.tsx)
```typescript
// Shimmer 애니메이션
const shimmerAnim = useRef(new Animated.Value(0)).current;

useEffect(() => {
  const shimmerLoop = Animated.loop(
    Animated.sequence([
      Animated.timing(shimmerAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.timing(shimmerAnim, {
        toValue: 0,
        duration: 1000,
        useNativeDriver: true,
      }),
    ])
  );
  shimmerLoop.start();
  return () => shimmerLoop.stop();
}, [shimmerAnim]);

const opacity = shimmerAnim.interpolate({
  inputRange: [0, 1],
  outputRange: [0.3, 0.7],
});
```

#### 2. SkeletonList 컴포넌트
```typescript
export const SkeletonList: React.FC<{ count?: number }> = ({ count = 3 }) => {
  return (
    <View style={styles.listContainer}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} />
      ))}
    </View>
  );
};
```

#### 3. HomeScreen 적용
```typescript
if (loading) {
  return <SkeletonList count={3} />;
}
```

### 스켈레톤 구조
- 썸네일: 100% x 180px
- 제목: 2줄 (90%, 60%)
- 요약: 2줄 (100%, 80%)
- 태그: 3개 (60px, 60px, 45px)
- 날짜: 80px

### 테스트 결과 체크
- [x] APP08-TC01: SkeletonCard 컴포넌트 생성
- [x] APP08-TC02: Shimmer 애니메이션 구현
- [x] APP08-TC03: HomeScreen 적용
- [x] APP08-TC04: TypeScript 타입 체크 통과

### 참고 파일
- `app/src/components/SkeletonCard.tsx` (신규)
- `app/src/screens/HomeScreen.tsx` (수정)

---

## TASK APP-07: 에러 처리 및 토스트 메시지 시스템 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 사용자 친화적인 피드백 시스템 구현 (Toast 메시지) |
| **작업 유형** | 앱 |
| **의존성** | APP-06 완료 |

### 구현 내용

#### 1. Toast 유틸리티 (src/utils/toast.ts)
```typescript
import Toast from 'react-native-toast-message';

export const showToast = {
  success: (message: string, description?: string) => {
    Toast.show({
      type: 'success',
      text1: message,
      text2: description,
      position: 'bottom',
      visibilityTime: 3000,
    });
  },

  error: (message: string, description?: string) => {
    Toast.show({
      type: 'error',
      text1: message,
      text2: description,
      position: 'bottom',
      visibilityTime: 4000,
    });
  },

  info: (message: string, description?: string) => {
    Toast.show({
      type: 'info',
      text1: message,
      text2: description,
      position: 'bottom',
      visibilityTime: 3000,
    });
  },
};
```

#### 2. SaveLinkScreen 수정
- URL 미입력 시: `showToast.error('URL을 입력해주세요.')`
- 저장 성공 시: `showToast.success('저장 완료!', result.title)`
- 저장 실패 시: `showToast.error('링크 저장 실패', message)`

#### 3. LinkDetailScreen 수정
- 삭제 확인: Alert 유지 (사용자 확인 필요)
- 삭제 성공 시: `showToast.success('삭제 완료', '링크가 삭제되었습니다.')`
- 삭제 실패 시: `showToast.error('삭제 실패', message)`

### 설계 결정
- **Toast**: 비침투적 피드백 (성공/에러/정보 메시지)
- **Alert**: 사용자 확인이 필요한 중요 액션 (삭제 확인)
- **position: 'bottom'**: 사용자 시야 방해 최소화
- **visibilityTime**: 에러(4초) > 성공/정보(3초)

### 테스트 결과 체크
- [x] APP07-TC01: Toast 유틸리티 생성
- [x] APP07-TC02: SaveLinkScreen Alert → Toast 변경
- [x] APP07-TC03: LinkDetailScreen Alert → Toast 변경
- [x] APP07-TC04: TypeScript 타입 체크 통과

### 참고 파일
- `app/src/utils/toast.ts` (신규)
- `app/src/screens/SaveLinkScreen.tsx` (수정)
- `app/src/screens/LinkDetailScreen.tsx` (수정)

---

# PHASE 5: 실기기 테스트 배포

---

## TASK DEPLOY-01: GitHub 푸시 및 서버 실제 배포 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 백엔드 서버를 클라우드에 실제 배포하여 스마트폰에서 접근 가능하게 함 |
| **작업 유형** | 배포 |
| **의존성** | APP-11 완료 |

### 구현 내용

#### 1. GitHub 저장소 코드 푸시
- 전체 프로젝트 코드를 GitHub에 푸시 완료

#### 2. Railway 클라우드 배포
- 플랫폼: Railway
- Root Directory: `server`
- 빌드 방식: Railpack (자동 감지)
- 서버 URL: `https://linknote-api.up.railway.app`

#### 3. 환경 변수 설정
| 변수명 | 용도 |
|--------|------|
| `SUPABASE_URL` | Supabase 프로젝트 URL |
| `SUPABASE_KEY` | Supabase anon key |
| `OPENAI_API_KEY` | OpenAI API 키 |

### 테스트 결과 체크
- [x] DP01-TC01: 헬스 체크 (`/health`) 정상 응답
- [x] DP01-TC02: API 루트 (`/`) 서비스 정보 JSON 반환
- [x] DP01-TC03: 링크 저장 POST 요청 정상 동작
- [x] DP01-TC04: 링크 목록 조회 정상 동작

### 트러블슈팅
- `railway.json`에서 NIXPACKS 빌더 명시 제거 → Railpack 자동 호환 적용

### 참고 파일
- `server/railway.json` (수정)
- `server/Procfile`
- `server/requirements.txt`

---

## TASK DEPLOY-02: Expo 계정 및 EAS 프로젝트 설정 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | EAS Build를 사용하기 위한 Expo 계정 및 프로젝트 초기화 |
| **작업 유형** | 설정 |
| **의존성** | DEPLOY-01 완료 |

### 구현 내용

#### 1. EAS CLI 설치 및 로그인
```bash
npm install -g eas-cli
eas login
```

#### 2. EAS 프로젝트 초기화
```bash
eas init
eas project:info
```
- `eas init` 실행 시 자동으로 `app.config.js`의 `eas.projectId` 업데이트

### 테스트 결과 체크
- [x] DP02-TC01: `eas whoami` - 계정 이름 정상 출력
- [x] DP02-TC02: `eas project:info` - 프로젝트 ID 정상 출력

---

## TASK DEPLOY-03: 빌드 전 코드 수정 (플러그인 활성화 등) ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | EAS Build 전 필수 코드 수정 (주석 해제, ID 설정 등) |
| **작업 유형** | 코드 수정 |
| **의존성** | DEPLOY-02 완료 |

### 구현 내용

#### 1. app.config.js 수정
- EAS Project ID 실제 값으로 교체
- `expo-share-intent` 플러그인 주석 해제 (Expo Go → EAS Build 전환)
- `ShareIntentProvider` 활성화

#### 2. expo-share-intent 플러그인 설정
```javascript
plugins: [
  [
    'expo-share-intent',
    {
      androidIntentFilters: ['text/*'],
      iosShareExtensionName: 'LinkNoteShare',
      iosActivationRules: {
        NSExtensionActivationSupportsText: true,
        NSExtensionActivationSupportsWebURLWithMaxCount: 1,
      },
    },
  ],
],
```

#### 3. eas.json API URL 확인
- preview/production 프로파일의 `API_BASE_URL`이 실제 배포 서버 URL과 일치 확인

#### 4. 공유 시 자동 저장 기능 추가
- 공유 인텐트 수신 시 자동 저장 로직 추가

### 테스트 결과 체크
- [x] DP03-TC01: Expo 설정 검증 (`npx expo config`) 에러 없음
- [x] DP03-TC02: TypeScript 체크 통과
- [x] DP03-TC03: EAS Project ID 실제 값 확인

### 참고 파일
- `app/app.config.js` (수정)
- `app/eas.json` (확인)
- `app/App.tsx` (수정)

---

## TASK DEPLOY-04: Android APK 빌드 (EAS Build) ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 스마트폰에 설치할 수 있는 APK 파일 빌드 |
| **작업 유형** | 빌드 |
| **의존성** | DEPLOY-03 완료 |

### 구현 내용

#### 1. Preview 프로파일로 APK 빌드
```bash
npm run build:preview:android
# 또는: eas build --profile preview --platform android
```

#### 2. 빌드 프로파일 (preview)
| 설정 | 값 |
|------|-----|
| distribution | internal |
| build type | apk |
| API URL | `https://linknote-api.up.railway.app/api` |
| Node 버전 | 20.18.0 |

#### 3. 빌드 결과
- EAS 클라우드에서 빌드 진행 (로컬 환경 무관)
- 빌드 완료 후 다운로드 링크 제공

### 테스트 결과 체크
- [x] DP04-TC01: 빌드 큐에 정상 등록
- [x] DP04-TC02: 빌드 상태 Finished
- [x] DP04-TC03: APK 파일 다운로드 완료

### 참고
- Node 버전을 20.18.0으로 맞추어 EAS Build 호환성 확보
- EAS Update 설정으로 향후 OTA 업데이트 가능

---

## TASK DEPLOY-05: 스마트폰 설치 및 전체 기능 테스트 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | APK를 스마트폰에 설치하고 모든 기능이 정상 작동하는지 검증 |
| **작업 유형** | 테스트 |
| **의존성** | DEPLOY-04 완료 |

### 테스트 결과 (20/20 통과)

#### A. 기본 기능 테스트
- [x] DP05-TC01: 앱 실행 (스플래시 → 홈 화면)
- [x] DP05-TC02: 빈 상태 화면 + FAB 버튼
- [x] DP05-TC03: FAB 버튼 → SaveLink 화면 이동

#### B. 링크 저장 테스트
- [x] DP05-TC04: URL 직접 입력 → 저장 성공
- [x] DP05-TC05: 로딩 스켈레톤 UI 표시
- [x] DP05-TC06: 링크 카드 (썸네일, 제목, 요약, 태그)
- [x] DP05-TC07: 중복 저장 방지 에러 토스트
- [x] DP05-TC08: 빈 URL 입력 에러 토스트

#### C. 링크 상세 화면 테스트
- [x] DP05-TC09: 상세 화면 표시
- [x] DP05-TC10: YouTube에서 보기 버튼
- [x] DP05-TC11: 공유하기 버튼

#### D. 링크 삭제 테스트
- [x] DP05-TC12: 삭제 확인 Alert 표시
- [x] DP05-TC13: 삭제 취소
- [x] DP05-TC14: 삭제 실행 → 홈 복귀

#### E. 공유 인텐트 테스트
- [x] DP05-TC15: YouTube 앱에서 공유 → URL 수신
- [x] DP05-TC16: 공유 후 자동 저장
- [x] DP05-TC17: 브라우저에서 공유 → URL 수신

#### F. AI 기능 확인
- [x] DP05-TC18: AI 요약 품질 (20~50자 한국어)
- [x] DP05-TC19: AI 태그 관련성
- [x] DP05-TC20: AI 카테고리 분류

---

# PHASE 6: 인증 + 멀티 플랫폼 + 카테고리 확장

---

## TASK AUTH-01: Supabase Auth 스키마 + 서버 인증 미들웨어 ✅

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | Supabase Auth 기반 사용자 인증 시스템의 서버 측 구현 |
| **작업 유형** | 서버 |
| **의존성** | 없음 (PHASE 6 첫 번째 태스크) |

### 구현 내용

#### 1. JWT 검증 미들웨어 (server/app/core/auth.py)
```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    payload = jwt.decode(
        token, settings.SUPABASE_JWT_SECRET,
        algorithms=["HS256"], audience="authenticated",
    )
    user_id = payload.get("sub")
    return user_id
```
- Bearer 토큰에서 HS256 디코딩 → user_id(sub) 추출
- 만료/무효 토큰 시 `AuthenticationError(401)` 발생

#### 2. 환경변수 추가 (config.py)
| 변수 | 용도 |
|------|------|
| `SUPABASE_SERVICE_KEY` | service role key (RLS 우회) |
| `SUPABASE_JWT_SECRET` | JWT 토큰 검증용 시크릿 |

#### 3. 인증 예외 클래스 (exceptions.py)
```python
class AuthenticationError(LinkNoteException):
    def __init__(self, message="인증이 필요합니다."):
        super().__init__(message, status_code=401, error_type="authentication_error")
```

#### 4. API 엔드포인트 보호 (api/links.py)
- `POST /save` → `user_id = Depends(get_current_user)`
- `GET /` → `user_id = Depends(get_current_user)`
- `GET /{link_id}` → `user_id = Depends(get_current_user)`
- `DELETE /{link_id}` → `user_id = Depends(get_current_user)`

#### 5. 사용자별 데이터 격리 (database.py)
- 모든 메서드에 `user_id` 파라미터 추가
- `.eq('user_id', user_id)` 필터 적용
- service key 사용 시 RLS 우회 + 서버 측 수동 필터링
- 중복 체크도 사용자별 (`get_link_by_url(url, user_id)`)

#### 6. 모델 업데이트 (models/link.py)
- `LinkResponse`에 `user_id: str` 필드 추가

#### 7. 예외 핸들러 (main.py)
- `AuthenticationError` 전용 핸들러 + `WWW-Authenticate: Bearer` 헤더

#### 8. DB 스키마 (supabase_schema.sql)
```sql
-- user_id 컬럼 + RLS 정책
user_id UUID NOT NULL REFERENCES auth.users(id)
CREATE POLICY "Users read own links" ON links FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own links" ON links FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users delete own links" ON links FOR DELETE USING (auth.uid() = user_id);
```

#### 9. 보안 조치
- `.env.example`에 노출된 실제 API 키 → 플레이스홀더로 교체
- `PyJWT>=2.8.0` 의존성 추가

### 인증 방식
- 서버는 `SUPABASE_SERVICE_KEY`(service role)로 Supabase 접근 (RLS 우회)
- JWT를 직접 디코딩하여 user_id 추출 → Supabase API 호출 없이 빠름
- 클라이언트별 데이터 격리는 쿼리 필터링으로 처리

### 변경 파일 (11개)
| 파일 | 변경 |
|------|------|
| **신규** `server/app/core/auth.py` | JWT 검증 Dependency |
| **신규** `server/tests/test_auth.py` | 9개 테스트 케이스 |
| `server/app/core/config.py` | JWT_SECRET, SERVICE_KEY 추가 |
| `server/app/core/exceptions.py` | AuthenticationError 추가 |
| `server/app/api/links.py` | 인증 Dependency 적용 |
| `server/app/services/database.py` | user_id 필터링 |
| `server/app/models/link.py` | user_id 필드 추가 |
| `server/main.py` | 인증 예외 핸들러 |
| `server/requirements.txt` | PyJWT 추가 |
| `server/.env.example` | 플레이스홀더 교체 |
| `server/supabase_schema.sql` | user_id + RLS 정책 |

### 테스트 결과 체크 (9/9 PASSED)
- [x] AUTH01-TC01: Authorization 헤더 없으면 401
- [x] AUTH01-TC02: 잘못된 JWT면 401
- [x] AUTH01-TC02b: 만료된 JWT면 401
- [x] AUTH01-TC03: 유효한 JWT에서 user_id 정상 추출
- [x] AUTH01-TC04: User A가 User B의 링크 목록 조회 불가
- [x] AUTH01-TC04b: User A가 User B의 링크 ID 조회 불가
- [x] AUTH01-TC05: 같은 URL 다른 사용자 각각 저장 가능
- [x] AUTH01-추가1: 루트 엔드포인트 인증 불필요
- [x] AUTH01-추가2: 헬스 엔드포인트 인증 불필요

### 배포 전 수동 작업
1. Supabase SQL Editor에서 마이그레이션 실행 (user_id 컬럼 + RLS 정책)
2. Railway 환경변수에 `SUPABASE_SERVICE_KEY`, `SUPABASE_JWT_SECRET` 추가
3. 기존 데이터에 user_id 할당 (첫 사용자 생성 후)

### 참고 파일
- `server/app/core/auth.py` (신규)
- `server/tests/test_auth.py` (신규)
- `server/app/core/config.py` (수정)
- `server/app/core/exceptions.py` (수정)
- `server/app/api/links.py` (수정)
- `server/app/services/database.py` (수정)
- `server/app/models/link.py` (수정)
- `server/main.py` (수정)
- `server/requirements.txt` (수정)
- `server/.env.example` (수정)
- `server/supabase_schema.sql` (수정)
