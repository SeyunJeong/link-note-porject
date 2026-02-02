# LinkNote 앱 빌드 가이드

## 사전 준비

### 1. EAS CLI 설치
```bash
npm install -g eas-cli
```

### 2. Expo 계정 로그인
```bash
eas login
```

### 3. 프로젝트 초기화 (최초 1회)
```bash
eas build:configure
```

## 빌드 프로파일

| 프로파일 | 용도 | API 서버 |
|---------|------|----------|
| `development` | 개발용 (Dev Client) | localhost |
| `preview` | 내부 테스트용 | production |
| `production` | 스토어 배포용 | production |

## 빌드 명령어

### Android APK 빌드

```bash
# 개발용 (Dev Client)
npm run build:dev:android
# 또는
eas build --profile development --platform android

# 테스트용 (Preview)
npm run build:preview:android
# 또는
eas build --profile preview --platform android

# 프로덕션
npm run build:prod:android
# 또는
eas build --profile production --platform android
```

### iOS 빌드

```bash
# 개발용 (시뮬레이터)
npm run build:dev:ios
# 또는
eas build --profile development --platform ios

# 테스트용 (Preview)
npm run build:preview:ios
# 또는
eas build --profile preview --platform ios

# 프로덕션
npm run build:prod:ios
# 또는
eas build --profile production --platform ios
```

### 모든 플랫폼 동시 빌드

```bash
# 개발용
npm run build:dev

# 테스트용
npm run build:preview

# 프로덕션
npm run build:prod
```

## 빌드 확인

빌드 상태 확인:
```bash
eas build:list
```

빌드 로그 확인:
```bash
eas build:view
```

## APK/IPA 다운로드

빌드 완료 후 EAS 대시보드 또는 CLI에서 다운로드 링크 확인:
```bash
eas build:list --status=finished
```

## iOS 빌드 요구사항

iOS 빌드를 위해서는 다음이 필요합니다:

1. **Apple Developer 계정** ($99/년)
2. **App Store Connect 앱 등록**
3. **프로비저닝 프로파일** (EAS가 자동 관리)

### iOS 인증서 설정
```bash
eas credentials
```

## Android 서명

### 키스토어 자동 생성
EAS가 첫 빌드 시 자동으로 키스토어를 생성합니다.

### 키스토어 관리
```bash
eas credentials
```

## 스토어 제출

### Google Play Store
```bash
eas submit --platform android
```
- `google-services.json` 파일 필요 (Google Play Console에서 다운로드)

### Apple App Store
```bash
eas submit --platform ios
```
- Apple ID와 App Store Connect 앱 ID 필요

## 문제 해결

### 빌드 실패 시
1. `eas build:view`로 로그 확인
2. 캐시 삭제: `eas build --clear-cache`
3. node_modules 재설치

### 자주 발생하는 오류

| 오류 | 해결 방법 |
|-----|----------|
| `Gradle build failed` | Android SDK 버전 확인, gradlew 권한 확인 |
| `Code signing failed` | `eas credentials`로 인증서 재설정 |
| `Node version mismatch` | eas.json의 node 버전 확인 |

## 환경 변수

빌드 시 환경 변수는 eas.json의 `env` 섹션에서 설정됩니다:

```json
{
  "build": {
    "production": {
      "env": {
        "API_BASE_URL": "https://your-api.com/api"
      }
    }
  }
}
```

## 버전 관리

- `app.config.js`의 `version` 필드로 앱 버전 관리
- `autoIncrement: true` 옵션으로 빌드 번호 자동 증가
