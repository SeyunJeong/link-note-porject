import yt_dlp
import re
import time
from typing import Optional
from app.core.logging import get_logger
from app.core.exceptions import YouTubeExtractionError

logger = get_logger("youtube")


class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,  # 상세 정보 추출을 위해 False로 변경
            'skip_download': True,
        }
        self.max_retries = 2
        self.retry_delay = 1.0

    def extract_video_id(self, url: str) -> Optional[str]:
        """다양한 유튜브 URL 형식에서 video_id 추출"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def validate_youtube_url(self, url: str) -> tuple[bool, str]:
        """
        유튜브 URL 유효성 검증
        Returns: (is_valid, error_message)
        """
        if not url:
            return False, "URL이 비어있습니다."

        if not self.is_youtube_url(url):
            return False, "지원하지 않는 URL 형식입니다. YouTube URL만 지원합니다."

        video_id = self.extract_video_id(url)
        if not video_id:
            return False, "유효한 YouTube 영상 ID를 찾을 수 없습니다."

        return True, ""

    def normalize_youtube_url(self, url: str) -> str:
        """
        다양한 유튜브 URL 형식을 표준 형식으로 변환
        - youtu.be/xxx -> youtube.com/watch?v=xxx
        - 불필요한 쿼리 파라미터 제거 (si, feature 등)
        """
        video_id = self.extract_video_id(url)
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        return url

    def extract_metadata(self, url: str) -> Optional[dict]:
        """
        YouTube 영상 메타데이터 추출 (재시도 로직 포함)
        """
        logger.info(f"Extracting metadata for URL: {url}")

        # URL 유효성 검사
        is_valid, error_msg = self.validate_youtube_url(url)
        if not is_valid:
            logger.warning(f"Invalid URL: {url} - {error_msg}")
            raise YouTubeExtractionError(error_msg, "invalid_url")

        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                result = self._extract_metadata_internal(url)
                logger.info(f"Metadata extracted successfully: {result.get('title', 'N/A')[:50]}")
                return result
            except YouTubeExtractionError:
                raise  # 명확한 에러는 재시도하지 않음
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} for URL: {url}")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue

        # 모든 재시도 실패
        logger.error(f"Failed to extract metadata after retries: {url} - {last_exception}")
        raise YouTubeExtractionError(
            f"메타데이터 추출에 실패했습니다: {str(last_exception)}",
            "network_error"
        )

    def _extract_metadata_internal(self, url: str) -> dict:
        """실제 메타데이터 추출 로직"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if info is None:
                    raise YouTubeExtractionError(
                        "영상 정보를 가져올 수 없습니다.",
                        "extraction_failed"
                    )

                # 썸네일 URL 선택 (최고 화질 우선)
                thumbnail = self._get_best_thumbnail(info)

                return {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'thumbnail': thumbnail,
                    'duration': info.get('duration', 0),
                    'channel': info.get('channel', info.get('uploader', '')),
                    'channel_url': info.get('channel_url', info.get('uploader_url', '')),
                    'view_count': info.get('view_count', 0),
                    'upload_date': self._format_upload_date(info.get('upload_date', '')),
                    'tags': info.get('tags', []) or [],
                }

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            logger.warning(f"yt-dlp DownloadError: {e}")

            if 'private video' in error_msg or 'private' in error_msg:
                raise YouTubeExtractionError(
                    "비공개 영상입니다. 공개 영상만 저장할 수 있습니다.",
                    "private_video"
                )
            elif 'video unavailable' in error_msg or 'removed' in error_msg or 'deleted' in error_msg:
                raise YouTubeExtractionError(
                    "삭제되었거나 존재하지 않는 영상입니다.",
                    "video_unavailable"
                )
            elif 'geo' in error_msg or 'country' in error_msg or 'region' in error_msg:
                raise YouTubeExtractionError(
                    "해당 지역에서 재생할 수 없는 영상입니다.",
                    "geo_restricted"
                )
            elif 'age' in error_msg:
                raise YouTubeExtractionError(
                    "연령 제한 영상입니다.",
                    "age_restricted"
                )
            else:
                raise YouTubeExtractionError(
                    f"영상을 불러올 수 없습니다: {str(e)}",
                    "download_error"
                )

    def _get_best_thumbnail(self, info: dict) -> str:
        """최고 화질 썸네일 URL 반환"""
        thumbnails = info.get('thumbnails', [])
        if thumbnails:
            # 해상도가 높은 순으로 정렬
            sorted_thumbs = sorted(
                thumbnails,
                key=lambda x: (x.get('height', 0) or 0) * (x.get('width', 0) or 0),
                reverse=True
            )
            if sorted_thumbs:
                return sorted_thumbs[0].get('url', '')
        return info.get('thumbnail', '')

    def _format_upload_date(self, date_str: str) -> str:
        """업로드 날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)"""
        if date_str and len(date_str) == 8:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return date_str

    def is_youtube_url(self, url: str) -> bool:
        """유튜브 URL 여부 확인"""
        youtube_patterns = [
            'youtube.com/watch',
            'youtu.be/',
            'youtube.com/shorts',
            'youtube.com/embed',
            'youtube.com/v/',
        ]
        return any(pattern in url for pattern in youtube_patterns)


youtube_service = YouTubeService()
