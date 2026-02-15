"""
CAT-01: 듀얼 카테고리 시스템 + media_type 테스트
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.platform import detect_media_type


class TestDetectMediaType:
    """URL 도메인 기반 media_type 감지 테스트"""

    def test_tc01_youtube_com(self):
        """TC01: youtube.com URL → youtube"""
        assert detect_media_type("https://www.youtube.com/watch?v=abc123") == "youtube"

    def test_tc02_youtu_be(self):
        """TC02: youtu.be URL → youtube"""
        assert detect_media_type("https://youtu.be/abc123") == "youtube"

    def test_tc03_instagram(self):
        """TC03: instagram.com URL → instagram"""
        assert detect_media_type("https://www.instagram.com/p/abc123/") == "instagram"

    def test_tc04_threads(self):
        """TC04: threads.net URL → threads"""
        assert detect_media_type("https://www.threads.net/@user/post/abc123") == "threads"

    def test_tc05_x_com(self):
        """TC05: x.com URL → x"""
        assert detect_media_type("https://x.com/user/status/123456") == "x"

    def test_tc05b_twitter_com(self):
        """TC05b: twitter.com URL → x"""
        assert detect_media_type("https://twitter.com/user/status/123456") == "x"

    def test_tc06_tiktok(self):
        """TC06: tiktok.com URL → tiktok"""
        assert detect_media_type("https://www.tiktok.com/@user/video/123") == "tiktok"

    def test_tc07_web_generic(self):
        """TC07: 기타 URL → web"""
        assert detect_media_type("https://example.com/article/123") == "web"

    def test_tc07b_web_naver(self):
        """TC07b: 네이버 URL → web"""
        assert detect_media_type("https://blog.naver.com/user/123") == "web"

    def test_tc07c_invalid_url(self):
        """TC07c: 잘못된 URL → web"""
        assert detect_media_type("not-a-url") == "web"

    def test_youtube_without_www(self):
        """YouTube URL without www"""
        assert detect_media_type("https://youtube.com/watch?v=abc123") == "youtube"

    def test_instagram_subdomain(self):
        """Instagram URL with subdomain"""
        assert detect_media_type("https://m.instagram.com/reel/abc123/") == "instagram"

    def test_youtube_nocookie(self):
        """YouTube no-cookie URL"""
        assert detect_media_type("https://www.youtube-nocookie.com/embed/abc") == "youtube"


class TestMediaTypeInSaveLink:
    """저장 시 media_type이 DB에 전달되는지 확인"""

    def test_tc08_save_link_includes_media_type(self):
        """TC08: save_link에 media_type 파라미터가 정상 전달되는지 확인"""
        import jwt
        import time
        from unittest.mock import patch, AsyncMock
        from fastapi.testclient import TestClient
        from main import app

        TEST_JWT_SECRET = "test-jwt-secret-for-unit-tests"
        TEST_USER_ID = "user-a-11111111-1111-1111-1111-111111111111"

        now = int(time.time())
        token = jwt.encode(
            {"sub": TEST_USER_ID, "aud": "authenticated", "iat": now, "exp": now + 3600, "role": "authenticated"},
            TEST_JWT_SECRET, algorithm="HS256"
        )

        client = TestClient(app)

        with patch("app.core.auth.settings") as mock_settings, \
             patch("app.api.links.db_service") as mock_db, \
             patch("app.api.links.youtube_service") as mock_youtube, \
             patch("app.api.links.ai_service") as mock_ai:

            mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

            # Instagram URL 테스트 (비YouTube)
            mock_db.get_link_by_url = AsyncMock(return_value=None)
            mock_db.save_link = AsyncMock(return_value={
                "id": "link-1",
                "url": "https://www.instagram.com/p/abc123/",
                "title": "https://www.instagram.com/p/abc123/",
                "thumbnail": None,
                "summary": "인스타그램 콘텐츠",
                "tags": ["콘텐츠", "링크", "정보", "일반", "추천"],
                "category": "기타",
                "media_type": "instagram",
                "user_id": TEST_USER_ID,
                "created_at": "2024-01-01T00:00:00",
            })
            mock_ai.generate_summary = AsyncMock(return_value="인스타그램 콘텐츠")
            mock_ai.generate_tags = AsyncMock(return_value=["콘텐츠", "링크", "정보", "일반", "추천"])
            mock_ai.categorize = AsyncMock(return_value="기타")

            response = client.post(
                "/api/links/save",
                json={"url": "https://www.instagram.com/p/abc123/"},
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["media_type"] == "instagram"

            # save_link에 media_type이 전달되었는지 확인
            call_kwargs = mock_db.save_link.call_args
            assert call_kwargs.kwargs.get("media_type") == "instagram" or \
                   (len(call_kwargs.args) > 7 and call_kwargs.args[7] == "instagram") or \
                   call_kwargs[1].get("media_type") == "instagram"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
