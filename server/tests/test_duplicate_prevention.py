"""
BE-04: 링크 중복 저장 방지 테스트
"""
import pytest
import jwt
import time
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from app.services.youtube import YouTubeService
from app.services.metadata.base import ContentMetadata


# 테스트용 JWT
TEST_JWT_SECRET = "test-jwt-secret-for-unit-tests"
TEST_USER_ID = "user-dup-11111111-1111-1111-1111-111111111111"


def make_auth_header() -> dict:
    now = int(time.time())
    token = jwt.encode(
        {"sub": TEST_USER_ID, "aud": "authenticated", "iat": now, "exp": now + 3600, "role": "authenticated"},
        TEST_JWT_SECRET, algorithm="HS256"
    )
    return {"Authorization": f"Bearer {token}"}


class TestURLNormalization:
    """URL 정규화 테스트"""

    def setup_method(self):
        self.youtube_service = YouTubeService()

    def test_normalize_standard_url(self):
        """표준 YouTube URL 정규화"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        normalized = self.youtube_service.normalize_youtube_url(url)
        assert normalized == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_normalize_short_url(self):
        """단축 URL (youtu.be) 정규화"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        normalized = self.youtube_service.normalize_youtube_url(url)
        assert normalized == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_normalize_url_with_extra_params(self):
        """추가 파라미터가 있는 URL 정규화"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&si=abc123&t=120"
        normalized = self.youtube_service.normalize_youtube_url(url)
        assert normalized == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_normalize_shorts_url(self):
        """Shorts URL 정규화"""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        normalized = self.youtube_service.normalize_youtube_url(url)
        assert normalized == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_normalize_embed_url(self):
        """Embed URL 정규화"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        normalized = self.youtube_service.normalize_youtube_url(url)
        assert normalized == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class TestDuplicatePrevention:
    """중복 저장 방지 API 테스트"""

    def setup_method(self):
        self.client = TestClient(app)

    @patch("app.core.auth.settings")
    def test_first_save_success(self, mock_settings):
        """TC01: 최초 저장 성공"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        with patch('app.api.links.youtube_service') as mock_youtube, \
             patch('app.api.links.db_service') as mock_db, \
             patch('app.api.links.ai_service') as mock_ai, \
             patch('app.api.links.metadata_factory') as mock_factory:

            mock_youtube.is_youtube_url.return_value = True
            mock_youtube.normalize_youtube_url.return_value = "https://www.youtube.com/watch?v=test123"

            mock_factory.extract.return_value = ContentMetadata(
                title='테스트 영상', description='테스트 설명',
                thumbnail='https://example.com/thumb.jpg', platform='youtube',
            )

            mock_db.get_link_by_url = AsyncMock(return_value=None)
            mock_db.save_link = AsyncMock(return_value={
                'id': 'new-id',
                'url': 'https://www.youtube.com/watch?v=test123',
                'title': '테스트 영상',
                'thumbnail': 'https://example.com/thumb.jpg',
                'summary': '테스트 요약',
                'tags': ['태그1', '태그2'],
                'category': '기타',
                'media_type': 'youtube',
                'user_id': TEST_USER_ID,
                'created_at': '2024-01-01T00:00:00'
            })

            mock_ai.generate_summary = AsyncMock(return_value='테스트 요약')
            mock_ai.generate_tags = AsyncMock(return_value=['태그1', '태그2'])
            mock_ai.categorize = AsyncMock(return_value='기타')

            response = self.client.post(
                "/api/links/save",
                json={"url": "https://www.youtube.com/watch?v=test123"},
                headers=make_auth_header(),
            )

            assert response.status_code == 200
            assert response.json()['id'] == 'new-id'

    @patch("app.core.auth.settings")
    def test_duplicate_save_conflict(self, mock_settings):
        """TC02: 중복 저장 시도 - 409 Conflict"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        with patch('app.api.links.youtube_service') as mock_youtube, \
             patch('app.api.links.db_service') as mock_db:

            mock_youtube.is_youtube_url.return_value = True
            mock_youtube.normalize_youtube_url.return_value = "https://www.youtube.com/watch?v=existing"

            mock_db.get_link_by_url = AsyncMock(return_value={
                'id': 'existing-id',
                'url': 'https://www.youtube.com/watch?v=existing'
            })

            response = self.client.post(
                "/api/links/save",
                json={"url": "https://www.youtube.com/watch?v=existing"},
                headers=make_auth_header(),
            )

            assert response.status_code == 409
            assert "이미 저장된 링크" in response.json()['detail']
            assert response.headers.get('X-Existing-Link-Id') == 'existing-id'

    @patch("app.core.auth.settings")
    def test_short_url_duplicate_detected(self, mock_settings):
        """TC03: 단축 URL 중복 감지"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        with patch('app.api.links.youtube_service') as mock_youtube, \
             patch('app.api.links.db_service') as mock_db:

            mock_youtube.is_youtube_url.return_value = True
            mock_youtube.normalize_youtube_url.return_value = "https://www.youtube.com/watch?v=existing"

            mock_db.get_link_by_url = AsyncMock(return_value={
                'id': 'existing-id',
                'url': 'https://www.youtube.com/watch?v=existing'
            })

            response = self.client.post(
                "/api/links/save",
                json={"url": "https://youtu.be/existing"},
                headers=make_auth_header(),
            )

            assert response.status_code == 409
            assert "이미 저장된 링크" in response.json()['detail']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
