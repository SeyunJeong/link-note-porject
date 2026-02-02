# 링크 노트 태스크 단위 작업 계획서

> 이 문서는 프롬프트를 초기화하면서 작업할 수 있도록, 각 태스크가 독립적으로 실행 가능하게 구성되어 있습니다.
> 각 태스크는 해당 섹션만 읽고도 작업을 완료할 수 있도록 충분한 컨텍스트를 포함합니다.

---

## 작업 현황 체크리스트

| 순서 | 태스크 ID | 태스크명 | 상태 | 테스트 | 의존성 |
|------|-----------|----------|------|--------|--------|
| 1 | ENV-01 | 서버 환경 변수 및 설정 구성 | ✅ 완료 | ✅ | 없음 |
| 2 | DB-01 | Supabase 프로젝트 생성 및 테이블 설정 | ✅ 완료 | ✅ | ENV-01 |
| 3 | SERVER-01 | 서버 로컬 실행 및 기본 API 테스트 | ✅ 완료 | ✅ | DB-01 |
| 4 | BE-01 | YouTube 메타데이터 추출 개선 | ✅ 완료 | ✅ | SERVER-01 |
| 5 | BE-02 | 서버 에러 핸들링 및 로깅 시스템 | ✅ 완료 | ✅ | BE-02 |
| 6 | AI-01 | AI 요약 프롬프트 최적화 | ✅ 완료 | ✅ | BE-02 |
| 7 | AI-02 | AI 태그 및 카테고리 분류 개선 | ✅ 완료 | ✅ | AI-01 |
| 8 | AI-03 | AI 요청 실패 시 폴백 처리 | ✅ 완료 | ✅ | AI-02 |
| 9 | BE-03 | 링크 삭제 API 구현 | ✅ 완료 | ✅ | AI-03 |
| 10 | BE-04 | 링크 중복 저장 방지 | ⬜ 대기 | ⬜ | BE-03 |
| 11 | APP-01 | 앱 환경 변수 및 API 연결 설정 | ⬜ 대기 | ⬜ | BE-04 |
| 12 | APP-02 | 홈 화면 FAB 버튼 및 네비게이션 개선 | ⬜ 대기 | ⬜ | APP-01 |
| 13 | APP-03 | 링크 상세 화면 구현 | ⬜ 대기 | ⬜ | APP-02 |
| 14 | APP-04 | 링크 삭제 기능 (앱) | ⬜ 대기 | ⬜ | APP-03 |
| 15 | APP-05 | Android 공유 인텐트 수신 구현 | ⬜ 대기 | ⬜ | APP-04 |
| 16 | APP-06 | iOS 공유 익스텐션 기본 설정 | ⬜ 대기 | ⬜ | APP-05 |
| 17 | APP-07 | 에러 처리 및 토스트 메시지 시스템 | ⬜ 대기 | ⬜ | APP-06 |
| 18 | APP-08 | 로딩 상태 및 스켈레톤 UI 구현 | ⬜ 대기 | ⬜ | APP-07 |
| 19 | APP-09 | 앱 아이콘 및 스플래시 화면 설정 | ⬜ 대기 | ⬜ | APP-08 |
| 20 | SERVER-02 | 서버 배포 (Railway/Render) | ⬜ 대기 | ⬜ | APP-09 |
| 21 | APP-10 | 프로덕션 API URL 설정 및 빌드 테스트 | ⬜ 대기 | ⬜ | SERVER-02 |
| 22 | APP-11 | EAS Build 설정 및 APK/IPA 빌드 | ⬜ 대기 | ⬜ | APP-10 |

**상태 범례**: ⬜ 대기 | 🔄 진행중 | ✅ 완료 | ❌ 실패

---

## ⚠️ 작업 주의사항

1. **작업 완료 후 노션 문서화 필수**
   - 각 태스크 완료 후 [노션 Task 페이지](https://www.notion.so/Task-2ed96b78642980bb8314e7cc97eb42de)에 새 페이지를 생성하여 다음 내용을 작성합니다:
     - 작업 내용 요약
     - 완성도 (%)
     - 개선점
     - 인사이트

2. **태스크 처리 원칙**
   - 별도 요청이 없으면 **한 번에 하나의 태스크만** 처리합니다
   - 다음 태스크 진행 전 사용자 확인을 받습니다

3. **완료된 작업 아카이브**
   - 작업이 완료되면 해당 작업의 상세 내용은 `COMPLETED_TASKS.md` 파일로 이동합니다
   - 이 파일에는 체크리스트와 다음 작업에 필요한 컨텍스트만 유지합니다

4. **TASKS.md 최신화 체크**
   - 각 작업이 끝날 때마다 이 파일의 상태가 최신화되어 있는지 확인합니다
   - 체크리스트 상태 업데이트 확인
   - 불필요한 내용 정리 확인

---

## 완료된 작업 요약

> 상세 내용은 `COMPLETED_TASKS.md` 파일 참조

### PHASE 1: 환경 설정 ✅
- **ENV-01**: `.env` 파일 생성, Supabase/OpenAI 키 설정
- **DB-01**: Supabase `links` 테이블 생성, RLS 정책 적용
- **SERVER-01**: FastAPI 서버 실행 확인, 기본 API 테스트 통과

### PHASE 2: 백엔드 기능 개선 ✅
- **BE-01**: YouTube 메타데이터 추출 개선
  - URL 유효성 검사, 정규화 함수 추가
  - 비공개/삭제/지역제한 영상 에러 처리
  - 재시도 로직 구현
- **BE-02**: 로깅 및 에러 핸들링 시스템 구축
  - `app/core/logging.py`: 구조화된 로깅
  - `app/core/exceptions.py`: 커스텀 예외 클래스
  - 전역 예외 핸들러 등록

### PHASE 3: AI 기능 개선 ✅
- **AI-01**: AI 요약 프롬프트 최적화 완료
- **AI-02**: AI 태그 및 카테고리 분류 개선 완료
- **AI-03**: AI 요청 실패 시 폴백 처리 완료
  - 재시도 데코레이터 (`retry_on_failure`)
  - OpenAI 클라이언트 타임아웃 설정 (30초)
  - Rate Limit / 연결 에러 전용 처리
  - 14개 유닛 테스트 통과

### PHASE 2 추가: 백엔드 기능 (계속)
- **BE-03**: 링크 삭제 API 구현 완료
  - `database.py`에 `delete_link()` 메서드 추가
  - `DELETE /api/links/{link_id}` 엔드포인트 구현
  - UUID 형식 검증 추가 (400 에러)
  - 존재하지 않는 링크 처리 (404 에러)
  - 3개 테스트 케이스 통과

---

# 다음 작업: BE-04

---

## TASK BE-04: 링크 중복 저장 방지

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 동일한 URL 중복 저장 방지 |
| **작업 유형** | 백엔드 |
| **의존성** | BE-03 완료 |

### 현재 상태
- 중복 체크 없이 저장
- 같은 URL 여러 번 저장 가능
- `normalize_youtube_url` 함수는 BE-01에서 이미 구현됨

### 작업 내용

#### 1. 중복 체크 메서드
```python
# server/app/services/database.py

async def get_link_by_url(self, url: str) -> Optional[dict]:
    result = self.client.table('links').select('*').eq('url', url).execute()
    return result.data[0] if result.data else None
```

#### 2. 저장 로직 수정
```python
# server/app/api/links.py

@router.post("/save", response_model=LinkResponse)
async def save_link(link: LinkCreate):
    # 1. URL 정규화
    normalized_url = youtube_service.normalize_youtube_url(link.url)

    # 2. 중복 체크
    existing = await db_service.get_link_by_url(normalized_url)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 저장된 링크입니다.",
            headers={"X-Existing-Link-Id": existing['id']}
        )

    # 3. 저장 진행
    ...
```

### 테스트 수행

#### 테스트 케이스
| TC-ID | 테스트 항목 | 입력/조건 | 예상 결과 |
|-------|-------------|-----------|-----------|
| BE04-TC01 | 최초 저장 | 새 URL | 201/200, 저장 성공 |
| BE04-TC02 | 중복 저장 시도 | 동일 URL | 409 Conflict |
| BE04-TC03 | 단축 URL 중복 | youtu.be 형식으로 중복 | 409 Conflict |
| BE04-TC04 | URL 정규화 | 다른 형식 같은 영상 | 동일하게 처리 |

#### 테스트 실행 방법
```bash
# TC01: 최초 저장
curl -X POST http://localhost:8000/api/links/save \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# TC02: 중복 저장 시도
curl -X POST http://localhost:8000/api/links/save \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
# 응답: 409 Conflict

# TC03: 단축 URL 중복
curl -X POST http://localhost:8000/api/links/save \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/dQw4w9WgXcQ"}'
# 응답: 409 Conflict (정규화 후 같은 URL)
```

### 테스트 결과 체크
- [ ] BE04-TC01: 최초 저장 성공
- [ ] BE04-TC02: 중복 시 409 에러
- [ ] BE04-TC03: 단축 URL 중복 감지
- [ ] BE04-TC04: URL 정규화 동작 확인

### 완료 조건
- [ ] 중복 체크 로직 구현
- [ ] 409 Conflict 응답 구현
- [ ] 모든 테스트 케이스 통과

### 참고 파일
- `server/app/api/links.py`
- `server/app/services/youtube.py`
- `server/app/services/database.py`

---

# PHASE 4: 앱 기능 구현

> APP-01 ~ APP-11 태스크는 백엔드 작업 완료 후 진행됩니다.
> 각 태스크의 상세 내용은 작업 시점에 추가됩니다.

### 간략 목록

| 태스크 ID | 제목 | 핵심 테스트 |
|-----------|------|-------------|
| APP-01 | 앱 환경 변수 및 API 연결 설정 | 앱-서버 통신 확인 |
| APP-02 | 홈 화면 FAB 버튼 및 네비게이션 개선 | FAB → SaveLink 화면 이동 |
| APP-03 | 링크 상세 화면 구현 | 카드 클릭 → 상세 화면 |
| APP-04 | 링크 삭제 기능 (앱) | 삭제 확인 → 삭제 실행 |
| APP-05 | Android 공유 인텐트 수신 | 유튜브 앱에서 공유 → URL 수신 |
| APP-06 | iOS 공유 익스텐션 기본 설정 | Safari에서 공유 → URL 수신 |
| APP-07 | 에러 처리 및 토스트 메시지 | 성공/실패 시 토스트 표시 |
| APP-08 | 로딩 상태 및 스켈레톤 UI | 로딩 중 스켈레톤 표시 |
| APP-09 | 앱 아이콘 및 스플래시 화면 | 커스텀 아이콘/스플래시 |
| SERVER-02 | 서버 배포 | 클라우드 URL에서 API 응답 |
| APP-10 | 프로덕션 API URL 설정 | 실제 디바이스에서 서버 통신 |
| APP-11 | EAS Build 설정 | APK/IPA 빌드 성공 |

---

## 부록: 태스크 실행 가이드

### 새 세션에서 태스크 시작하기

```
프로젝트: LinkNote (링크 노트)
경로: /Users/jeongseyun/Project/LinkNote

TASKS.md의 [태스크 ID] 작업을 진행해줘.

현재 상태:
- [이전 태스크 완료 여부]
- [관련 환경 정보]
```

### 태스크 완료 시 체크리스트

1. [ ] 모든 작업 내용 완료
2. [ ] 모든 테스트 케이스 실행
3. [ ] 테스트 결과 체크 완료
4. [ ] 작업 현황 체크리스트 상태 업데이트 (⬜ → ✅)
5. [ ] 테스트 열 업데이트 (⬜ → ✅)
6. [ ] 노션 문서화 페이지 작성
7. [ ] 완료된 작업 상세 내용 COMPLETED_TASKS.md로 이동
8. [ ] TASKS.md 최신화 확인

---

## 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2024-01-19 | 초기 작성 |
| 2.0 | 2024-01-19 | AI/백엔드 태스크 추가, 테스트 섹션 추가 |
| 3.0 | 2024-01-19 | 완료된 작업 아카이브 정책 추가, 토큰 최적화 |
