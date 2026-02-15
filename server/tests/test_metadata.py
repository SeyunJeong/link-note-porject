"""
PLATFORM-01: 멀티 플랫폼 메타데이터 추출기 테스트
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, AsyncMock
import jwt
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.metadata.base import ContentMetadata
from app.services.metadata.ytdlp_extractor import YtDlpExtractor
from app.services.metadata.opengraph_extractor import OpenGraphExtractor
from app.services.metadata.extractor_factory import MetadataExtractorFactory


class TestYtDlpCanHandle:
    """TC01~04: 각 플랫폼 URL can_handle 확인"""

    def setup_method(self):
        self.extractor = YtDlpExtractor()

    def test_tc01_youtube_can_handle(self):
        assert self.extractor.can_handle("https://www.youtube.com/watch?v=abc123")

    def test_tc02_instagram_can_handle(self):
        assert self.extractor.can_handle("https://www.instagram.com/p/abc123/")

    def test_tc03_tiktok_can_handle(self):
        assert self.extractor.can_handle("https://www.tiktok.com/@user/video/123")

    def test_tc04_x_can_handle(self):
        assert self.extractor.can_handle("https://x.com/user/status/123")

    def test_twitter_can_handle(self):
        assert self.extractor.can_handle("https://twitter.com/user/status/123")

    def test_generic_cannot_handle(self):
        assert not self.extractor.can_handle("https://example.com/article")

    def test_threads_cannot_handle(self):
        """Threads는 yt-dlp 미지원"""
        assert not self.extractor.can_handle("https://www.threads.net/@user/post/123")


class TestOpenGraphCanHandle:
    """OpenGraph 추출기는 모든 URL 처리 가능"""

    def setup_method(self):
        self.extractor = OpenGraphExtractor()

    def test_can_handle_any_url(self):
        assert self.extractor.can_handle("https://example.com")
        assert self.extractor.can_handle("https://www.threads.net/@user/post/123")
        assert self.extractor.can_handle("https://naver.com")


class TestFactorySelection:
    """TC05: 팩토리 추출기 선택"""

    def setup_method(self):
        self.factory = MetadataExtractorFactory()

    def test_tc05_youtube_selects_ytdlp(self):
        extractor = self.factory.get_extractor("https://www.youtube.com/watch?v=abc")
        assert isinstance(extractor, YtDlpExtractor)

    def test_tc05_instagram_selects_ytdlp(self):
        extractor = self.factory.get_extractor("https://www.instagram.com/p/abc/")
        assert isinstance(extractor, YtDlpExtractor)

    def test_tc05_threads_selects_opengraph(self):
        extractor = self.factory.get_extractor("https://www.threads.net/@user/post/123")
        assert isinstance(extractor, OpenGraphExtractor)

    def test_tc05_web_selects_opengraph(self):
        extractor = self.factory.get_extractor("https://example.com/article")
        assert isinstance(extractor, OpenGraphExtractor)


class TestYtDlpExtract:
    """TC06~07: YtDlp 추출기 메타데이터 추출 (mock)"""

    def setup_method(self):
        self.extractor = YtDlpExtractor()

    @patch("app.services.metadata.ytdlp_extractor.yt_dlp.YoutubeDL")
    def test_tc06_youtube_extract(self, mock_ydl_class):
        """YouTube 메타데이터 추출"""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__ = MagicMock(return_value=mock_ydl)
        mock_ydl_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ydl.extract_info.return_value = {
            'title': '테스트 영상',
            'description': '테스트 설명',
            'thumbnail': 'https://img.youtube.com/thumb.jpg',
            'thumbnails': [{'url': 'https://img.youtube.com/thumb.jpg', 'height': 720, 'width': 1280}],
            'extractor_key': 'Youtube',
            'duration': 300,
            'channel': '테스트 채널',
            'view_count': 1000,
        }

        result = self.extractor.extract("https://www.youtube.com/watch?v=abc123")

        assert isinstance(result, ContentMetadata)
        assert result.title == '테스트 영상'
        assert result.description == '테스트 설명'
        assert result.thumbnail == 'https://img.youtube.com/thumb.jpg'
        assert result.duration == 300
        assert result.author == '테스트 채널'

    @patch("app.services.metadata.ytdlp_extractor.yt_dlp.YoutubeDL")
    def test_tc07_instagram_extract(self, mock_ydl_class):
        """Instagram 메타데이터 추출"""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__ = MagicMock(return_value=mock_ydl)
        mock_ydl_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ydl.extract_info.return_value = {
            'title': '인스타 게시물',
            'description': '인스타 설명',
            'thumbnail': 'https://insta.com/thumb.jpg',
            'thumbnails': [],
            'extractor_key': 'Instagram',
            'uploader': 'insta_user',
        }

        result = self.extractor.extract("https://www.instagram.com/p/abc/")

        assert result.title == '인스타 게시물'
        assert result.author == 'insta_user'


class TestOpenGraphExtract:
    """TC08~09: OpenGraph 추출기 메타데이터 추출 (mock)"""

    def setup_method(self):
        self.extractor = OpenGraphExtractor()

    @patch("app.services.metadata.opengraph_extractor.httpx.Client")
    def test_tc08_web_extract(self, mock_client_class):
        """일반 웹 페이지 OpenGraph 추출"""
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_class.return_value.__exit__ = MagicMock(return_value=False)

        mock_response = MagicMock()
        mock_response.text = """
        <html><head>
            <meta property="og:title" content="테스트 기사" />
            <meta property="og:description" content="기사 설명입니다" />
            <meta property="og:image" content="https://example.com/image.jpg" />
            <meta property="og:site_name" content="테스트 뉴스" />
        </head><body></body></html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response

        result = self.extractor.extract("https://example.com/article/123")

        assert isinstance(result, ContentMetadata)
        assert result.title == '테스트 기사'
        assert result.description == '기사 설명입니다'
        assert result.thumbnail == 'https://example.com/image.jpg'
        assert result.author == '테스트 뉴스'

    @patch("app.services.metadata.opengraph_extractor.httpx.Client")
    def test_tc09_fallback_on_failure(self, mock_client_class):
        """네트워크 오류 시 URL 기반 기본 메타데이터 반환"""
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.get.side_effect = Exception("Connection error")

        result = self.extractor.extract("https://example.com/article")

        assert result.title == "https://example.com/article"
        assert result.platform == "web"


class TestFactoryFallback:
    """TC10: yt-dlp 실패 시 OpenGraph fallback"""

    @patch("app.services.metadata.opengraph_extractor.httpx.Client")
    @patch("app.services.metadata.ytdlp_extractor.yt_dlp.YoutubeDL")
    def test_tc10_ytdlp_fails_fallback_to_opengraph(self, mock_ydl_class, mock_client_class):
        """yt-dlp 실패 → OpenGraph fallback"""
        # yt-dlp 실패
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__ = MagicMock(return_value=mock_ydl)
        mock_ydl_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ydl.extract_info.side_effect = Exception("yt-dlp error")

        # OpenGraph 성공
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_response = MagicMock()
        mock_response.text = """
        <html><head>
            <meta property="og:title" content="Fallback 제목" />
        </head><body></body></html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response

        factory = MetadataExtractorFactory()
        result = factory.extract("https://www.instagram.com/p/abc/")

        assert result.title == "Fallback 제목"


class TestSaveLinkIntegration:
    """TC11: 비YouTube URL 저장 통합 테스트"""

    def test_tc11_non_youtube_url_save(self):
        """비YouTube URL이 정상적으로 저장되는지 확인"""
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
             patch("app.api.links.metadata_factory") as mock_factory, \
             patch("app.api.links.ai_service") as mock_ai:

            mock_settings.SUPABASE_JWT_SECRET = TEST_JWT_SECRET

            # 메타데이터 팩토리 모킹
            mock_factory.extract.return_value = ContentMetadata(
                title="네이버 블로그 글",
                description="블로그 내용입니다",
                thumbnail="https://blog.naver.com/thumb.jpg",
                platform="web",
            )

            mock_db.get_link_by_url = AsyncMock(return_value=None)
            mock_db.save_link = AsyncMock(return_value={
                "id": "link-web-1",
                "url": "https://blog.naver.com/post/123",
                "title": "네이버 블로그 글",
                "thumbnail": "https://blog.naver.com/thumb.jpg",
                "summary": "블로그 요약",
                "tags": ["블로그", "네이버", "정보", "일반", "추천"],
                "category": "기타",
                "media_type": "web",
                "user_id": TEST_USER_ID,
                "created_at": "2024-01-01T00:00:00",
            })
            mock_ai.generate_summary = AsyncMock(return_value="블로그 요약")
            mock_ai.generate_tags = AsyncMock(return_value=["블로그", "네이버", "정보", "일반", "추천"])
            mock_ai.categorize = AsyncMock(return_value="기타")

            response = client.post(
                "/api/links/save",
                json={"url": "https://blog.naver.com/post/123"},
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "네이버 블로그 글"
            assert data["media_type"] == "web"
            assert data["thumbnail"] == "https://blog.naver.com/thumb.jpg"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
