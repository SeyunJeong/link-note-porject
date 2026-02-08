# 링크 노트 태스크 단위 작업 계획서

> 이 문서는 프롬프트를 초기화하면서 작업할 수 있도록, 각 태스크가 독립적으로 실행 가능하게 구성되어 있습니다.
> 각 태스크는 해당 섹션만 읽고도 작업을 완료할 수 있도록 충분한 컨텍스트를 포함합니다.

---

## 작업 현황 체크리스트

> PHASE 1~5 완료 (27개 태스크) → 상세 내용은 `COMPLETED_TASKS.md` 참조

### PHASE 6: 인증 + 멀티 플랫폼 + 카테고리 확장

| 순서 | 태스크 ID | 태스크명 | 상태 | 테스트 | 노션 | 의존성 |
|------|-----------|----------|------|--------|------|--------|
| 28 | AUTH-01 | Supabase Auth 스키마 + 서버 인증 미들웨어 | ✅ 완료 | ✅ | ✅ | 없음 |
| 29 | AUTH-02 | 앱 로그인/회원가입 + Google OAuth | ⬜ 대기 | ⬜ | ⬜ | AUTH-01 |
| 30 | AUTH-03 | 앱-서버 JWT 연동 | ⬜ 대기 | ⬜ | ⬜ | AUTH-02 |
| 31 | CAT-01 | 듀얼 카테고리 시스템 + media_type | ⬜ 대기 | ⬜ | ⬜ | AUTH-01 |
| 32 | PLATFORM-01 | 멀티 플랫폼 메타데이터 추출기 | ⬜ 대기 | ⬜ | ⬜ | CAT-01 |
| 33 | PLATFORM-02 | 앱 UI 멀티 플랫폼 + 필터 칩 | ⬜ 대기 | ⬜ | ⬜ | PLATFORM-01 |

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
- **BE-01**: YouTube 메타데이터 추출 개선 (URL 유효성 검사, 정규화, 에러 처리)
- **BE-02**: 로깅 및 에러 핸들링 시스템 구축
- **BE-03**: 링크 삭제 API 구현 (`DELETE /api/links/{link_id}`)
- **BE-04**: 링크 중복 저장 방지 (URL 정규화, 409 Conflict)

### PHASE 3: AI 기능 개선 ✅
- **AI-01**: AI 요약 프롬프트 최적화 (20-50자 한국어 요약)
- **AI-02**: AI 태그 및 카테고리 분류 개선 (8개 카테고리)
- **AI-03**: AI 요청 실패 시 폴백 처리 (재시도 데코레이터, 타임아웃)

### PHASE 4: 앱 기능 구현 ✅
- **APP-01**: 앱 환경 변수 및 API 연결 설정
- **APP-02**: 홈 화면 FAB 버튼 및 네비게이션 개선
- **APP-03**: 링크 상세 화면 구현
- **APP-04**: 링크 삭제 기능 (앱)
- **APP-05**: Android 공유 인텐트 수신 구현
- **APP-06**: iOS 공유 익스텐션 기본 설정
- **APP-07**: 에러 처리 및 토스트 메시지 시스템
- **APP-08**: 로딩 상태 및 스켈레톤 UI 구현
- **APP-09**: 앱 아이콘 및 스플래시 화면 설정
- **SERVER-02**: 서버 배포 (Railway)
- **APP-10**: 프로덕션 API URL 설정 및 빌드 테스트
- **APP-11**: EAS Build 설정 및 APK/IPA 빌드

### PHASE 5: 실기기 테스트 배포 ✅
- **DEPLOY-01**: GitHub 푸시 및 Railway 서버 실제 배포
- **DEPLOY-02**: Expo 계정 및 EAS 프로젝트 설정
- **DEPLOY-03**: 빌드 전 코드 수정 (플러그인 활성화, ShareIntent 자동저장)
- **DEPLOY-04**: Android APK 빌드 (EAS Build preview 프로파일)
- **DEPLOY-05**: 스마트폰 설치 및 전체 기능 테스트 (20/20 통과)

---

## 현재 상태

> **PHASE 1~5 완료** (27개 태스크) / **PHASE 6 진행 중** (6개 태스크)

### 프로젝트 아키텍처
- **서버**: FastAPI + Supabase + OpenAI → Railway 배포 (`https://linknote-api.up.railway.app`)
- **앱**: React Native (Expo) → EAS Build로 APK 생성
- **핵심 플로우**: URL 공유 → 링크 노트 앱 수신 → AI 요약/태그/카테고리 → Supabase 저장

### PHASE 6: 인증 + 멀티 플랫폼 + 카테고리 확장

**목표:**
1. Supabase Auth 기반 로그인/회원가입 + Google OAuth
2. 매체별(YouTube/Instagram/...) + 주제별(개발/투자/...) 듀얼 카테고리
3. Instagram, Threads, X, TikTok 링크 저장 지원
4. 홈 화면 필터 칩 UI

**의존성 그래프:**
```
AUTH-01 → AUTH-02 → AUTH-03
AUTH-01 → CAT-01 → PLATFORM-01 → PLATFORM-02
```

---

## AUTH-02: 앱 로그인/회원가입 화면 + Google OAuth

### 목표
- `@supabase/supabase-js` 설치 (인증 전용)
- 이메일/비밀번호 로그인 및 회원가입 화면 구현
- Google OAuth 연동
- AuthContext로 인증 상태 관리
- 인증 여부에 따른 네비게이션 분기

### 사전 조건
- AUTH-01 완료 (서버 인증 미들웨어 동작)

### 설치 패키지
```
@supabase/supabase-js
@react-native-async-storage/async-storage
expo-web-browser (Google OAuth 브라우저 플로우)
```

### 파일 변경 목록
| 파일 | 변경 내용 |
|------|-----------|
| **신규** `app/src/services/supabase.ts` | Supabase 클라이언트 (auth 전용, AsyncStorage 어댑터) |
| **신규** `app/src/contexts/AuthContext.tsx` | user/session 상태, signUp/signIn/signInWithGoogle/signOut |
| **신규** `app/src/screens/LoginScreen.tsx` | 이메일/비밀번호 입력 + Google 로그인 버튼 |
| **신규** `app/src/screens/SignUpScreen.tsx` | 이메일/비밀번호/확인 입력 + 가입 |
| `app/App.tsx` | AuthProvider 래핑, `{user ? <AppStack /> : <AuthStack />}` 분기 |
| `app/src/config/index.ts` | supabaseUrl, supabaseAnonKey 추가 |
| `app/app.config.js` | Supabase 환경변수 노출 |

### Google OAuth 설정 (수동)
1. Google Cloud Console에서 OAuth 2.0 클라이언트 생성
2. Supabase Dashboard → Authentication → Providers → Google 활성화
3. 앱에서 `supabase.auth.signInWithOAuth({ provider: 'google' })` + expo-web-browser

### 테스트 케이스
| TC | 설명 | 예상 결과 |
|----|------|-----------|
| TC01 | 이메일 회원가입 | 확인 메시지 표시 |
| TC02 | 이메일 로그인 | Home 화면 이동 |
| TC03 | 잘못된 비밀번호 | 에러 메시지 표시 |
| TC04 | Google OAuth 플로우 | 로그인 성공 후 Home 이동 |
| TC05 | 앱 재시작 | 세션 유지 (자동 로그인) |
| TC06 | 로그아웃 | 로그인 화면 복귀 |

---

## AUTH-03: 앱-서버 JWT 연동

### 목표
- axios 인터셉터로 JWT 토큰 자동 첨부
- 401 응답 시 토큰 갱신 + 재요청
- 공유 인텐트 수신 시 인증 상태 확인

### 사전 조건
- AUTH-02 완료 (앱 로그인 동작)

### 파일 변경 목록
| 파일 | 변경 내용 |
|------|-----------|
| `app/src/services/api.ts` | request 인터셉터 (Bearer 토큰), response 인터셉터 (401 → 갱신/재요청) |
| `app/App.tsx` | 미인증 상태에서 공유 인텐트 → URL 대기열 저장 후 로그인 후 처리 |

### 인터셉터 로직
```
Request: getSession() → Bearer 토큰 첨부
Response 401: refreshSession() → 성공이면 재요청, 실패면 signOut()
```

### 테스트 케이스
| TC | 설명 | 예상 결과 |
|----|------|-----------|
| TC01 | API 요청 시 헤더 확인 | Bearer 토큰 포함 |
| TC02 | 만료된 토큰으로 요청 | 갱신 후 재요청 성공 |
| TC03 | 갱신 실패 | 로그인 화면 리다이렉트 |
| TC04 | 로그인 상태에서 공유 인텐트 | 자동 저장 정상 동작 |

---

## CAT-01: 듀얼 카테고리 시스템 + media_type

### 목표
- links 테이블에 `media_type` 컬럼 추가
- URL 도메인 기반 자동 매체 감지
- 기존 AI 프롬프트를 플랫폼 무관하게 수정
- 앱 Link 타입에 media_type 필드 추가

### 사전 조건
- AUTH-01 완료 (user_id 컬럼 적용 후)

### DB 마이그레이션 (Supabase SQL Editor에서 실행)
```sql
ALTER TABLE links ADD COLUMN media_type TEXT DEFAULT 'web';
UPDATE links SET media_type = 'youtube' WHERE url LIKE '%youtube.com%' OR url LIKE '%youtu.be%';
CREATE INDEX idx_links_media_type ON links(media_type);
```

### media_type 값
`youtube`, `instagram`, `threads`, `x`, `tiktok`, `web`

### 주제 카테고리 (기존 유지)
`개발`, `투자`, `건강`, `교육`, `엔터테인먼트`, `뉴스`, `라이프스타일`, `기타`

### 파일 변경 목록
| 파일 | 변경 내용 |
|------|-----------|
| **신규** `server/app/services/platform.py` | `detect_media_type(url)` - 도메인 패턴 매칭 |
| `server/app/api/links.py` | 저장 시 `detect_media_type()` 호출, DB에 전달 |
| `server/app/services/database.py` | `save_link()`에 media_type 필드 추가 |
| `server/app/models/link.py` | `media_type: str` 필드 추가 |
| `server/app/services/ai.py` | 프롬프트에서 "YouTube 영상" → "콘텐츠"로 변경, 폴백 태그 수정 |
| `app/src/types/link.ts` | Link 인터페이스에 `media_type: string` 추가 |

### 테스트 케이스
| TC | 설명 | 예상 결과 |
|----|------|-----------|
| TC01 | youtube.com URL | media_type = "youtube" |
| TC02 | youtu.be URL | media_type = "youtube" |
| TC03 | instagram.com URL | media_type = "instagram" |
| TC04 | threads.net URL | media_type = "threads" |
| TC05 | x.com / twitter.com URL | media_type = "x" |
| TC06 | tiktok.com URL | media_type = "tiktok" |
| TC07 | 기타 URL | media_type = "web" |
| TC08 | 저장된 링크 조회 | media_type 필드 포함 확인 |

---

## PLATFORM-01: 멀티 플랫폼 메타데이터 추출기

### 목표
- YouTube 전용 추출기를 전략 패턴으로 리팩토링
- yt-dlp 기반 추출 (YouTube/Instagram/TikTok/X)
- OpenGraph 기반 추출 (Threads/일반 웹)
- YouTube 전용 URL 게이트 제거 → 모든 URL 허용

### 사전 조건
- CAT-01 완료 (media_type 시스템 동작)

### 아키텍처
```
ContentMetadata (dataclass)
  ├─ title, description, thumbnail, platform
  └─ duration, author, view_count (optional)

MetadataExtractor (ABC)
  ├─ YtDlpExtractor: YouTube, Instagram, TikTok, X
  └─ OpenGraphExtractor: Threads, 일반 웹 (fallback)

MetadataExtractorFactory
  └─ get_extractor(url) → 적합한 추출기 반환
```

### 플랫폼별 전략
| 플랫폼 | 추출기 | 비고 |
|--------|--------|------|
| YouTube | YtDlpExtractor | 기존 youtube.py 로직 그대로 (검증됨) |
| Instagram/TikTok/X | YtDlpExtractor | 실패 시 OpenGraph fallback |
| Threads | OpenGraphExtractor | yt-dlp 미지원 |
| 기타 웹 | OpenGraphExtractor | og: 메타 태그 추출 |

### 파일 변경 목록
| 파일 | 변경 내용 |
|------|-----------|
| **신규** `server/app/services/metadata/__init__.py` | 패키지 |
| **신규** `server/app/services/metadata/base.py` | ContentMetadata, MetadataExtractor ABC |
| **신규** `server/app/services/metadata/ytdlp_extractor.py` | youtube.py 리팩토링, 멀티 플랫폼 |
| **신규** `server/app/services/metadata/opengraph_extractor.py` | httpx + BeautifulSoup으로 og: 태그 추출 |
| **신규** `server/app/services/metadata/extractor_factory.py` | 팩토리 클래스 |
| `server/app/api/links.py` | YouTube 전용 게이트 제거, 팩토리 사용 |
| `server/app/core/exceptions.py` | `MetadataExtractionError` 추가 |
| `server/requirements.txt` | `beautifulsoup4>=4.12.0` 추가 |

### 테스트 케이스
| TC | 설명 | 예상 결과 |
|----|------|-----------|
| TC01~04 | 각 플랫폼 URL can_handle 확인 | 올바른 추출기 매칭 |
| TC05 | 팩토리 추출기 선택 | 올바른 추출기 반환 |
| TC06~09 | 각 추출기별 메타데이터 추출 (mock) | title, description, thumbnail 포함 |
| TC10 | yt-dlp 실패 | OpenGraph fallback 동작 |
| TC11 | 비YouTube URL 저장 통합 테스트 | 정상 저장 |

---

## PLATFORM-02: 앱 UI 멀티 플랫폼 + 필터 칩

### 목표
- YouTube 하드코딩 제거
- LinkCard에 매체 뱃지 추가
- 상세 화면 동적 버튼/뱃지
- 홈 화면에 매체별 + 주제별 필터 칩
- 서버에 필터링 API 파라미터 추가

### 사전 조건
- PLATFORM-01 완료 (멀티 플랫폼 메타데이터 추출 동작)

### 플랫폼 설정
```typescript
PLATFORM_CONFIG = {
  youtube:   { label: 'YouTube',   color: '#FF0000' },
  instagram: { label: 'Instagram', color: '#E4405F' },
  threads:   { label: 'Threads',   color: '#000000' },
  x:         { label: 'X',         color: '#000000' },
  tiktok:    { label: 'TikTok',    color: '#010101' },
  web:       { label: 'Web',       color: '#4A90D9' },
}
```

### 홈 화면 필터 칩 UI
```
┌─────────────────────────────────────┐
│ [전체] [YouTube] [Instagram] [X] ...│  ← 매체별 필터 (수평 스크롤)
│ [전체] [개발] [투자] [건강] [교육]...│  ← 주제별 필터 (수평 스크롤)
├─────────────────────────────────────┤
│ LinkCard 1                          │
│ LinkCard 2                          │
│ ...                                 │
└─────────────────────────────────────┘
```

### 파일 변경 목록
| 파일 | 변경 내용 |
|------|-----------|
| **신규** `app/src/utils/platform.ts` | PLATFORM_CONFIG, getPlatformConfig() |
| **신규** `app/src/components/FilterChips.tsx` | 필터 칩 컴포넌트 (매체별/주제별) |
| `app/src/components/LinkCard.tsx` | 매체 뱃지 추가 (썸네일 위 또는 제목 옆) |
| `app/src/screens/HomeScreen.tsx` | 필터 칩 추가, 필터 상태 관리, API 호출에 필터 전달 |
| `app/src/screens/LinkDetailScreen.tsx` | "YouTube에서 보기" → 동적 플랫폼 버튼, 듀얼 뱃지 |
| `app/src/screens/SaveLinkScreen.tsx` | "유튜브 링크" → "링크", 플레이스홀더 변경 |
| `app/src/services/api.ts` | getLinks()에 media_type, category 필터 파라미터 추가 |
| `server/app/api/links.py` | GET /api/links/에 `media_type`, `category` 쿼리 파라미터 추가 |
| `server/app/services/database.py` | get_links()에 필터 조건 추가 |

### 테스트 케이스
| TC | 설명 | 예상 결과 |
|----|------|-----------|
| TC01 | 필터 칩 "전체" 선택 | 모든 링크 표시 |
| TC02 | YouTube 필터 선택 | YouTube 링크만 표시 |
| TC03 | 매체 + 주제 필터 조합 | 교집합 결과 표시 |
| TC04 | LinkCard 확인 | 플랫폼 뱃지 표시 |
| TC05 | 상세 화면 확인 | 동적 버튼 텍스트 ("Instagram에서 보기" 등) |
| TC06 | SaveLinkScreen 확인 | 범용 텍스트 ("링크를 입력하세요") |

---

## 부록: 태스크 실행 가이드

### 새 세션에서 태스크 시작하기

```
프로젝트: LinkNote (링크 노트)
경로: C:\Users\seyun\link-note-porject

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
| 4.0 | 2026-02-08 | PHASE 5 실기기 테스트 배포 계획 추가 (DEPLOY-01~05) |
| 5.0 | 2026-02-08 | PHASE 1~5 전체 완료, DEPLOY 상세 내용 COMPLETED_TASKS.md로 이동, 태스크 보드 정리 |
| 6.0 | 2026-02-08 | PHASE 6 태스크 추가 (AUTH-01~03, CAT-01, PLATFORM-01~02) |
