"""
AUTH-01: Supabase Auth 스키마 + 서버 인증 미들웨어 테스트
"""
import pytest
import jwt
import time
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app


# 테스트용 JWT Secret
TEST_JWT_SECRET = "test-jwt-secret-for-unit-tests"
TEST_USER_A_ID = "user-a-11111111-1111-1111-1111-111111111111"
TEST_USER_B_ID = "user-b-22222222-2222-2222-2222-222222222222"


def make_jwt(user_id: str, expired: bool = False) -> str:
    """테스트용 JWT 토큰 생성"""
    now = int(time.time())
    payload = {
        "sub": user_id,
        "aud": "authenticated",
        "iat": now - 3600,
        "exp": (now - 100) if expired else (now + 3600),
        "role": "authenticated",
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")


def auth_header(user_id: str) -> dict:
    """Authorization 헤더 생성"""
    token = make_jwt(user_id)
    return {"Authorization": f"Bearer {token}"}


class TestAuthMiddleware:
    """인증 미들웨어 테스트"""

    def setup_method(self):
        self.client = TestClient(app)

    @patch("app.core.auth.settings")
    def test_tc01_no_auth_header_returns_401(self, mock_settings):
        """TC01: Authorization 헤더 없으면 401"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        response = self.client.get("/api/links/")
        assert response.status_code in [401, 403]

    @patch("app.core.auth.settings")
    def test_tc02_invalid_jwt_returns_401(self, mock_settings):
        """TC02: 잘못된 JWT면 401"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        response = self.client.get(
            "/api/links/",
            headers={"Authorization": "Bearer invalid-token-here"}
        )
        assert response.status_code == 401
        assert "유효하지 않은 토큰" in response.json()["detail"]

    @patch("app.core.auth.settings")
    def test_tc02_expired_jwt_returns_401(self, mock_settings):
        """TC02-b: 만료된 JWT면 401"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        expired_token = make_jwt(TEST_USER_A_ID, expired=True)
        response = self.client.get(
            "/api/links/",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
        assert "만료" in response.json()["detail"]

    @patch("app.core.auth.settings")
    @patch("app.api.links.db_service")
    def test_tc03_valid_jwt_extracts_user_id(self, mock_db, mock_settings):
        """TC03: 유효한 JWT에서 user_id 정상 추출"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET
        mock_db.get_links = AsyncMock(return_value=[])
        mock_db.get_links_count = AsyncMock(return_value=0)

        response = self.client.get(
            "/api/links/",
            headers=auth_header(TEST_USER_A_ID)
        )
        assert response.status_code == 200

        # user_id가 DB 서비스에 올바르게 전달되었는지 확인
        mock_db.get_links.assert_called_once_with(
            TEST_USER_A_ID, limit=50, offset=0
        )


class TestUserIsolation:
    """사용자 간 데이터 격리 테스트"""

    def setup_method(self):
        self.client = TestClient(app)

    @patch("app.core.auth.settings")
    @patch("app.api.links.db_service")
    def test_tc04_user_cannot_see_others_links(self, mock_db, mock_settings):
        """TC04: User A가 User B의 링크 조회 불가"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        # User B의 링크가 있지만, User A로 조회 시 빈 결과
        mock_db.get_links = AsyncMock(return_value=[])
        mock_db.get_links_count = AsyncMock(return_value=0)

        response = self.client.get(
            "/api/links/",
            headers=auth_header(TEST_USER_A_ID)
        )
        assert response.status_code == 200
        assert response.json()["total"] == 0

        # User A의 user_id로만 조회했는지 확인
        mock_db.get_links.assert_called_once_with(
            TEST_USER_A_ID, limit=50, offset=0
        )

    @patch("app.core.auth.settings")
    @patch("app.api.links.db_service")
    def test_tc04_user_cannot_get_others_link_by_id(self, mock_db, mock_settings):
        """TC04-b: User A가 User B의 링크를 ID로 조회 불가"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

        link_id = "some-link-id"
        # get_link_by_id가 user_id 필터로 인해 None 반환
        mock_db.get_link_by_id = AsyncMock(return_value=None)

        response = self.client.get(
            f"/api/links/{link_id}",
            headers=auth_header(TEST_USER_A_ID)
        )
        assert response.status_code == 404

        # user_id가 함께 전달되었는지 확인
        mock_db.get_link_by_id.assert_called_once_with(link_id, TEST_USER_A_ID)

    @patch("app.core.auth.settings")
    @patch("app.api.links.db_service")
    @patch("app.api.links.youtube_service")
    @patch("app.api.links.ai_service")
    def test_tc05_same_url_different_users(
        self, mock_ai, mock_youtube, mock_db, mock_settings
    ):
        """TC05: 같은 URL을 다른 사용자가 각각 저장 가능"""
        mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET
        test_url = "https://www.youtube.com/watch?v=shared123"

        # YouTube 서비스 모킹
        mock_youtube.is_youtube_url.return_value = True
        mock_youtube.normalize_youtube_url.return_value = test_url
        mock_youtube.extract_metadata.return_value = {
            "title": "공유 영상",
            "description": "설명",
            "thumbnail": "https://example.com/thumb.jpg",
        }

        # AI 서비스 모킹
        mock_ai.generate_summary = AsyncMock(return_value="요약")
        mock_ai.generate_tags = AsyncMock(return_value=["태그1", "태그2", "태그3", "태그4", "태그5"])
        mock_ai.categorize = AsyncMock(return_value="기타")

        # --- User A 저장 ---
        mock_db.get_link_by_url = AsyncMock(return_value=None)  # 중복 없음
        mock_db.save_link = AsyncMock(return_value={
            "id": "link-a",
            "url": test_url,
            "title": "공유 영상",
            "thumbnail": "https://example.com/thumb.jpg",
            "summary": "요약",
            "tags": ["태그1", "태그2", "태그3", "태그4", "태그5"],
            "category": "기타",
            "user_id": TEST_USER_A_ID,
            "created_at": "2024-01-01T00:00:00",
        })

        response_a = self.client.post(
            "/api/links/save",
            json={"url": test_url},
            headers=auth_header(TEST_USER_A_ID),
        )
        assert response_a.status_code == 200

        # User A의 user_id로 중복 체크했는지 확인
        mock_db.get_link_by_url.assert_called_with(test_url, TEST_USER_A_ID)

        # --- User B 저장 ---
        mock_db.get_link_by_url = AsyncMock(return_value=None)  # User B에겐 중복 없음
        mock_db.save_link = AsyncMock(return_value={
            "id": "link-b",
            "url": test_url,
            "title": "공유 영상",
            "thumbnail": "https://example.com/thumb.jpg",
            "summary": "요약",
            "tags": ["태그1", "태그2", "태그3", "태그4", "태그5"],
            "category": "기타",
            "user_id": TEST_USER_B_ID,
            "created_at": "2024-01-01T00:00:00",
        })

        response_b = self.client.post(
            "/api/links/save",
            json={"url": test_url},
            headers=auth_header(TEST_USER_B_ID),
        )
        assert response_b.status_code == 200

        # User B의 user_id로 중복 체크했는지 확인
        mock_db.get_link_by_url.assert_called_with(test_url, TEST_USER_B_ID)


class TestHealthEndpoints:
    """인증 불필요 엔드포인트 테스트"""

    def setup_method(self):
        self.client = TestClient(app)

    def test_root_no_auth_required(self):
        """루트 엔드포인트는 인증 불필요"""
        response = self.client.get("/")
        assert response.status_code == 200

    def test_health_no_auth_required(self):
        """헬스 엔드포인트는 인증 불필요"""
        response = self.client.get("/health")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
