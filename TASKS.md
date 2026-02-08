# 링크 노트 태스크 단위 작업 계획서

> 이 문서는 프롬프트를 초기화하면서 작업할 수 있도록, 각 태스크가 독립적으로 실행 가능하게 구성되어 있습니다.
> 각 태스크는 해당 섹션만 읽고도 작업을 완료할 수 있도록 충분한 컨텍스트를 포함합니다.

---

## 작업 현황 체크리스트

| 순서 | 태스크 ID | 태스크명 | 상태 | 테스트 | 노션 | 의존성 |
|------|-----------|----------|------|--------|------|--------|
| 1 | ENV-01 | 서버 환경 변수 및 설정 구성 | ✅ 완료 | ✅ | ✅ | 없음 |
| 2 | DB-01 | Supabase 프로젝트 생성 및 테이블 설정 | ✅ 완료 | ✅ | ✅ | ENV-01 |
| 3 | SERVER-01 | 서버 로컬 실행 및 기본 API 테스트 | ✅ 완료 | ✅ | ✅ | DB-01 |
| 4 | BE-01 | YouTube 메타데이터 추출 개선 | ✅ 완료 | ✅ | ✅ | SERVER-01 |
| 5 | BE-02 | 서버 에러 핸들링 및 로깅 시스템 | ✅ 완료 | ✅ | ✅ | BE-02 |
| 6 | AI-01 | AI 요약 프롬프트 최적화 | ✅ 완료 | ✅ | ✅ | BE-02 |
| 7 | AI-02 | AI 태그 및 카테고리 분류 개선 | ✅ 완료 | ✅ | ✅ | AI-01 |
| 8 | AI-03 | AI 요청 실패 시 폴백 처리 | ✅ 완료 | ✅ | ✅ | AI-02 |
| 9 | BE-03 | 링크 삭제 API 구현 | ✅ 완료 | ✅ | ✅ | AI-03 |
| 10 | BE-04 | 링크 중복 저장 방지 | ✅ 완료 | ✅ | ✅ | BE-03 |
| 11 | APP-01 | 앱 환경 변수 및 API 연결 설정 | ✅ 완료 | ✅ | ✅ | BE-04 |
| 12 | APP-02 | 홈 화면 FAB 버튼 및 네비게이션 개선 | ✅ 완료 | ✅ | ✅ | APP-01 |
| 13 | APP-03 | 링크 상세 화면 구현 | ✅ 완료 | ✅ | ✅ | APP-02 |
| 14 | APP-04 | 링크 삭제 기능 (앱) | ✅ 완료 | ✅ | ✅ | APP-03 |
| 15 | APP-05 | Android 공유 인텐트 수신 구현 | ✅ 완료 | ✅ | ✅ | APP-04 |
| 16 | APP-06 | iOS 공유 익스텐션 기본 설정 | ✅ 완료 | ✅ | ✅ | APP-05 |
| 17 | APP-07 | 에러 처리 및 토스트 메시지 시스템 | ✅ 완료 | ✅ | ✅ | APP-06 |
| 18 | APP-08 | 로딩 상태 및 스켈레톤 UI 구현 | ✅ 완료 | ✅ | ✅ | APP-07 |
| 19 | APP-09 | 앱 아이콘 및 스플래시 화면 설정 | ✅ 완료 | ✅ | ✅ | APP-08 |
| 20 | SERVER-02 | 서버 배포 (Railway/Render) | ✅ 완료 | ✅ | ✅ | APP-09 |
| 21 | APP-10 | 프로덕션 API URL 설정 및 빌드 테스트 | ✅ 완료 | ✅ | ✅ | SERVER-02 |
| 22 | APP-11 | EAS Build 설정 및 APK/IPA 빌드 | ✅ 완료 | ✅ | ✅ | APP-10 |

| | | | | | | |
| **PHASE 5: 실기기 테스트 배포** | | | | | | |
| 23 | DEPLOY-01 | GitHub 푸시 및 서버 실제 배포 | ✅ 완료 | ✅ | ⬜ | APP-11 |
| 24 | DEPLOY-02 | Expo 계정 및 EAS 프로젝트 설정 | ✅ 완료 | ✅ | ⬜ | DEPLOY-01 |
| 25 | DEPLOY-03 | 빌드 전 코드 수정 (플러그인 활성화 등) | ✅ 완료 | ✅ | ⬜ | DEPLOY-02 |
| 26 | DEPLOY-04 | Android APK 빌드 (EAS Build) | ⬜ 대기 | ⬜ | ⬜ | DEPLOY-03 |
| 27 | DEPLOY-05 | 스마트폰 설치 및 전체 기능 테스트 | ⬜ 대기 | ⬜ | ⬜ | DEPLOY-04 |

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
- **BE-04**: 링크 중복 저장 방지 완료
  - `database.py`에 `get_link_by_url()` 메서드 추가
  - URL 정규화 후 중복 체크
  - 409 Conflict 응답 (X-Existing-Link-Id 헤더 포함)
  - 8개 테스트 케이스 통과

---

# 다음 작업: DEPLOY-01

---

# PHASE 5: 실기기 테스트 배포 (스마트폰에서 직접 사용하기)

> 개발 완료된 앱을 실제 스마트폰에 설치하여 모든 기능을 테스트하기 위한 단계입니다.
> Android 기기 기준으로 작성되었으며, iOS는 Apple Developer 계정이 필요합니다.

---

## TASK DEPLOY-01: GitHub 푸시 및 서버 실제 배포 ⬜

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 백엔드 서버를 클라우드에 실제 배포하여 스마트폰에서 접근 가능하게 함 |
| **작업 유형** | 배포 |
| **의존성** | APP-11 완료 |
| **소요 시간** | 약 20~30분 |

### 사전 준비
- [GitHub](https://github.com) 계정
- [Railway](https://railway.app) 계정 (GitHub 로그인 가능)
- Supabase URL, Key (기존 `.env`에 있음)
- OpenAI API Key (기존 `.env`에 있음)

### 작업 내용

#### 1. GitHub 저장소에 코드 푸시
```bash
cd C:\Users\seyun\link-note-porject
git add -A
git commit -m "Complete all development tasks"
git remote add origin https://github.com/[본인계정]/link-note-project.git
git push -u origin main
```
> **주의**: GitHub 저장소가 이미 연결되어 있다면 `git push origin main`만 실행

#### 2. Railway에 서버 배포
1. [Railway](https://railway.app)에 GitHub 계정으로 로그인
2. **New Project** → **Deploy from GitHub repo** 클릭
3. `link-note-project` 저장소 선택
4. **Root Directory**: `server` 입력 (중요!)
5. **Variables** 탭에서 환경 변수 추가:

| 변수명 | 값 |
|--------|-----|
| `SUPABASE_URL` | `server/.env`의 SUPABASE_URL 값 복사 |
| `SUPABASE_KEY` | `server/.env`의 SUPABASE_KEY 값 복사 |
| `OPENAI_API_KEY` | `server/.env`의 OPENAI_API_KEY 값 복사 |

6. **Deploy** 클릭 → 배포 완료 대기 (약 3~5분)

#### 3. 배포된 서버 URL 확인
- Railway 대시보드에서 배포된 서비스의 **Public URL** 확인
- 형식: `https://[서비스명].up.railway.app`

### 테스트 수행

#### 테스트 케이스
| TC-ID | 테스트 항목 | 방법 | 예상 결과 |
|-------|-------------|------|-----------|
| DP01-TC01 | 헬스 체크 | 브라우저에서 `https://[URL]/health` 접속 | `{"status": "healthy"}` |
| DP01-TC02 | API 루트 | 브라우저에서 `https://[URL]/` 접속 | 서비스 정보 JSON |
| DP01-TC03 | 링크 저장 테스트 | curl 또는 Postman으로 POST 요청 | 링크 데이터 반환 |
| DP01-TC04 | 링크 목록 조회 | 브라우저에서 `https://[URL]/api/links/` 접속 | 링크 배열 반환 |

#### 테스트 실행 (PowerShell)
```powershell
# TC01: 헬스 체크
Invoke-RestMethod -Uri "https://[URL]/health"

# TC02: API 루트
Invoke-RestMethod -Uri "https://[URL]/"

# TC03: 링크 저장
Invoke-RestMethod -Uri "https://[URL]/api/links/save" -Method Post -ContentType "application/json" -Body '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# TC04: 링크 목록
Invoke-RestMethod -Uri "https://[URL]/api/links/"
```

### 완료 조건
- [ ] GitHub에 코드 푸시됨
- [ ] Railway 배포 성공 (녹색 상태)
- [ ] 헬스 체크 응답 확인
- [ ] 링크 저장/조회 API 정상 동작
- [ ] 배포된 서버 URL 기록: `https://________________.up.railway.app`

### 트러블슈팅
| 문제 | 해결 방법 |
|------|-----------|
| 빌드 실패 | Railway 로그 확인 → `requirements.txt` 의존성 문제 가능 |
| 환경 변수 에러 | Variables 탭에서 키 이름/값 정확히 확인 |
| 헬스 체크 실패 | 서비스가 완전히 시작될 때까지 1~2분 대기 |
| yt-dlp 관련 에러 | Railway에서 yt-dlp 실행 가능한지 로그 확인 |

---

## TASK DEPLOY-02: Expo 계정 및 EAS 프로젝트 설정 ⬜

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | EAS Build를 사용하기 위한 Expo 계정 및 프로젝트 초기화 |
| **작업 유형** | 설정 |
| **의존성** | DEPLOY-01 완료 |
| **소요 시간** | 약 10~15분 |

### 사전 준비
- Node.js 설치되어 있어야 함
- npm 사용 가능해야 함

### 작업 내용

#### 1. Expo 계정 생성
- [expo.dev](https://expo.dev/signup) 에서 계정 생성 (무료)
- 또는 기존 계정이 있다면 로그인

#### 2. EAS CLI 설치 및 로그인
```bash
# EAS CLI 전역 설치
npm install -g eas-cli

# Expo 로그인
cd C:\Users\seyun\link-note-porject\app
eas login
# → Expo 계정 이메일/비밀번호 입력
```

#### 3. EAS 프로젝트 초기화
```bash
cd C:\Users\seyun\link-note-porject\app
eas init
```
- 이 명령이 실행되면 자동으로 EAS 프로젝트가 생성됨
- **projectId**가 출력됨 → 메모해둘 것

#### 4. EAS Project ID 확인
```bash
eas project:info
```
- 출력된 **Project ID**를 복사

### 테스트 수행

| TC-ID | 테스트 항목 | 방법 | 예상 결과 |
|-------|-------------|------|-----------|
| DP02-TC01 | EAS 로그인 | `eas whoami` | 계정 이름 출력 |
| DP02-TC02 | 프로젝트 연결 | `eas project:info` | 프로젝트 ID 출력 |

### 완료 조건
- [ ] Expo 계정 생성/로그인 완료
- [ ] EAS CLI 설치됨
- [ ] EAS 프로젝트 초기화 완료
- [ ] Project ID 확인: `____________________________________`

---

## TASK DEPLOY-03: 빌드 전 코드 수정 (플러그인 활성화 등) ⬜

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | EAS Build 전 필수 코드 수정 (주석 해제, ID 설정 등) |
| **작업 유형** | 코드 수정 |
| **의존성** | DEPLOY-02 완료 |
| **소요 시간** | 약 5~10분 |

### 현재 문제점
1. `app.config.js`의 `expo-share-intent` 플러그인이 주석 처리됨 (Expo Go 호환 때문)
2. `eas.projectId`가 플레이스홀더 값 (`your-eas-project-id`)
3. `eas.json`의 API URL이 실제 서버 URL과 일치하는지 확인 필요

### 작업 내용

#### 1. app.config.js - EAS Project ID 업데이트
```javascript
// 변경 전
eas: {
  projectId: 'your-eas-project-id',
},

// 변경 후 (DEPLOY-02에서 확인한 ID 사용)
eas: {
  projectId: '[실제 EAS 프로젝트 ID]',
},
```

#### 2. app.config.js - expo-share-intent 플러그인 주석 해제
```javascript
// 변경 전 (주석 처리됨)
// plugins: [
//   [
//     'expo-share-intent',
//     { ... },
//   ],
// ],

// 변경 후 (주석 해제)
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

#### 3. eas.json - API URL 확인
- `preview` 프로파일의 `API_BASE_URL`이 DEPLOY-01에서 배포한 서버 URL과 일치하는지 확인
- 일치하지 않으면 수정:
```json
"preview": {
  "env": {
    "API_BASE_URL": "https://[실제배포URL]/api"
  }
}
```

### 테스트 수행

| TC-ID | 테스트 항목 | 방법 | 예상 결과 |
|-------|-------------|------|-----------|
| DP03-TC01 | Expo 설정 검증 | `npx expo config --type public` | 에러 없이 설정 출력 |
| DP03-TC02 | TypeScript 체크 | `npx tsc --noEmit` | 에러 없음 |
| DP03-TC03 | EAS Project ID | config 출력에서 projectId 확인 | 실제 ID 표시 |

### 완료 조건
- [ ] EAS Project ID 실제 값으로 교체됨
- [ ] expo-share-intent 플러그인 주석 해제됨
- [ ] API URL이 실제 배포 서버와 일치함
- [ ] Expo 설정 검증 통과

### 참고 파일
- `app/app.config.js` (수정)
- `app/eas.json` (확인/수정)

---

## TASK DEPLOY-04: Android APK 빌드 (EAS Build) ⬜

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | 스마트폰에 설치할 수 있는 APK 파일 빌드 |
| **작업 유형** | 빌드 |
| **의존성** | DEPLOY-03 완료 |
| **소요 시간** | 약 15~30분 (EAS 클라우드 빌드) |

### 사전 준비
- DEPLOY-01 ~ DEPLOY-03 완료
- EAS CLI 로그인 상태 확인: `eas whoami`

### 작업 내용

#### 1. Preview 프로파일로 APK 빌드
```bash
cd C:\Users\seyun\link-note-porject\app
npm run build:preview:android
# 또는 직접 실행:
# eas build --profile preview --platform android
```

- EAS 클라우드에서 빌드가 진행됨 (로컬 PC 사양 무관)
- 빌드 상태를 터미널 또는 [expo.dev](https://expo.dev) 대시보드에서 확인 가능
- 완료까지 약 10~20분 소요

#### 2. 빌드 완료 후 APK 다운로드
빌드 완료 시 터미널에 다운로드 링크 표시:
```
Build complete!
Download: https://expo.dev/artifacts/eas/xxxxx.apk
```

**다운로드 방법 (택 1):**
- **(A) PC에서 다운로드 후 폰에 전송**: 링크 클릭 → APK 다운로드 → USB/카카오톡/구글드라이브로 전송
- **(B) 스마트폰에서 직접 다운로드**: QR 코드를 폰 카메라로 스캔 → 바로 다운로드

#### 3. (빌드 실패 시) 로그 확인
```bash
# 가장 최근 빌드 로그 확인
eas build:list
eas build:view [build-id]
```

### 테스트 수행

| TC-ID | 테스트 항목 | 방법 | 예상 결과 |
|-------|-------------|------|-----------|
| DP04-TC01 | 빌드 시작 | `npm run build:preview:android` 실행 | 빌드 큐에 등록됨 |
| DP04-TC02 | 빌드 완료 | EAS 대시보드 확인 | 빌드 상태 "Finished" |
| DP04-TC03 | APK 다운로드 | 다운로드 링크 접속 | APK 파일 다운로드됨 |

### 완료 조건
- [ ] EAS Build 성공 (Finished 상태)
- [ ] APK 파일 다운로드 완료
- [ ] APK 파일 크기 확인 (보통 30~80MB)

### 트러블슈팅
| 문제 | 해결 방법 |
|------|-----------|
| `eas: command not found` | `npm install -g eas-cli` 재설치 |
| 프로젝트 ID 에러 | `eas init` 재실행 |
| 빌드 실패 (dependency) | `npm install` 후 재빌드 |
| 빌드 큐 대기 오래 걸림 | EAS 무료 플랜은 큐 대기 있음, 5~15분 대기 정상 |
| expo-share-intent 에러 | 플러그인 주석 해제 여부 확인 (DEPLOY-03) |

### 참고
- **EAS 무료 플랜**: 월 30회 빌드 가능, 빌드 큐 대기 있음
- **preview 프로파일**: production API URL 사용, APK 포맷 (설치 파일)
- **development 프로파일**: localhost API → 실기기에서 사용 불가

---

## TASK DEPLOY-05: 스마트폰 설치 및 전체 기능 테스트 ⬜

### 개요
| 항목 | 내용 |
|------|------|
| **목적** | APK를 스마트폰에 설치하고 모든 기능이 정상 작동하는지 검증 |
| **작업 유형** | 테스트 |
| **의존성** | DEPLOY-04 완료 |
| **소요 시간** | 약 15~20분 |

### 사전 준비
- DEPLOY-04에서 빌드한 APK 파일
- Android 스마트폰 (Android 6.0 이상)
- 스마트폰에 YouTube 앱 설치되어 있어야 함

### 작업 내용

#### 1. APK 설치
1. APK 파일을 스마트폰으로 전송 (USB, 카카오톡, 구글 드라이브 등)
2. 파일 매니저에서 APK 파일 탭
3. "출처를 알 수 없는 앱 설치" 허용 팝업 → **허용**
4. 설치 완료 → **열기** 클릭

#### 2. 앱 최초 실행 확인
- 스플래시 화면 표시 확인
- 홈 화면 로딩 (빈 목록 상태)
- 커스텀 앱 아이콘 확인

### 테스트 수행 (전체 기능)

#### A. 기본 기능 테스트

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC01 | 앱 실행 | 앱 아이콘 탭 | 스플래시 → 홈 화면 표시 | ☐ |
| DP05-TC02 | 빈 상태 화면 | 첫 실행 시 홈 화면 확인 | 빈 상태 메시지 + FAB 버튼 표시 | ☐ |
| DP05-TC03 | FAB 버튼 이동 | + 버튼 탭 | SaveLink 화면으로 이동 | ☐ |

#### B. 링크 저장 테스트

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC04 | URL 직접 입력 | SaveLink 화면에서 YouTube URL 입력 후 저장 | 로딩 → 저장 성공 토스트 → 홈으로 복귀 | ☐ |
| DP05-TC05 | 로딩 스켈레톤 | 저장 후 홈 화면 로딩 시 | 스켈레톤 UI 표시 후 카드 표시 | ☐ |
| DP05-TC06 | 링크 카드 표시 | 홈 화면에서 저장된 링크 확인 | 썸네일, 제목, 요약, 태그 표시 | ☐ |
| DP05-TC07 | 중복 저장 방지 | 같은 URL 다시 저장 시도 | 에러 토스트 "이미 저장된 링크입니다" | ☐ |
| DP05-TC08 | 빈 URL 입력 | URL 비워두고 저장 클릭 | 에러 토스트 표시 | ☐ |

#### C. 링크 상세 화면 테스트

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC09 | 상세 화면 이동 | 홈에서 카드 탭 | 상세 화면 표시 (썸네일, 제목, 요약, 태그, 날짜) | ☐ |
| DP05-TC10 | YouTube 열기 | "YouTube에서 보기" 버튼 탭 | YouTube 앱 또는 브라우저에서 영상 열림 | ☐ |
| DP05-TC11 | 공유하기 | "공유하기" 버튼 탭 | 시스템 공유 시트 표시 | ☐ |

#### D. 링크 삭제 테스트

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC12 | 삭제 버튼 탭 | 상세 화면에서 삭제 버튼 탭 | 삭제 확인 Alert 표시 | ☐ |
| DP05-TC13 | 삭제 취소 | Alert에서 "취소" 탭 | Alert 닫힘, 아무 변화 없음 | ☐ |
| DP05-TC14 | 삭제 실행 | Alert에서 "삭제" 탭 | 삭제 성공 → 홈 화면 복귀 → 목록에서 사라짐 | ☐ |

#### E. 공유 인텐트 테스트 (핵심 기능!)

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC15 | YouTube 앱에서 공유 | YouTube 앱 → 공유 → "링크 노트" 선택 | 링크 노트 앱 열림 → URL 자동 입력됨 | ☐ |
| DP05-TC16 | 공유 후 저장 | URL 자동 입력 후 저장 버튼 탭 | 저장 성공 → 홈 화면에 새 카드 표시 | ☐ |
| DP05-TC17 | 브라우저에서 공유 | Chrome → YouTube 영상 → 공유 → "링크 노트" | 링크 노트 앱 열림 → URL 자동 입력됨 | ☐ |

#### F. AI 기능 확인

| TC-ID | 테스트 항목 | 테스트 방법 | 예상 결과 | 결과 |
|-------|-------------|-------------|-----------|------|
| DP05-TC18 | AI 요약 품질 | 저장된 링크의 요약 확인 | 20~50자 한국어 요약, 의미 있는 내용 | ☐ |
| DP05-TC19 | AI 태그 확인 | 저장된 링크의 태그 확인 | 관련성 있는 태그 표시 | ☐ |
| DP05-TC20 | AI 카테고리 확인 | 저장된 링크의 카테고리 확인 | 적절한 카테고리 분류 (개발/투자/건강 등) | ☐ |

### 추천 테스트용 YouTube 영상 URL
| URL | 내용 | 기대 카테고리 |
|-----|------|---------------|
| `https://youtu.be/dQw4w9WgXcQ` | 음악 영상 | 엔터테인먼트 |
| `https://www.youtube.com/watch?v=jNQXAC9IVRw` | 최초 유튜브 영상 | 엔터테인먼트 |
| 본인이 자주 보는 유튜브 영상 URL | 실제 사용 시나리오 | 다양 |

### 완료 조건
- [ ] APK 설치 성공
- [ ] 기본 기능 (저장/조회/삭제) 모두 동작
- [ ] 공유 인텐트로 YouTube URL 수신 동작
- [ ] AI 요약/태그/카테고리 정상 생성
- [ ] 토스트 메시지 정상 표시
- [ ] 스켈레톤 로딩 UI 표시
- [ ] 전체 20개 테스트 케이스 중 17개 이상 통과

### 트러블슈팅
| 문제 | 해결 방법 |
|------|-----------|
| 설치 불가 (보안 차단) | 설정 → 보안 → 출처를 알 수 없는 앱 허용 |
| 앱 실행 시 백색 화면 | 서버가 응답하지 않는 경우 → DEPLOY-01 서버 상태 확인 |
| 저장 시 네트워크 에러 | Wi-Fi/데이터 연결 확인, 서버 URL 확인 |
| 공유 목록에 앱 없음 | expo-share-intent 플러그인 활성화 확인 (DEPLOY-03) |
| YouTube 메타데이터 실패 | 서버 로그 확인 → yt-dlp 업데이트 필요할 수 있음 |
| AI 요약이 "에 대한 영상" | OpenAI API 키 잔액 확인 |

---

## PHASE 5 전체 흐름 요약

```
[DEPLOY-01] GitHub 푸시 & Railway 서버 배포
     ↓
[DEPLOY-02] Expo 계정 생성 & EAS 프로젝트 초기화
     ↓
[DEPLOY-03] app.config.js 수정 (projectId, 플러그인 활성화)
     ↓
[DEPLOY-04] eas build --profile preview --platform android (APK 빌드)
     ↓
[DEPLOY-05] 스마트폰에 APK 설치 & 20개 테스트 케이스 검증
```

**예상 총 소요 시간**: 약 1시간 ~ 1시간 30분

**비용 안내**:
- Railway: 무료 플랜 ($5 크레딧/월) 또는 Hobby 플랜 ($5/월)
- EAS Build: 무료 플랜 (월 30회 빌드)
- Supabase: 무료 플랜 (500MB DB)
- OpenAI: 종량제 (링크 1개 저장 시 약 $0.001~$0.01)

---

# PHASE 4: 앱 기능 구현 (완료)

### APP-01 완료 요약
- `app.config.js` 생성 (환경 변수 노출)
- `src/config/index.ts` 생성 (환경 변수 접근)
- `src/services/api.ts` 수정 (환경 변수 사용, deleteLink 추가)
- `.env` 파일 생성
- TypeScript 타입 체크 통과

### APP-02 완료 요약
- HomeScreen에 FAB 버튼 추가 (+ 버튼)
- FAB 클릭 시 SaveLink 화면으로 이동
- `useFocusEffect` 사용하여 화면 포커스 시 목록 새로고침
- 저장 완료 후 1.5초 뒤 자동으로 홈 화면 복귀
- 빈 상태 화면에도 FAB 표시

### APP-03 완료 요약
- `LinkDetailScreen.tsx` 생성 (링크 상세 화면)
- 썸네일, 제목, 카테고리, 요약, 태그, 저장일 표시
- "YouTube에서 보기" 버튼 (빨간색)
- "공유하기" 버튼 (Share API 사용)
- LinkCard 클릭 시 상세 화면으로 이동

### APP-04 완료 요약
- LinkDetailScreen에 삭제 버튼 추가 (빨간 테두리)
- 삭제 확인 Alert 표시
- linkApi.deleteLink() 호출
- 삭제 완료 후 홈 화면으로 자동 복귀
- 삭제 중 로딩 인디케이터 표시

### APP-05 완료 요약
- `expo-share-intent` 라이브러리 설치
- app.config.js에 플러그인 설정
- App.tsx에 ShareIntentProvider 래핑
- YouTube URL 자동 추출 및 SaveLink 화면으로 전달
- SaveLinkScreen에서 params URL 변경 감지

### APP-06 완료 요약
- iOS Share Extension 설정 추가 (`iosShareExtensionName: 'LinkNoteShare'`)
- iOS 활성화 규칙 설정 (텍스트 및 URL 지원)
- APP-05에서 구현한 코드가 iOS에서도 동일하게 작동
- 실제 테스트는 EAS Build 후 가능

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
| 4.0 | 2026-02-08 | PHASE 5 실기기 테스트 배포 계획 추가 (DEPLOY-01~05) |
