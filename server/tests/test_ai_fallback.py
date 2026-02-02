"""
AI-03: AI 요청 실패 시 폴백 처리 테스트
"""
import pytest
from unittest.mock import patch, MagicMock
from openai import RateLimitError, APITimeoutError, APIConnectionError

import sys
sys.path.insert(0, '/Users/jeongseyun/Project/LinkNote/server')

from app.services.ai import AIService, retry_on_failure


class TestRetryDecorator:
    """재시도 데코레이터 테스트"""

    @pytest.mark.asyncio
    async def test_retry_success_on_first_attempt(self):
        """첫 번째 시도에서 성공"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.01)
        async def success_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await success_func()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_success_on_second_attempt(self):
        """두 번째 시도에서 성공"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.01)
        async def fail_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise APITimeoutError(request=MagicMock())
            return "success"

        result = await fail_then_success()
        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_exhausted(self):
        """모든 재시도 실패"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.01)
        async def always_fail():
            nonlocal call_count
            call_count += 1
            raise APITimeoutError(request=MagicMock())

        with pytest.raises(APITimeoutError):
            await always_fail()

        assert call_count == 3  # 최초 1회 + 재시도 2회


class TestAIServiceFallback:
    """AI 서비스 폴백 테스트"""

    def setup_method(self):
        self.ai_service = AIService()

    def test_fallback_summary_basic(self):
        """TC03: 폴백 요약 생성 테스트"""
        title = "파이썬 기초 강좌"
        summary = self.ai_service.generate_fallback_summary(title)

        assert summary is not None
        assert len(summary) > 0
        assert "파이썬 기초 강좌" in summary

    def test_fallback_summary_long_title(self):
        """긴 제목에서 폴백 요약 생성"""
        title = "이것은 매우 긴 제목입니다 - 여러 가지 내용이 포함되어 있음 | 채널명"
        summary = self.ai_service.generate_fallback_summary(title)

        assert summary is not None
        assert len(summary) <= 50

    def test_fallback_summary_empty_title(self):
        """빈 제목에서 폴백 요약 생성"""
        summary = self.ai_service.generate_fallback_summary("")
        assert summary == "콘텐츠 요약"

    def test_fallback_tags_basic(self):
        """TC04: 폴백 태그 생성 테스트"""
        title = "파이썬 기초 강좌"
        tags = self.ai_service.generate_fallback_tags(title)

        assert tags is not None
        assert len(tags) == 5
        assert all(isinstance(tag, str) for tag in tags)

    def test_fallback_tags_empty_title(self):
        """빈 제목에서 폴백 태그 생성"""
        tags = self.ai_service.generate_fallback_tags("")

        assert tags is not None
        assert len(tags) == 5
        assert "유튜브" in tags

    def test_validate_category_valid(self):
        """유효한 카테고리 검증"""
        assert self.ai_service.validate_category("개발") == "개발"
        assert self.ai_service.validate_category("투자") == "투자"

    def test_validate_category_invalid(self):
        """유효하지 않은 카테고리는 '기타' 반환"""
        assert self.ai_service.validate_category("잘못된카테고리") == "기타"
        assert self.ai_service.validate_category("") == "기타"

    def test_validate_tags_fill_missing(self):
        """부족한 태그는 기본 태그로 채움"""
        tags = ["태그1", "태그2"]
        validated = self.ai_service.validate_tags(tags)

        assert len(validated) == 5
        assert "태그1" in validated
        assert "태그2" in validated


class TestAIServiceAPIFallback:
    """API 실패 시 폴백 동작 테스트"""

    def setup_method(self):
        self.ai_service = AIService()

    @pytest.mark.asyncio
    async def test_summary_fallback_on_rate_limit(self):
        """Rate Limit 에러 시 폴백 요약 반환"""
        with patch.object(
            self.ai_service,
            '_call_summary_api_with_retry',
            side_effect=RateLimitError(
                message="Rate limit exceeded",
                response=MagicMock(status_code=429),
                body=None
            )
        ):
            result = await self.ai_service.generate_summary("테스트 제목", "테스트 설명")

            assert result is not None
            assert "테스트 제목" in result

    @pytest.mark.asyncio
    async def test_tags_fallback_on_timeout(self):
        """타임아웃 에러 시 폴백 태그 반환"""
        with patch.object(
            self.ai_service,
            '_call_tags_api_with_retry',
            side_effect=APITimeoutError(request=MagicMock())
        ):
            result = await self.ai_service.generate_tags("테스트 제목", "테스트 설명")

            assert result is not None
            assert len(result) == 5

    @pytest.mark.asyncio
    async def test_category_fallback_on_connection_error(self):
        """연결 에러 시 폴백 카테고리 반환"""
        with patch.object(
            self.ai_service,
            '_call_category_api_with_retry',
            side_effect=APIConnectionError(request=MagicMock())
        ):
            result = await self.ai_service.categorize("테스트 제목", "테스트 설명")

            assert result == "기타"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
