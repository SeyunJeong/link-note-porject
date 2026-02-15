"""
PLATFORM-02: 필터링 API 테스트
"""
import pytest
import jwt
import time
from unittest.mock import patch, AsyncMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from main import app


TEST_JWT_SECRET = "test-jwt-secret-for-unit-tests"
TEST_USER_ID = "user-filter-11111111-1111-1111-1111-111111111111"


def make_auth_header() -> dict:
    now = int(time.time())
    token = jwt.encode(
        {"sub": TEST_USER_ID, "aud": "authenticated", "iat": now, "exp": now + 3600, "role": "authenticated"},
        TEST_JWT_SECRET, algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


SAMPLE_LINKS = [
    {"id": "1", "url": "https://youtube.com/1", "title": "유튜브1", "thumbnail": None,
     "summary": "요약1", "tags": ["t1"], "category": "개발", "media_type": "youtube",
     "user_id": TEST_USER_ID, "created_at": "2024-01-01T00:00:00"},
    {"id": "2", "url": "https://instagram.com/2", "title": "인스타2", "thumbnail": None,
     "summary": "요약2", "tags": ["t2"], "category": "투자", "media_type": "instagram",
     "user_id": TEST_USER_ID, "created_at": "2024-01-02T00:00:00"},
    {"id": "3", "url": "https://example.com/3", "title": "웹3", "thumbnail": None,
     "summary": "요약3", "tags": ["t3"], "category": "개발", "media_type": "web",
     "user_id": TEST_USER_ID, "created_at": "2024-01-03T00:00:00"},
]


class TestFilterAPI:
    """필터링 API 테스트"""

    def setup_method(self):
        self.client = TestClient(app)

    @patch("app.core.auth.settings")
    def test_tc01_get_all_links(self, mock_settings):
        """TC01: 필터 없이 전체 링크 조회"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        with patch("app.api.links.db_service") as mock_db:
            mock_db.get_links = AsyncMock(return_value=SAMPLE_LINKS)
            mock_db.get_links_count = AsyncMock(return_value=3)

            response = self.client.get("/api/links/", headers=make_auth_header())

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 3
            assert len(data["links"]) == 3

            # get_links에 필터가 None으로 전달되었는지 확인
            mock_db.get_links.assert_called_once_with(
                TEST_USER_ID, limit=50, offset=0, media_type=None, category=None,
            )

    @patch("app.core.auth.settings")
    def test_tc02_filter_by_media_type(self, mock_settings):
        """TC02: media_type 필터로 YouTube만 조회"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        youtube_only = [l for l in SAMPLE_LINKS if l["media_type"] == "youtube"]

        with patch("app.api.links.db_service") as mock_db:
            mock_db.get_links = AsyncMock(return_value=youtube_only)
            mock_db.get_links_count = AsyncMock(return_value=1)

            response = self.client.get(
                "/api/links/?media_type=youtube", headers=make_auth_header(),
            )

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert len(data["links"]) == 1
            assert data["links"][0]["media_type"] == "youtube"

            mock_db.get_links.assert_called_once_with(
                TEST_USER_ID, limit=50, offset=0, media_type="youtube", category=None,
            )

    @patch("app.core.auth.settings")
    def test_tc03_filter_by_category(self, mock_settings):
        """TC03: category 필터로 '개발'만 조회"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        dev_only = [l for l in SAMPLE_LINKS if l["category"] == "개발"]

        with patch("app.api.links.db_service") as mock_db:
            mock_db.get_links = AsyncMock(return_value=dev_only)
            mock_db.get_links_count = AsyncMock(return_value=2)

            response = self.client.get(
                "/api/links/?category=%EA%B0%9C%EB%B0%9C", headers=make_auth_header(),
            )

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2

            mock_db.get_links.assert_called_once_with(
                TEST_USER_ID, limit=50, offset=0, media_type=None, category="개발",
            )

    @patch("app.core.auth.settings")
    def test_tc04_filter_combined(self, mock_settings):
        """TC04: media_type + category 교집합 필터"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        combined = [l for l in SAMPLE_LINKS if l["media_type"] == "youtube" and l["category"] == "개발"]

        with patch("app.api.links.db_service") as mock_db:
            mock_db.get_links = AsyncMock(return_value=combined)
            mock_db.get_links_count = AsyncMock(return_value=1)

            response = self.client.get(
                "/api/links/?media_type=youtube&category=%EA%B0%9C%EB%B0%9C",
                headers=make_auth_header(),
            )

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1

            mock_db.get_links.assert_called_once_with(
                TEST_USER_ID, limit=50, offset=0, media_type="youtube", category="개발",
            )
            mock_db.get_links_count.assert_called_once_with(
                TEST_USER_ID, media_type="youtube", category="개발",
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
