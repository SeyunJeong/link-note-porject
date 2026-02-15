"""yt-dlp 기반 메타데이터 추출기 (YouTube, Instagram, TikTok, X)"""

import yt_dlp
import time
from app.core.logging import get_logger
from .base import ContentMetadata, MetadataExtractor

logger = get_logger("metadata.ytdlp")

# yt-dlp가 지원하는 도메인 목록
YTDLP_DOMAINS = [
    "youtube.com", "youtu.be", "youtube-nocookie.com",
    "instagram.com", "instagr.am",
    "tiktok.com",
    "x.com", "twitter.com",
]


class YtDlpExtractor(MetadataExtractor):
    """yt-dlp를 사용하는 멀티 플랫폼 추출기"""

    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'socket_timeout': 15,
        }
        self.max_retries = 2
        self.retry_delay = 1.0

    def can_handle(self, url: str) -> bool:
        url_lower = url.lower()
        return any(domain in url_lower for domain in YTDLP_DOMAINS)

    def extract(self, url: str) -> ContentMetadata:
        logger.info(f"YtDlp extracting: {url[:80]}")

        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                return self._extract_internal(url)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait = self.retry_delay * (attempt + 1)
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} for: {url[:60]} ({e})")
                    time.sleep(wait)

        logger.error(f"YtDlp extraction failed after retries: {url[:60]} - {last_exception}")
        raise last_exception  # type: ignore[misc]

    def _extract_internal(self, url: str) -> ContentMetadata:
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if info is None:
                    raise RuntimeError("추출 결과가 없습니다.")

                thumbnail = self._get_best_thumbnail(info)

                return ContentMetadata(
                    title=info.get('title', '') or '',
                    description=info.get('description', '') or '',
                    thumbnail=thumbnail or None,
                    platform=info.get('extractor_key', 'unknown').lower(),
                    duration=info.get('duration'),
                    author=info.get('channel') or info.get('uploader') or None,
                    view_count=info.get('view_count'),
                )

        except yt_dlp.utils.DownloadError as e:
            logger.warning(f"yt-dlp DownloadError: {e}")
            raise

    def _get_best_thumbnail(self, info: dict) -> str:
        thumbnails = info.get('thumbnails', [])
        if thumbnails:
            sorted_thumbs = sorted(
                thumbnails,
                key=lambda x: (x.get('height', 0) or 0) * (x.get('width', 0) or 0),
                reverse=True,
            )
            if sorted_thumbs:
                return sorted_thumbs[0].get('url', '')
        return info.get('thumbnail', '')
