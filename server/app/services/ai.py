import asyncio
from functools import wraps
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("ai")


def retry_on_failure(max_retries: int = 2, delay: float = 1.0):
    """
    AI API 호출 실패 시 재시도 데코레이터
    - max_retries: 최대 재시도 횟수
    - delay: 재시도 간 대기 시간 (지수 백오프 적용)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError as e:
                    last_exception = e
                    wait_time = delay * (2 ** attempt)  # 지수 백오프
                    logger.warning(f"Rate limit exceeded, attempt {attempt + 1}/{max_retries + 1}, waiting {wait_time}s")
                    if attempt < max_retries:
                        await asyncio.sleep(wait_time)
                except (APITimeoutError, APIConnectionError) as e:
                    last_exception = e
                    wait_time = delay * (attempt + 1)
                    logger.warning(f"API connection error, attempt {attempt + 1}/{max_retries + 1}, waiting {wait_time}s")
                    if attempt < max_retries:
                        await asyncio.sleep(wait_time)
                except Exception as e:
                    last_exception = e
                    logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                    if attempt < max_retries:
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# 유효한 카테고리 목록
VALID_CATEGORIES = ['개발', '투자', '건강', '교육', '엔터테인먼트', '뉴스', '라이프스타일', '기타']

# 요약 프롬프트
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

# 태그 프롬프트
TAG_SYSTEM_PROMPT = """당신은 콘텐츠 태깅 전문가입니다.

## 작업
YouTube 영상의 제목과 설명을 분석하여 검색과 분류에 유용한 태그를 생성하세요.

## 규칙
1. 태그 개수: 정확히 5개
2. 태그 형식: 명사 또는 명사구 (2-4단어)
3. 태그 유형 혼합:
   - 주제 태그 2개: 영상의 핵심 주제
   - 형식 태그 1개: 튜토리얼, 리뷰, 브이로그 등
   - 대상 태그 1개: 초보자, 전문가, 일반인 등
   - 감성 태그 1개: 재미, 정보, 감동 등

## 출력 형식
태그만 쉼표로 구분하여 출력 (설명 없이)

## 예시
입력: "파이썬 기초 강좌 1편 - 변수와 자료형"
출력: 파이썬, 프로그래밍 기초, 튜토리얼, 초보자, 정보
"""

# 카테고리 프롬프트
CATEGORY_SYSTEM_PROMPT = """당신은 콘텐츠 분류 전문가입니다.

## 카테고리 정의
| 카테고리 | 설명 | 예시 |
|----------|------|------|
| 개발 | 프로그래밍, IT, 기술 | 코딩 강좌, 앱 리뷰 |
| 투자 | 주식, 부동산, 재테크 | 주식 분석, 경제 뉴스 |
| 건강 | 운동, 의학, 다이어트 | 홈트레이닝, 건강 정보 |
| 교육 | 학습, 자기계발, 언어 | 영어 강좌, 독서 리뷰 |
| 엔터테인먼트 | 예능, 음악, 게임 | 게임 플레이, 음악 리뷰 |
| 뉴스 | 시사, 정치, 사회 | 뉴스 분석, 이슈 정리 |
| 라이프스타일 | 일상, 요리, 여행 | 브이로그, 맛집 탐방 |
| 기타 | 위 카테고리에 해당 없음 | |

## 출력
카테고리 이름만 출력 (설명 없이)
"""


class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=30.0,  # 30초 타임아웃
            max_retries=0,  # OpenAI 내부 재시도 비활성화 (우리 데코레이터 사용)
        )

        # 의미 없는 요약 패턴
        self.invalid_patterns = [
            "영상입니다",
            "콘텐츠입니다",
            "비디오입니다",
            "요약을 생성할 수 없",
            "요약할 수 없",
            "알 수 없",
        ]

    def validate_summary(self, summary: str, title: str) -> bool:
        """
        요약 유효성 검증
        - 길이: 10자 이상 60자 이하
        - 의미 없는 요약 필터링
        - 제목과 동일한지 체크
        """
        if not summary:
            return False

        # 길이 검증
        if len(summary) < 10 or len(summary) > 60:
            logger.warning(f"Summary length invalid: {len(summary)} chars")
            return False

        # 의미 없는 패턴 체크
        for pattern in self.invalid_patterns:
            if pattern in summary:
                logger.warning(f"Summary contains invalid pattern: {pattern}")
                return False

        # 제목과 동일한지 체크 (80% 이상 유사하면 무효)
        if self._similarity(summary, title) > 0.8:
            logger.warning("Summary too similar to title")
            return False

        return True

    def _similarity(self, s1: str, s2: str) -> float:
        """간단한 문자열 유사도 계산"""
        if not s1 or not s2:
            return 0.0

        s1_set = set(s1.lower())
        s2_set = set(s2.lower())

        intersection = len(s1_set & s2_set)
        union = len(s1_set | s2_set)

        return intersection / union if union > 0 else 0.0

    def generate_fallback_summary(self, title: str) -> str:
        """AI 실패 시 제목 기반 기본 요약 생성"""
        if not title:
            return "콘텐츠 요약"

        # 제목이 너무 길면 잘라서 사용
        truncated_title = title[:30] if len(title) > 30 else title

        # 제목에서 불필요한 부분 제거
        clean_title = truncated_title.split('|')[0].split('-')[0].strip()

        if len(clean_title) < 5:
            clean_title = truncated_title

        return f"{clean_title}에 대한 영상"

    def validate_category(self, category: str) -> str:
        """카테고리 유효성 검증 - 유효하지 않으면 '기타' 반환"""
        if category not in VALID_CATEGORIES:
            logger.warning(f"Invalid category '{category}', falling back to '기타'")
            return '기타'
        return category

    def validate_tags(self, tags: list[str]) -> list[str]:
        """태그 유효성 검증 - 개수와 형식 체크"""
        if not tags:
            return self.generate_fallback_tags("")

        # 빈 태그 제거, 공백 정리
        cleaned_tags = [tag.strip() for tag in tags if tag and tag.strip()]

        # 너무 긴 태그 자르기 (최대 20자)
        cleaned_tags = [tag[:20] for tag in cleaned_tags]

        # 5개 미만이면 기본 태그로 채우기
        if len(cleaned_tags) < 5:
            default_tags = ['유튜브', '영상', '콘텐츠', '정보', '일반']
            for dt in default_tags:
                if len(cleaned_tags) >= 5:
                    break
                if dt not in cleaned_tags:
                    cleaned_tags.append(dt)

        return cleaned_tags[:5]

    def generate_fallback_tags(self, title: str) -> list[str]:
        """AI 실패 시 제목 기반 태그 생성"""
        if not title:
            return ['유튜브', '영상', '콘텐츠', '정보', '일반']

        # 제목에서 단어 추출 (불용어 제외)
        stopwords = ['의', '를', '을', '에', '이', '가', '은', '는', '하는', '한', '된', '대한']
        words = title.split()
        filtered = [w for w in words if w not in stopwords and len(w) > 1][:3]

        # 기본 태그와 합치기
        base_tags = ['유튜브', '콘텐츠']
        all_tags = filtered + base_tags

        return all_tags[:5] if len(all_tags) >= 5 else all_tags + ['정보', '일반'][:5 - len(all_tags)]

    async def _call_summary_api(self, title: str, description: str) -> str:
        """OpenAI API를 호출하여 요약 생성 (재시도 대상)"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"제목: {title}\n\n설명: {description[:500] if description else '설명 없음'}"
                }
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    @retry_on_failure(max_retries=2, delay=1.0)
    async def _call_summary_api_with_retry(self, title: str, description: str) -> str:
        """재시도 로직이 적용된 요약 API 호출"""
        return await self._call_summary_api(title, description)

    async def generate_summary(self, title: str, description: str) -> str:
        logger.info(f"Generating summary for: {title[:50]}")
        try:
            summary = await self._call_summary_api_with_retry(title, description)

            # 요약 검증
            if not self.validate_summary(summary, title):
                logger.warning(f"Summary validation failed, using fallback")
                summary = self.generate_fallback_summary(title)

            logger.info(f"Summary generated: {summary}")
            return summary

        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded after retries, using fallback: {e}")
            return self.generate_fallback_summary(title)
        except (APITimeoutError, APIConnectionError) as e:
            logger.warning(f"API connection failed after retries, using fallback: {e}")
            return self.generate_fallback_summary(title)
        except Exception as e:
            logger.error(f"AI summary generation error: {e}")
            return self.generate_fallback_summary(title)

    async def _call_tags_api(self, title: str, description: str) -> str:
        """OpenAI API를 호출하여 태그 생성 (재시도 대상)"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": TAG_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"제목: {title}\n\n설명: {description[:500] if description else '설명 없음'}"
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    @retry_on_failure(max_retries=2, delay=1.0)
    async def _call_tags_api_with_retry(self, title: str, description: str) -> str:
        """재시도 로직이 적용된 태그 API 호출"""
        return await self._call_tags_api(title, description)

    async def generate_tags(self, title: str, description: str) -> list[str]:
        logger.info(f"Generating tags for: {title[:50]}")
        try:
            tags_text = await self._call_tags_api_with_retry(title, description)
            tags = [tag.strip() for tag in tags_text.split(',')]

            # 태그 검증 및 정규화
            validated_tags = self.validate_tags(tags)
            logger.info(f"Tags generated: {validated_tags}")
            return validated_tags

        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded after retries, using fallback tags: {e}")
            return self.generate_fallback_tags(title)
        except (APITimeoutError, APIConnectionError) as e:
            logger.warning(f"API connection failed after retries, using fallback tags: {e}")
            return self.generate_fallback_tags(title)
        except Exception as e:
            logger.error(f"AI tag generation error: {e}")
            return self.generate_fallback_tags(title)

    async def _call_category_api(self, title: str, description: str) -> str:
        """OpenAI API를 호출하여 카테고리 분류 (재시도 대상)"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": CATEGORY_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"제목: {title}\n\n설명: {description[:500] if description else '설명 없음'}"
                }
            ],
            max_tokens=20,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    @retry_on_failure(max_retries=2, delay=1.0)
    async def _call_category_api_with_retry(self, title: str, description: str) -> str:
        """재시도 로직이 적용된 카테고리 API 호출"""
        return await self._call_category_api(title, description)

    async def categorize(self, title: str, description: str) -> str:
        logger.info(f"Categorizing: {title[:50]}")
        try:
            category = await self._call_category_api_with_retry(title, description)

            # 카테고리 검증
            validated_category = self.validate_category(category)
            logger.info(f"Category assigned: {validated_category}")
            return validated_category

        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded after retries, using fallback category: {e}")
            return "기타"
        except (APITimeoutError, APIConnectionError) as e:
            logger.warning(f"API connection failed after retries, using fallback category: {e}")
            return "기타"
        except Exception as e:
            logger.error(f"AI categorization error: {e}")
            return "기타"


ai_service = AIService()
