"""메타데이터 추출기 팩토리 - URL에 따라 적합한 추출기를 선택"""

from app.core.logging import get_logger
from .base import ContentMetadata, MetadataExtractor
from .ytdlp_extractor import YtDlpExtractor
from .opengraph_extractor import OpenGraphExtractor

logger = get_logger("metadata.factory")


class MetadataExtractorFactory:
    """URL에 따라 적합한 추출기를 선택하고, 실패 시 fallback을 실행하는 팩토리"""

    def __init__(self):
        self._ytdlp = YtDlpExtractor()
        self._opengraph = OpenGraphExtractor()

    def get_extractor(self, url: str) -> MetadataExtractor:
        """URL에 맞는 최적 추출기를 반환"""
        if self._ytdlp.can_handle(url):
            return self._ytdlp
        return self._opengraph

    def extract(self, url: str) -> ContentMetadata:
        """URL에서 메타데이터를 추출. yt-dlp 실패 시 OpenGraph fallback."""
        extractor = self.get_extractor(url)

        try:
            return extractor.extract(url)
        except Exception as e:
            # yt-dlp 실패 시 OpenGraph fallback
            if isinstance(extractor, YtDlpExtractor):
                logger.warning(f"YtDlp failed, falling back to OpenGraph: {url[:60]} ({e})")
                return self._opengraph.extract(url)
            raise


# 싱글턴 인스턴스
metadata_factory = MetadataExtractorFactory()
