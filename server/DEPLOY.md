# LinkNote API 서버 배포 가이드

## 필요한 환경 변수

배포 플랫폼에서 다음 환경 변수를 설정해야 합니다:

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `SUPABASE_URL` | Supabase 프로젝트 URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase anon/service key | `eyJhbGc...` |
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-...` |

## Railway 배포

### 방법 1: Railway CLI
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
cd server
railway init

# 환경 변수 설정
railway variables set SUPABASE_URL=your_url
railway variables set SUPABASE_KEY=your_key
railway variables set OPENAI_API_KEY=your_key

# 배포
railway up
```

### 방법 2: GitHub 연동
1. [Railway](https://railway.app) 접속
2. New Project → Deploy from GitHub repo
3. LinkNote 저장소 선택
4. Root Directory: `server` 설정
5. Variables 탭에서 환경 변수 추가
6. Deploy 클릭

## Render 배포

### 방법 1: render.yaml 사용
1. [Render](https://render.com) 접속
2. New → Blueprint
3. GitHub 저장소 연결
4. `render.yaml` 자동 감지
5. 환경 변수 입력
6. Apply 클릭

### 방법 2: 수동 설정
1. New → Web Service
2. GitHub 저장소 연결
3. 설정:
   - Name: `linknote-api`
   - Root Directory: `server`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment 탭에서 환경 변수 추가
5. Create Web Service 클릭

## 배포 확인

배포 완료 후 다음 엔드포인트로 확인:

```bash
# 헬스 체크
curl https://your-app-url/health

# API 테스트
curl https://your-app-url/

# 링크 저장 테스트
curl -X POST https://your-app-url/api/links \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## 문제 해결

### 빌드 실패
- `runtime.txt`의 Python 버전 확인
- `requirements.txt` 의존성 확인

### 서버 시작 실패
- 환경 변수 설정 확인
- 로그에서 에러 메시지 확인

### API 응답 없음
- `/health` 엔드포인트 먼저 테스트
- CORS 설정 확인
