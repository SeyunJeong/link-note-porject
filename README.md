# 링크 노트 (LinkNote)

링크를 보내면, 자동으로 저장 + 요약 + 분류해주는 개인용 노트 앱

## 프로젝트 구조

```
LinkNote/
├── app/                 # Expo (React Native) 앱
│   ├── src/
│   │   ├── components/  # 재사용 컴포넌트
│   │   ├── screens/     # 화면 컴포넌트
│   │   ├── services/    # API 서비스
│   │   ├── types/       # TypeScript 타입
│   │   └── hooks/       # 커스텀 훅
│   └── App.tsx
├── server/              # FastAPI 서버
│   ├── app/
│   │   ├── api/         # API 라우터
│   │   ├── core/        # 설정
│   │   ├── models/      # Pydantic 모델
│   │   └── services/    # 비즈니스 로직
│   └── main.py
└── PLANNING.md          # 기획 문서
```

## 기술 스택

- **앱**: Expo (React Native)
- **서버**: FastAPI
- **DB**: Supabase
- **AI**: OpenAI

## 시작하기

### 서버 실행

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # 환경 변수 설정
python main.py
```

### 앱 실행

```bash
cd app
npm install
npx expo start
```

## 환경 변수

### 서버 (.env)

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
```

## Supabase 테이블 구조

```sql
CREATE TABLE links (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  thumbnail TEXT,
  summary TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```
