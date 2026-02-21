# LinkNote

링크를 공유하면 자동으로 저장 + 요약 + 태그 + 분류해주는 앱.

유튜브 보다가 "나중에 봐야지" 하고 공유 버튼 누르면, 앱이 알아서 어떤 내용인지 요약하고, 태그 달고, 카테고리까지 분류해서 정리해준다.

## 작동 방식

```
유튜브/인스타/X에서 [공유] 탭
        ↓
  LinkNote 선택
        ↓
  ┌─────────────────────────────┐
  │  1. URL 정규화 (중복 방지)     │
  │  2. 메타데이터 추출            │
  │     (제목, 썸네일, 설명)       │
  │  3. AI 처리 (병렬)            │
  │     ├─ 한줄 요약 생성          │
  │     ├─ 태그 5개 자동 생성      │
  │     └─ 카테고리 자동 분류      │
  └─────────────────────────────┘
        ↓
  홈 화면에 카드로 표시
```

로그인 안 한 상태에서 공유하면 큐에 저장해뒀다가 로그인 후 자동 처리한다.

## 지원 플랫폼

| 플랫폼 | 메타데이터 추출 | 비고 |
|--------|:-:|------|
| YouTube | yt-dlp | 영상 제목, 설명, 썸네일 |
| Instagram | OpenGraph | OG 태그 기반 |
| Threads | OpenGraph | |
| X (Twitter) | OpenGraph | |
| TikTok | OpenGraph | |
| 일반 웹 | OpenGraph | 어떤 URL이든 기본 지원 |

플랫폼별 추출기는 Factory Pattern으로 구현했다. 새 플랫폼 추가 시 `MetadataExtractor`를 구현하고 팩토리에 등록하면 된다.

## AI 처리

링크 저장 시 OpenAI API로 3가지를 병렬 생성한다:

- **요약**: 20~50자 한국어 한줄 요약 (제목 앵무새 반복 방지 로직 포함)
- **태그**: 5개 (주제 2 + 형식 1 + 대상 1 + 성격 1)
- **카테고리**: 개발, 투자, 건강, 교육, 엔터테인먼트, 뉴스, 라이프스타일, 기타

API 실패 시 지수 백오프로 재시도하고, 최종 실패 시 제목 기반 폴백 요약을 생성한다.

## 기술 스택

### 앱 (React Native)

| 기술 | 용도 |
|------|------|
| Expo (SDK 54) | React Native 프레임워크 |
| TypeScript | 타입 안전성 |
| React Navigation | 화면 전환 |
| expo-share-intent | OS 공유 인텐트 수신 |
| Supabase JS | 인증 + DB 클라이언트 |
| Axios | HTTP 통신 (JWT 자동 갱신 인터셉터) |
| EAS Build | 앱 빌드/배포 (dev/preview/production 프로필) |

### 서버 (FastAPI)

| 기술 | 용도 |
|------|------|
| FastAPI | REST API |
| OpenAI (GPT-4o-mini) | 요약/태그/카테고리 생성 |
| yt-dlp | YouTube 메타데이터 추출 |
| BeautifulSoup4 | OG 태그 파싱 |
| PyJWT | Supabase JWT 검증 |
| slowapi | Rate limiting (저장 30/min, 조회 60/min) |

### 인프라

| 기술 | 용도 |
|------|------|
| Supabase | PostgreSQL DB + Auth (이메일/Google OAuth) |
| Row-Level Security | 유저별 데이터 격리 |
| Railway | 서버 배포 |

## 프로젝트 구조

```
link-note-porject/
├── app/                          # Expo (React Native)
│   ├── src/
│   │   ├── screens/
│   │   │   ├── HomeScreen.tsx        메인 (링크 목록 + 필터)
│   │   │   ├── LoginScreen.tsx       로그인 (이메일 + Google)
│   │   │   ├── SignUpScreen.tsx      회원가입
│   │   │   ├── SaveLinkScreen.tsx    수동 링크 저장
│   │   │   └── LinkDetailScreen.tsx  링크 상세/삭제
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx    인증 상태 관리
│   │   ├── services/
│   │   │   └── api.ts            API 클라이언트 (JWT 인터셉터)
│   │   └── types/
│   ├── App.tsx
│   └── app.json
│
├── server/                       # FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── links.py          POST /save, GET /, GET /{id}, DELETE /{id}
│   │   ├── core/
│   │   │   ├── auth.py           JWT 검증
│   │   │   └── config.py         환경 변수
│   │   ├── models/
│   │   │   └── link.py           Pydantic 스키마
│   │   └── services/
│   │       ├── ai.py             OpenAI 연동 (재시도 + 폴백)
│   │       ├── youtube.py        URL 정규화
│   │       ├── platform.py       플랫폼 감지
│   │       └── metadata/         추출기 (Factory Pattern)
│   │           ├── base.py
│   │           ├── ytdlp_extractor.py
│   │           └── opengraph_extractor.py
│   ├── main.py
│   └── supabase_schema.sql
│
└── docs/
```

## DB 스키마

```sql
CREATE TABLE links (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID REFERENCES auth.users(id),
  url         TEXT NOT NULL,
  title       TEXT NOT NULL,
  thumbnail   TEXT,
  summary     TEXT NOT NULL,          -- AI 생성
  tags        TEXT[] DEFAULT '{}',    -- AI 생성 (5개)
  category    TEXT,                   -- AI 생성
  media_type  TEXT,                   -- youtube | instagram | threads | x | tiktok | web
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: 본인 데이터만 접근 가능
ALTER TABLE links ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only access own links"
  ON links FOR ALL USING (auth.uid() = user_id);
```

## 실행

### 서버

```bash
cd server
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY 설정
python main.py                    # http://localhost:8000
```

### 앱

```bash
cd app
npm install
npx expo start                    # Expo Go 또는 개발 빌드로 실행
```

### 빌드

```bash
npm run build:dev:android         # 개발용 APK
npm run build:preview:android     # 테스트용 APK
npm run build:prod:android        # 프로덕션 AAB
```

## 환경 변수

### 서버 (.env)

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_supabase_jwt_secret
```

### 앱 (.env.development / .env.production)

```
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_SUPABASE_URL=your_supabase_url
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```
